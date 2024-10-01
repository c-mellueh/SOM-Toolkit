from __future__ import annotations
import SOMcreator
import logging
import os
from typing import Iterator, TYPE_CHECKING, Union, Callable
from uuid import uuid4
import copy as cp
from . import filehandling
from .constants import value_constants
from dataclasses import dataclass, field

FILTER_KEYWORD = "filter"



# Add child to Parent leads to reverse


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
            filehandling.constants.IFC_MAPPING: True
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

    def get_filter_state(self, phase: Phase, use_case: UseCase) -> bool | None:
        phase_index = self.project.get_phase_index(phase)
        use_case_index = self.project.get_use_case_index(use_case)
        if phase_index is None or use_case_index is None:
            return None
        return self._filter_matrix[phase_index][use_case_index]

    def set_filter_state(self, phase: Phase, use_case: UseCase, value: bool) -> None:
        phase_index = self.project.get_phase_index(phase)
        use_case_index = self.project.get_use_case_index(use_case)
        self._filter_matrix[phase_index][use_case_index] = value

    def remove_phase(self, phase: Phase) -> None:
        phase_index = self.project.get_phase_index(phase)
        self.get_filter_matrix().pop(phase_index)

    def remove_use_case(self, use_case: UseCase) -> None:
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
            if self.parent.is_optional:
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



class PropertySet(Hirarchy):
    _registry: set[PropertySet] = set()

    def __init__(self, name: str, obj: SOMcreator.Object = None, uuid: str = None, description: None | str = None,
                 optional: None | bool = None, project: None | SOMcreator.Project = None,
                 filter_matrix: list[list[bool]] = None) -> None:
        super(PropertySet, self).__init__(name, description, optional, project, filter_matrix)
        self._attributes = set()
        self._object = None
        if obj is not None:
            obj.add_property_set(self)  # adds Pset to Object and sets pset.object = obj
        self._registry.add(self)
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = str(uuid4())

    def __lt__(self, other):
        if isinstance(other, PropertySet):
            return self.name < other.name
        else:
            return self.name < other

    def __str__(self):
        return f"PropertySet: {self.name}"

    def __copy__(self) -> PropertySet:
        new_pset = PropertySet(name=self.name, obj=None, uuid=str(uuid4()), description=self.description,
                               optional=self.is_optional(ignore_hirarchy=True), project=self.project,
                               filter_matrix=self._filter_matrix)

        for attribute in self.get_attributes(filter=False):
            new_attribute = cp.copy(attribute)
            new_pset.add_attribute(new_attribute)

        if self.parent is not None:
            self.parent.add_child(new_pset)

        return new_pset

    @property
    def is_predefined(self) -> bool:
        return self.object is None

    @property
    def parent(self) -> PropertySet:
        parent = super(PropertySet, self).parent
        return parent

    @parent.setter
    def parent(self, parent: PropertySet) -> None:
        """
        Use parent.add_child if you want to set the parent

        :param parent:
        :return:
        """
        if parent is None:
            self.remove_parent()
            return
        self._parent = parent

    def remove_child(self, child: PropertySet) -> None:
        super().remove_child(child)
        child.remove_parent()
        for attribute in [a for a in child.get_attributes(filter=False) if a.parent]:
            attribute.parent.remove_child(attribute)

    def change_parent(self, new_parent: PropertySet) -> None:
        for attribute in self.get_attributes(filter=False):
            if attribute.parent.property_set == self._parent:
                self.remove_attribute(attribute)
        self.parent = new_parent

    def delete(self, recursive: bool = False, override_ident_deletion=False) -> None:
        ident_attrib = None
        if self.object is not None:
            ident_attrib = self.object.ident_attrib

        if ident_attrib in self.get_attributes(filter=False) and not override_ident_deletion:
            logging.error(f"Can't delete Propertyset {self.name} because it countains the identifier Attribute")
            return

        super(PropertySet, self).delete()
        [attrib.delete(recursive) for attrib in self.get_attributes(filter=False) if attrib]
        if self.object is not None:
            self.object.remove_property_set(self)

    @property
    def object(self) -> SOMcreator.Object:
        return self._object

    @object.setter
    def object(self, value: SOMcreator.Object):
        self._object = value

    @filterable
    def get_attributes(self) -> Iterator[SOMcreator.Attribute]:
        """returns all Attributes even if they don't fit the current Project Phase"""
        return iter(self._attributes)

    def add_attribute(self, value: SOMcreator.Attribute) -> None:
        if value.property_set is not None and value.property_set != self:
            value.property_set.remove_attribute(value)
        self._attributes.add(value)

        value.property_set = self
        for child in self.get_children(filter=False):
            attrib: SOMcreator.Attribute = cp.copy(value)
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value: SOMcreator.Attribute, recursive=False) -> None:
        if value in self.get_attributes(filter=False):
            self._attributes.remove(value)
            if recursive:
                for child in value.get_children(filter=False):
                    child.property_set.remove_attribute(child)
        else:
            logging.warning(f"{self.name} -> {value} not in SOMcreator.Attributes")

    def get_attribute_by_name(self, name: str):
        for attribute in self.get_attributes(filter=False):
            if attribute.name.lower() == name.lower():
                return attribute
        return None

    def create_child(self, name) -> PropertySet:
        child = PropertySet(name=name, project=self.project)
        self._children.add(child)
        child.parent = self
        for attribute in self.get_attributes(filter=False):
            new_attrib = attribute.create_child()
            child.add_attribute(new_attrib)
        return child


