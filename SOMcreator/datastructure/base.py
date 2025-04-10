from __future__ import annotations

import copy

from SOMcreator.constants import value_constants
import SOMcreator
from typing import Iterator, Callable, TypeVar, TYPE_CHECKING, Union
import logging
import SOMcreator.datastructure.som_json
from functools import wraps
from abc import ABC, abstractmethod, ABCMeta

if TYPE_CHECKING:
    import SOMcreator

    BASE_TYPE = TypeVar(
        "BASE_TYPE",
        SOMcreator.SOMClass,
        SOMcreator.SOMAggregation,
        SOMcreator.SOMProperty,
        SOMcreator.SOMPropertySet,
        BaseClass,
    )
    BASE_CLASSES = Union[
        SOMcreator.SOMClass,
        SOMcreator.SOMAggregation,
        SOMcreator.SOMProperty,
        SOMcreator.SOMPropertySet,
    ]

FILTER_KEYWORD = "filter"


def filterable(
    func: Callable[..., Iterator[BASE_TYPE]],
) -> Callable[..., Iterator[BASE_TYPE]]:
    """decorator function that filters list output of function by  phase and usecase"""

    @wraps(func)
    def inner(self, *args, **kwargs) -> Iterator[BASE_TYPE]:
        filter_values = True
        if FILTER_KEYWORD in kwargs:
            filter_values = kwargs[FILTER_KEYWORD]
            kwargs.pop(FILTER_KEYWORD)

        result = func(self, *args, **kwargs)
        if not filter_values:
            return result

        proj: SOMcreator.SOMProject = (
            self if isinstance(self, SOMcreator.SOMProject) else self.project
        )
        if proj is None:
            return result
        return filter(lambda e: e.is_active(), result)

    return inner


class IterRegistry(ABCMeta):
    _registry = set()
    """ Helper for Iteration"""

    def __iter__(
        self,
    ) -> Iterator[
        SOMcreator.SOMPropertySet
        | SOMcreator.SOMClass
        | SOMcreator.SOMProperty
        | SOMcreator.SOMAggregation
    ]:
        return iter(sorted(list(self._registry), key=lambda x: x.name))

    def __len__(self) -> int:
        return len(self._registry)


