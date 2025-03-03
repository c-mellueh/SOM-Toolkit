from __future__ import annotations

import copy

from SOMcreator.constants import value_constants
import SOMcreator
from typing import Iterator, Callable
import logging
import SOMcreator.datastructure.som_json

FILTER_KEYWORD = "filter"


def filterable(func: Callable):
    """decorator function that filters list output of function by  phase and usecase"""

    def inner(self, *args, **kwargs):
        filter_values = True
        if FILTER_KEYWORD in kwargs:
            filter_values = kwargs[FILTER_KEYWORD]
            kwargs.pop(FILTER_KEYWORD)

        result: list[Hirarchy | SOMcreator.SOMProject] = func(self, *args, **kwargs)
        if not filter_values:
            return result

        proj: SOMcreator.SOMProject = (
            self if isinstance(self, SOMcreator.SOMProject) else self.project
        )
        if proj is None:
            return result
        return filter(lambda e: e.is_active(), result)

    return inner


class IterRegistry(type):
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


class Hirarchy(object, metaclass=IterRegistry):

    def __init__(
        self,
        name: str,
        description: str | None = None,
        optional: bool | None = None,
        project: SOMcreator.SOMProject | None = None,
        filter_matrix: list[list[bool]] = None,
    ) -> None:
        if project is None:
            project = SOMcreator.active_project

        self._project = project
        project.add_item(self)

        if filter_matrix is None:
            filter_matrix = project.create_filter_matrix(True)

        self._filter_matrix = copy.deepcopy(filter_matrix)
        self._parent = None
        self._children = set()
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

    def remove_parent(self) -> None:
        if self.parent is not None:
            if self in self.parent._children:
                self.parent.remove_child(self)
        self._parent = None

    def get_filter_matrix(self):
        return copy.deepcopy(self._filter_matrix)

    def get_filter_state(
        self, phase: SOMcreator.Phase, usecase: SOMcreator.UseCase
    ) -> bool | None:
        if self.project:
            if not self.project.get_filter_state(phase, usecase):
                return False

        if isinstance(phase, int):
            phase_index = phase
        else:
            phase_index = self.project.get_phase_index(phase)
        if isinstance(usecase, int):
            usecase_index = usecase
        else:
            usecase_index = self.project.get_usecase_index(usecase)
        if phase_index is None or usecase_index is None:
            return None
        return bool(self._filter_matrix[phase_index][usecase_index])

    def set_filter_state(
        self, phase: SOMcreator.Phase, usecase: SOMcreator.UseCase, value: bool
    ) -> None:
        phase_index = self.project.get_phase_index(phase)
        usecase_index = self.project.get_usecase_index(usecase)
        self._filter_matrix[phase_index][usecase_index] = value

    def remove_phase(self, phase: SOMcreator.Phase) -> None:
        phase_index = self.project.get_phase_index(phase)
        self._filter_matrix.pop(phase_index)

    def remove_usecase(self, usecase: SOMcreator.UseCase) -> None:
        usecase_index = self.project.get_usecase_index(usecase)
        for usecase_list in self._filter_matrix:
            usecase_list.pop(usecase_index)

    def add_phase(self) -> None:
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
        for phase in self.project.active_phases:
            for usecase in self.project.active_usecases:
                if self.get_filter_state(phase, usecase):
                    return True
        return False

    @property
    def project(self):
        return self._project

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
    def parent(
        self,
    ) -> (
        SOMcreator.SOMPropertySet
        | SOMcreator.SOMClass
        | SOMcreator.SOMProperty
        | SOMcreator.SOMAggregation
    ):
        return self._parent

    @parent.setter
    def parent(
        self,
        parent: (
            SOMcreator.SOMPropertySet
            | SOMcreator.SOMClass
            | SOMcreator.SOMProperty
            | SOMcreator.SOMAggregation
        ),
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
        self,
    ) -> Iterator[
        SOMcreator.SOMPropertySet
        | SOMcreator.SOMClass
        | SOMcreator.SOMProperty
        | SOMcreator.SOMAggregation
    ]:
        return iter(self._children)

    def add_child(
        self,
        child: (
            SOMcreator.SOMPropertySet
            | SOMcreator.SOMClass
            | SOMcreator.SOMProperty
            | SOMcreator.SOMAggregation
        ),
    ) -> None:
        self._children.add(child)
        child.parent = self

    def remove_child(
        self,
        child: (
            SOMcreator.SOMPropertySet
            | SOMcreator.SOMClass
            | SOMcreator.SOMProperty
            | SOMcreator.SOMAggregation
            | Hirarchy
        ),
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

        if self in self._registry:
            self._registry.remove(self)

        if recursive:
            for child in list(self.get_children(filter=False)):
                child.delete(recursive)

        else:
            for child in list(self.get_children(filter=False)):
                child.remove_parent()
        self.project.remove_item(self)
        del self