class Attribute(Hirarchy):
    _registry: set[Attribute] = set()

    def __init__(self, property_set: SOMcreator.PropertySet | None, name: str, value: list, value_type: str,
                 data_type: str = value_constants.LABEL,
                 child_inherits_values: bool = False, uuid: str = None, description: None | str = None,
                 optional: None | bool = None, revit_mapping: None | str = None,
                 project: SOMcreator.Project | None = None,
                 filter_matrix: list[list[bool]] = None):

        super(Attribute, self).__init__(name, description, optional, project, filter_matrix)
        self._value = value
        self._property_set = property_set
        self._value_type = value_type
        self._data_type = data_type
        self._registry.add(self)
        if revit_mapping is None:
            self._revit_name = name
        else:
            self._revit_name = revit_mapping

        self._child_inherits_values = child_inherits_values
        self.uuid = uuid

        if self.uuid is None:
            self.uuid = str(uuid4())
        if property_set is not None:
            property_set.add_attribute(self)

    def __str__(self) -> str:
        text = f"{self.property_set.name} : {self.name} = {self.value}"
        return text

    def __lt__(self, other):
        if isinstance(other, Attribute):
            return self.name < other.name
        else:
            return self.name < other

    def __copy__(self) -> Attribute:
        new_attrib = Attribute(property_set=None, name=self.name, value=cp.copy(self.value),
                               value_type=cp.copy(self.value_type),
                               data_type=cp.copy(self.data_type), child_inherits_values=self.child_inherits_values,
                               uuid=str(uuid4()),
                               description=self.description, optional=self.is_optional(ignore_hirarchy=True),
                               revit_mapping=self.revit_name,
                               project=self.project, filter_matrix=self._filter_matrix)

        if self.parent is not None:
            self.parent.add_child(new_attrib)
        return new_attrib

    def get_all_parents(self) -> list[Attribute]:
        parent = self.parent
        if parent is None:
            return []
        return parent.get_all_parents() + [parent]

    @property
    def revit_name(self) -> str:
        return self._revit_name

    @revit_name.setter
    def revit_name(self, value: str) -> None:
        self._revit_name = value

    @property
    def child_inherits_values(self) -> bool:
        return self._child_inherits_values

    @child_inherits_values.setter
    def child_inherits_values(self, value: bool) -> None:
        self._child_inherits_values = value

    @property
    def name(self) -> str:
        return super(Attribute, self).name

    @name.setter
    def name(self, value: str) -> None:
        # ToDo: add request for unlink
        self._name = value
        for child in self.get_children(filter=False):
            child.name = value

    @property
    def is_inheriting_values(self) -> bool:
        if self.parent is None:
            return False
        if self.parent.is_inheriting_values or self.parent.child_inherits_values:
            return True
        return False

    def get_own_values(self):
        """returns values without inherited values"""
        if not self.parent:
            return self._value
        return [v for v in self._value if v not in self.parent.value]

    @property
    def value(self) -> list:
        if self.is_inheriting_values:
            return self.parent.value + self.get_own_values()
        return self._value

    @value.setter
    def value(self, values: list) -> None:
        if self.is_inheriting_values:
            own_values = list()
            for value in values:
                if value not in self.parent.value:
                    own_values.append(value)
            self._value = own_values
        else:
            self._value = values

    @property
    def value_type(self) -> str:
        return self._value_type

    @value_type.setter
    def value_type(self, value: str):

        if not self.is_child:
            self._value_type = value

        if self.is_parent:
            for child in self.get_children(filter=False):
                child._value_type = value

    @property
    def data_type(self) -> str:
        """
        IfcSimpleValue -> https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/
        :return:
        """

        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> None:
        if not self.is_child:
            self._data_type = value

        if self.is_parent:
            for child in self.get_children(filter=False):
                child._data_type = value

    @property
    def property_set(self) -> SOMcreator.PropertySet:
        return self._property_set

    @property_set.setter
    def property_set(self, value: SOMcreator.PropertySet) -> None:
        self._property_set = value

    def is_equal(self, attribute: Attribute) -> bool:
        equal = True

        if self.name != attribute.name:
            equal = False

        if self.value != attribute.value:
            equal = False

        if self.property_set.name != attribute.property_set.name:
            equal = False

        if equal:
            return True
        else:
            return False

    def delete(self, recursive: bool = False) -> None:
        super(Attribute, self).delete(recursive)
        self.property_set.remove_attribute(self)

    def create_child(self) -> Attribute:
        child = cp.copy(self)
        self.add_child(child)
        return child