class BaseClass(ABC, metaclass=IterRegistry):

    def __init__(
        self: BASE_TYPE,
        name: str,
        description: str | None = None,
        optional: bool | None = None,
        project: SOMcreator.SOMProject | None = None,
        filter_matrix: list[list[bool]] | None = None,
    ) -> None:
        self._children: set[BASE_TYPE] = set()
        self._project: None | SOMcreator.SOMProject = None
        if project is not None:
            project.add_item(self)

        if filter_matrix is None:
            if project is not None:
                filter_matrix = project.create_filter_matrix(True)
            else:
                filter_matrix = []

        self._filter_matrix: list[list[bool]] = copy.deepcopy(filter_matrix)
        self._parent: BASE_TYPE | None = None  # type: ignore
        self._name = name
        self._mapping_dict = {
            value_constants.SHARED_PARAMETERS: True,
            SOMcreator.datastructure.som_json.IFC_MAPPING: True,
        }
        self._description = ""
        if description is not None:
            self.description = description

        self._optional = False
        if optional is not None:
            self._optional = optional

    def remove_parent(self: BASE_TYPE) -> None:
        if self.parent is not None:
            if self in self.parent._children:
                self.parent.remove_child(self)
        self._parent = None

    def get_filter_matrix(self):
        return copy.deepcopy(self._filter_matrix)

    def get_filter_state(
        self, phase: SOMcreator.Phase | int, usecase: SOMcreator.UseCase | int
    ) -> bool | None:
        if self.project is None:
            raise ValueError(f"Entity {self} is not linked to a project")

        if isinstance(phase, int):
            phase_index = phase
        else:
            phase_index = self.project.get_phase_index(phase)

        if isinstance(usecase, int):
            usecase_index = usecase
        else:
            usecase_index = self.project.get_usecase_index(usecase)

        phase = self.project.get_phase_by_index(phase_index)
        usecase = self.project.get_usecase_by_index(usecase_index)

        if phase_index is None:
            raise ValueError(f"phase '{phase.name}' doesn't exist for {self}")
        if usecase_index is None:
            raise ValueError(f"usecase '{usecase.name}' doesn't exist for {self}")

        return bool(self._filter_matrix[phase_index][usecase_index])

    def set_filter_state(
        self, phase: SOMcreator.Phase, usecase: SOMcreator.UseCase, value: bool
    ) -> None:
        if self.project is None:
            raise ValueError(f"Entity {self} is not linked to a project")
        phase_index = self.project.get_phase_index(phase)
        usecase_index = self.project.get_usecase_index(usecase)
        if phase_index is None or usecase_index is None:
            return
        self._filter_matrix[phase_index][usecase_index] = value

    def remove_phase(self, phase: SOMcreator.Phase) -> None:
        if self.project is None:
            raise ValueError(f"Entity {self} is not linked to a project")
        phase_index = self.project.get_phase_index(phase)
        if phase_index is None:
            raise ValueError(f"phase '{phase.name}' doesn't exist for {self}")
        self._filter_matrix.pop(phase_index)

    def remove_usecase(self, usecase: SOMcreator.UseCase) -> None:
        if self.project is None:
            raise ValueError(f"Entity {self} is not linked to a project")
        usecase_index = self.project.get_usecase_index(usecase)
        if usecase_index is None:
            raise ValueError(f"usecase '{usecase.name}' doesn't exist for {self}")
        for usecase_list in self._filter_matrix:
            usecase_list.pop(usecase_index)

    def add_phase(self) -> None:
        if self.project is None:
            raise ValueError(f"Entity {self} is not linked to a project")
        usecases = self.project.get_usecases()
        self._filter_matrix.append([True for _ in usecases])

    def add_usecase(self) -> None:
        for usecase_list in self._filter_matrix:
            usecase_list.append(True)

    def is_active(self) -> bool:
        """
        returns if Entity matches curren collection of usecases & phases
        Returns True if no Project with Filters exists
        """
        if not self.project:
            return True
        for phase_index in self.project.active_phases:
            phase = self.project.get_phase_by_index(phase_index)
            for usecase_index in self.project.active_usecases:
                usecase = self.project.get_usecase_by_index(usecase_index)
                if self.get_filter_state(phase, usecase):
                    return True
        return False

    @property
    def project(self) -> SOMcreator.SOMProject | None:
        return self._project

    @project.setter
    def project(self, value: SOMcreator.SOMProject) -> None:
        self._project = value
        value.add_item(self, overwrite_filter_matrix=False)

    def is_optional(self, ignore_hirarchy=False) -> bool:
        if ignore_hirarchy:
            return self._optional
        if self.parent is not None:
            if self.parent.is_optional():
                return True
        return self._optional

    def set_optional(self, optional: bool) -> None:
        self._optional = optional

    @property
    def description(self):
        if self.parent is None:
            return self._description
        if self._description:
            return self._description
        return self.parent.description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def mapping_dict(self) -> dict[str, bool]:
        return self._mapping_dict

    @mapping_dict.setter
    def mapping_dict(self, value: dict[str, bool]) -> None:
        self._mapping_dict = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        for child in self.get_children(filter=False):
            child.name = value

    @property
    def parent(self: BASE_TYPE) -> BASE_TYPE | None:
        return self._parent  # type: ignore

    @parent.setter
    def parent(
        self: BASE_TYPE,
        parent,
    ) -> None:
        if self.parent is not None:
            self.parent._children.remove(self)
        self._parent = parent
        if parent is not None:
            self._parent._children.add(self)

    @property
    def is_parent(self) -> bool:
        return bool(list(self.get_children(filter=False)))

    @property
    def is_child(self) -> bool:
        if self.parent is not None:
            return True
        else:
            return False

    @filterable
    def get_children(
        self: BASE_TYPE,
    ) -> Iterator[BASE_TYPE]:
        return iter(self._children)

    def add_child(
        self: BASE_TYPE,
        child: BASE_TYPE,
    ) -> None:
        self._children.add(child)
        child.parent = self  # type: ignore


    def remove_child(
        self: BASE_TYPE,
        child: BASE_TYPE,
    ) -> None:
        if child in self._children:
            self._children.remove(child)
            child.remove_parent()

    def delete(self, recursive: bool = False) -> None:
        logging.info(
            f"Delete {self.__class__.__name__} {self.name} (recursive: {recursive})"
        )
        if self.parent is not None:
            self.parent.remove_child(self)

        if recursive:
            for child in list(self.get_children(filter=False)):
                child.delete(recursive)

        else:
            for child in list(self.get_children(filter=False)):
                child.remove_parent()
        if self.project is not None:
            self.project.remove_item(self)
        del self
