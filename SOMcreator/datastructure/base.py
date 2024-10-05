from __future__ import annotations
from SOMcreator.constants import value_constants
import SOMcreator
from typing import Iterator, Callable
import logging
import SOMcreator.datastructure.som_json

FILTER_KEYWORD = "filter"


def filterable(func: Callable):
    """decorator function that filters list output of function by  phase and use_case"""

    def inner(self, *args, **kwargs):
        filter_values = True
        if FILTER_KEYWORD in kwargs:
            filter_values = kwargs[FILTER_KEYWORD]
            kwargs.pop(FILTER_KEYWORD)

        result: list[Hirarchy | SOMcreator.Project] = func(self, *args, **kwargs)
        if not filter_values:
            return result

        proj: SOMcreator.Project = self if isinstance(self, SOMcreator.Project) else self.project
        if proj is None:
            return result
        return filter(lambda e: e.is_active(), result)

    return inner


class IterRegistry(type):
    _registry = set()
    """ Helper for Iteration"""

    def __iter__(self) -> Iterator[
        SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation]:
        return iter(sorted(list(self._registry), key=lambda x: x.name))

    def __len__(self) -> int:
        return len(self._registry)


class Hirarchy(object, metaclass=IterRegistry):

    def __init__(self, name: str, description: str | None = None, optional: bool | None = None,
                 project: SOMcreator.Project | None = None,
                 filter_matrix: list[list[bool]] = None) -> None:
        if project is None:
            project = SOMcreator.active_project

        self._project = project
        project.add_item(self)
        self._filter_matrix = filter_matrix
        if self._filter_matrix is None:
            self._filter_matrix = project.create_filter_matrix(True)
        self._parent = None
        self._children = set()
        self._name = name
        self._mapping_dict = {
            value_constants.SHARED_PARAMETERS:  True,
            SOMcreator.datastructure.som_json.IFC_MAPPING: True
        }
        self._description = ""
        if description is not None:
            self.description = description

        self._optional = False
        if optional is not None:
            self._optional = optional

    def remove_parent(self) -> None:
        self._parent = None

    def get_filter_matrix(self):
        return self._filter_matrix

    def get_filter_state(self, phase: SOMcreator.Phase, use_case: SOMcreator.UseCase) -> bool | None:
        if self.project:
            if not self.project.get_filter_state(phase, use_case):
                return False
        phase_index = self.project.get_phase_index(phase)
        use_case_index = self.project.get_use_case_index(use_case)
        if phase_index is None or use_case_index is None:
            return None
        return self._filter_matrix[phase_index][use_case_index]

    def set_filter_state(self, phase: SOMcreator.Phase, use_case: SOMcreator.UseCase, value: bool) -> None:
        phase_index = self.project.get_phase_index(phase)
        use_case_index = self.project.get_use_case_index(use_case)
        self._filter_matrix[phase_index][use_case_index] = value

    def remove_phase(self, phase: SOMcreator.Phase) -> None:
        phase_index = self.project.get_phase_index(phase)
        self.get_filter_matrix().pop(phase_index)

    def remove_use_case(self, use_case: SOMcreator.UseCase) -> None:
        use_case_index = self.project.get_use_case_index(use_case)
        for use_case_list in self._filter_matrix:
            use_case_list.pop(use_case_index)

    def add_project_phase(self) -> None:
        use_cases = self.project.get_usecases()
        self._filter_matrix.append([True for _ in use_cases])

    def add_use_case(self) -> None:
        for use_case_list in self._filter_matrix:
            use_case_list.append(True)

    def is_active(self) -> bool:
        """
        returns if Entity matches curren collection of usecases & phases
        Returns True if no Project with Filters exists
        """
        if not self.project:
            return True
        for phase in self.project.active_phases:
            for usecase in self.project.active_usecases:
                if self._filter_matrix[phase][usecase]:
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
    def parent(self) -> SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation:
        return self._parent

    @parent.setter
    def parent(self,
               parent: SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation) -> None:
        if self.parent is not None:
            self.parent._children.remove(self)
        self._parent = parent
        if parent is not None:
            self._parent._children.add(self)

    @property
    def is_parent(self) -> bool:
        if self.get_children(filter=False):
            return True
        else:
            return False

    @property
    def is_child(self) -> bool:
        if self.parent is not None:
            return True
        else:
            return False

    @filterable
    def get_children(self) -> Iterator[
        SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation]:
        return iter(self._children)

    def add_child(self,
                  child: SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation) -> None:
        self._children.add(child)
        child.parent = self

    def remove_child(self,
                     child: SOMcreator.PropertySet | SOMcreator.Object | SOMcreator.Attribute | SOMcreator.Aggregation | Hirarchy) -> None:
        if child in self._children:
            self._children.remove(child)
            child.remove_parent()

    def delete(self, recursive: bool = False) -> None:
        logging.info(f"Delete {self.__class__.__name__} {self.name} (recursive: {recursive})")
        if self.parent is not None:
            self.parent.remove_child(self)

        if self in self._registry:
            self._registry.remove(self)

        if recursive:
            for child in list(self.get_children(filter=False)):
                child.delete(recursive)

        else:
            for child in self.get_children(filter=False):
                child.remove_parent()
        self.project.remove_item(self)
        del self