class Aggregation(Hirarchy):
    _registry: set[Aggregation] = set()

    def __str__(self):
        return self.name

    def __init__(self, obj: SOMcreator.Object, parent_connection=value_constants.AGGREGATION, uuid: str | None = None,
                 description: None | str = None,
                 optional: None | bool = None, filter_matrix: list[list[bool]] = None):

        super(Aggregation, self).__init__(obj.name, description, optional, obj.project, filter_matrix)
        self._registry.add(self)
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = str(uuid)
        self.object = obj
        self._parent: Aggregation | None = None
        self._parent_connection = parent_connection
        self.object.add_aggregation(self)

    def delete(self, recursive: bool = False) -> None:
        super(Aggregation, self).delete(recursive)

        self.object.remove_aggregation(self)
        if not self.is_root:
            self.parent.remove_child(self)

    @property
    def project(self) -> SOMcreator.Project | None:
        return self.object.project

    @property
    def parent_connection(self):
        if self.parent is None:
            return None
        return self._parent_connection

    @parent_connection.setter
    def parent_connection(self, value):
        self._parent_connection = value

    @property
    def parent(self) -> Aggregation:
        return self._parent

    def set_parent(self, value, connection_type):
        if self.parent is not None and value != self.parent:
            return False
        self._parent = value
        self._parent_connection = connection_type
        return True

    def add_child(self, child: Aggregation, connection_type: int = value_constants.AGGREGATION) -> bool:
        """returns if adding child is allowed"""

        def loop_parents(element, search_value):
            if element.parent is None:
                return True
            if element.parent.object == search_value:
                return False
            else:
                return loop_parents(element.parent, search_value)

        if child.object == self.object:
            return False

        if not loop_parents(self, child.object):
            return False

        if not child.set_parent(self, connection_type):
            return False

        self._children.add(child)
        child.parent_connection = connection_type
        return True

    @property
    def is_root(self):
        if self.parent is None:
            return True
        return False

    def id_group(self) -> str:
        abbrev_list = list()

        def iter_id(element: Aggregation):
            if element.parent_connection in (value_constants.AGGREGATION,
                                             value_constants.AGGREGATION + value_constants.INHERITANCE):
                abbrev_list.append(element.parent.object.abbreviation)
            if not element.is_root:
                iter_id(element.parent)

        if self.is_root:
            return ""

        iter_id(self)
        return "_xxx_".join(reversed(abbrev_list)) + "_xxx"

    def identity(self) -> str:
        return self.id_group() + "_" + self.object.abbreviation + "_xxx"


@dataclass(unsafe_hash=True)
class ProjectFilter:
    name: str
    long_name: str = field(compare=False)
    description: str = field(compare=False)
    filter_type: int = field(init=False)  # 0 = UseCase ,1 = Phase


class UseCase(ProjectFilter):
    filter_type = 0


class Phase(ProjectFilter):
    filter_type = 1


if TYPE_CHECKING:
    ClassTypes = Union[
        SOMcreator.Project, SOMcreator.Object, SOMcreator.PropertySet, SOMcreator.Attribute, SOMcreator.Aggregation]
