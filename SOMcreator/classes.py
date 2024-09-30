from __future__ import annotations
import SOMcreator
import logging
import os
from typing import Iterator, Union
from uuid import uuid4

import copy as cp
from anytree import AnyNode

from . import filehandling
from .constants import value_constants
from dataclasses import dataclass, field


# Add child to Parent leads to reverse

def _create_filter_matrix(phase_count, usecase_count, default=True):
    return [[default for __ in range(usecase_count)] for _ in range(phase_count)]


def filter_by_filter_dict(func):
    """decorator function that filters list output of function by project phase and use_case"""

    def inner(self):
        result: list[Hirarchy | Project] = func(self)
        proj: Project = self if isinstance(self, Project) else self.project
        entities = list()
        for entity in result:
            filter_matrix = entity.get_filter_matrix()
            res = False
            for phase in proj.active_phases:
                for usecase in proj.active_usecases:
                    if filter_matrix[phase][usecase]:
                        res = True
                        break  # Exit the usecase loop
                if res:
                    break  # Exit the phase loop
            if res:
                entities.append(entity)
        return entities

    return inner


def get_element_by_uuid(uuid: str, proj: SOMcreator.Project) -> Attribute | PropertySet | Object | Aggregation | None:
    if uuid is None:
        return None
    return proj.get_uuid_dict().get(uuid)


class IterRegistry(type):
    _registry = set()
    """ Helper for Iteration"""

    def __iter__(self) -> Iterator[PropertySet | Object | Attribute | Aggregation]:
        return iter(sorted(list(self._registry), key=lambda x: x.name))

    def __len__(self) -> int:
        return len(self._registry)


class Project(object):
    def __init__(self, name: str = "", author: str | None = None, phases: list[Phase] = None,
                 use_case: list[UseCase] = None, filter_matrix: list[list[bool]] = None) -> None:
        """
        filter_matrix: list[phase_index][use_case_index] = bool
        """
        SOMcreator.active_project = self
        self._items = set()
        self._name = ""
        self._author = author
        self._version = "1.0.0"
        self.name = name
        self.aggregation_attribute = ""
        self.aggregation_pset = ""
        self._filter_matrix = filter_matrix
        self._description = ""
        self.plugin_dict = dict()
        self.import_dict = dict()

        if phases is None:
            self._phases = [Phase("Stand", "Standard", "Automatisch generiert. Bitte umbenennen")]
        else:
            self._phases = phases

        self.active_phases = [0]

        if not use_case:
            self._use_cases = [UseCase("Stand", "Standard", "Automatisch generiert. Bitte umbenennen")]
        else:
            self._use_cases = use_case
        if filter_matrix is None:
            self._filter_matrix = self.create_filter_matrix(True)

        self.active_usecases = [0]
        self.change_log = list()

    def add_item(self, item: Hirarchy):
        self._items.add(item)

    def remove_item(self, item: Hirarchy):
        if item in self._items:
            self._items.remove(item)

    # Item Getter Methods
    def get_all_hirarchy_items(self) -> Iterator[Object, PropertySet, Attribute, Aggregation, Hirarchy]:
        return filter(lambda i: isinstance(i, (Object, PropertySet, Attribute, Aggregation)), self._items)

    def get_all_objects(self) -> Iterator[Object]:
        return filter(lambda item: isinstance(item, Object), self._items)

    def get_all_property_sets(self) -> Iterator[PropertySet]:
        return filter(lambda item: isinstance(item, PropertySet), self._items)

    def get_all_attributes(self) -> Iterator[Attribute]:
        return filter(lambda item: isinstance(item, Attribute), self._items)

    def get_all_aggregations(self) -> Iterator[Aggregation]:
        return filter(lambda item: isinstance(item, Aggregation), self._items)

    def get_predefined_psets(self) -> set[PropertySet]:
        return set(filter(lambda p: p.is_predefined, self.get_all_property_sets()))

    def get_main_attribute(self) -> tuple[str, str]:
        ident_attributes = dict()
        ident_psets = dict()
        for obj in self.objects:
            if not isinstance(obj.ident_attrib, Attribute):
                continue
            ident_pset = obj.ident_attrib.property_set.name
            ident_attribute = obj.ident_attrib.name
            if ident_pset not in ident_psets:
                ident_psets[ident_pset] = 0
            if ident_attribute not in ident_attributes:
                ident_attributes[ident_attribute] = 0
            ident_psets[ident_pset] += 1
            ident_attributes[ident_attribute] += 1

        ident_attribute = (sorted(ident_attributes.items(), key=lambda x: x[1]))
        ident_pset = (sorted(ident_psets.items(), key=lambda x: x[1]))
        if ident_attribute and ident_pset:
            return ident_pset[0][0], ident_attribute[0][0]
        else:
            return "", ""

    def get_object_by_identifier(self, identifier: str) -> Object | None:
        return {obj.ident_value: obj for obj in self.get_all_objects()}.get(identifier)

    def get_uuid_dict(self):
        pset_dict = {pset.uuid: pset for pset in self.get_all_property_sets()}
        object_dict = {obj.uuid: obj for obj in self.get_all_objects()}
        attribute_dict = {attribute.uuid: attribute for attribute in self.get_all_attributes()}
        aggregation_dict = {aggreg.uuid: aggreg for aggreg in self.get_all_aggregations()}
        full_dict = pset_dict | object_dict | attribute_dict | aggregation_dict
        if None in full_dict:
            full_dict.pop(None)
        return full_dict

    def get_element_by_uuid(self, uuid: str) -> Attribute | PropertySet | Object | Aggregation | None:
        """warnging: don't use in iterations will slow down code substantially"""
        if uuid is None:
            return None
        return self.get_uuid_dict().get(uuid)

    @classmethod
    def open(cls, path: str | os.PathLike) -> Project:
        return filehandling.open_json(cls, path)

    def save(self, path: str | os.PathLike) -> dict:
        json_dict = filehandling.export_json(self, path)
        return json_dict

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    # UseCase / ProjectPhase Handling

    def get_phase_by_index(self, index: int) -> Phase:
        return self._phases[index]

    def get_usecase_by_index(self, index: int) -> UseCase:
        return self._use_cases[index]

    def create_filter_matrix(self, default_state: bool = True):
        return _create_filter_matrix(len(self._phases), len(self._use_cases), default_state)

    def get_filter_matrix(self) -> list[list[bool]]:
        """
        [Phase][Usecase] = State
        """
        return self._filter_matrix

    def set_filter_matrix(self, matrix: list[list[bool]]):
        self._filter_matrix = matrix

    def get_filter_state(self, phase: Phase, use_case: UseCase):
        return self._filter_matrix[self.get_phase_index(phase)][self.get_use_case_index(use_case)]

    def set_filter_state(self, phase: Phase, use_case: UseCase, value: bool):
        self._filter_matrix[self.get_phase_index(phase)][self.get_use_case_index(use_case)] = value

    def get_phase_index(self, phase: Phase) -> int | None:
        if phase in self._phases:
            return self._phases.index(phase)
        return None

    def get_use_case_index(self, use_case: UseCase) -> int | None:
        if use_case in self._use_cases:
            return self._use_cases.index(use_case)
        return None

    def get_phases(self) -> list[Phase]:
        return list(self._phases)

    def get_usecases(self) -> list[UseCase]:
        return list(self._use_cases)

    def add_project_phase(self, phase: Phase):
        if phase not in self._phases:
            self._phases.append(phase)
            for item in self.get_all_hirarchy_items():
                item.add_project_phase()
            self._filter_matrix.append([True for _ in self._use_cases])
        return self._phases.index(phase)

    def add_use_case(self, use_case: UseCase):
        if use_case not in self._use_cases:
            self._use_cases.append(use_case)
            for item in self.get_all_hirarchy_items():
                item.add_use_case()
            for use_case_list in self._filter_matrix:
                use_case_list.append(True)
        return self._use_cases.index(use_case)

    def get_phase_by_name(self, name: str):
        for project_phase in self._phases:
            if project_phase.name == name:
                return project_phase

    def get_use_case_by_name(self, name: str):
        for use_case in self._use_cases:
            if use_case.name == name:
                return use_case

    def remove_phase(self, phase: Phase) -> None:
        if phase is None:
            return
        index = self.get_phase_index(phase)
        for item in self.get_all_hirarchy_items():
            item.remove_phase(phase)
        self._phases.remove(phase)
        self._filter_matrix.pop(index)
        if index in self.active_phases:
            self.active_phases.remove(index)

    def remove_use_case(self, use_case: UseCase) -> None:
        if use_case is None:
            return
        index = self.get_use_case_index(use_case)
        for item in self.get_all_hirarchy_items():
            item.remove_use_case(use_case)

        self._use_cases.remove(use_case)
        for use_case_list in self._filter_matrix:
            use_case_list.pop(index)

        if index in self.active_phases:
            self.active_phases.remove(index)

    @property
    @filter_by_filter_dict
    def objects(self) -> Iterator[Object]:
        return self.get_all_objects()

    @property
    @filter_by_filter_dict
    def property_sets(self) -> Iterator[PropertySet]:
        return self.get_all_property_sets()

    @property
    @filter_by_filter_dict
    def attributes(self) -> Iterator[Attribute]:
        return self.get_all_attributes()

    @property
    @filter_by_filter_dict
    def aggregations(self) -> list[Aggregation]:
        aggregations = list(Aggregation)
        return aggregations


class Hirarchy(object, metaclass=IterRegistry):

    def __init__(self, name: str, description: str | None = None, optional: bool | None = None,
                 project: Project | None = None,
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

    @property
    def project(self):
        return self._project

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

    @property
    def optional_wo_hirarchy(self) -> bool:
        return self._optional

    @property
    def optional(self) -> bool:
        if self.parent is not None:
            if self.parent.optional:
                return True
        return self._optional

    @optional.setter
    def optional(self, value: bool) -> None:
        self._optional = value

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
        for child in self.children:
            child.name = value

    @property
    def parent(self) -> PropertySet | Object | Attribute | Aggregation:
        return self._parent

    @parent.setter
    def parent(self, parent: PropertySet | Object | Attribute | Aggregation) -> None:
        if self.parent is not None:
            self.parent._children.remove(self)
        self._parent = parent
        if parent is not None:
            self._parent._children.add(self)

    @property
    def is_parent(self) -> bool:
        if self.children:
            return True
        else:
            return False

    @property
    def is_child(self) -> bool:
        if self.parent is not None:
            return True
        else:
            return False

    @property
    @filter_by_filter_dict
    def children(self) -> set[PropertySet | Object | Attribute | Aggregation]:
        return self._children

    def get_all_children(self):
        return self._children

    def add_child(self, child: PropertySet | Object | Attribute | Aggregation) -> None:
        self._children.add(child)
        child.parent = self

    def remove_child(self, child: PropertySet | Object | Attribute | Aggregation | Hirarchy) -> None:
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
            for child in list(self.children):
                child.delete(recursive)

        else:
            for child in self.children:
                child.remove_parent()
        self.project.remove_item(self)
        del self


class Object(Hirarchy):
    _registry: set[Object] = set()

    def __init__(self, name: str, ident_attrib: [Attribute, str], uuid: str = None,
                 ifc_mapping: set[str] | None = None, description: None | str = None,
                 optional: None | bool = None, abbreviation: None | str = None, project: None | Project = None,
                 filter_matrix: list[list[bool]] = None) -> None:
        super(Object, self).__init__(name, description, optional, project, filter_matrix)
        self._registry.add(self)
        self._property_sets: list[PropertySet] = list()
        self._ident_attrib = ident_attrib
        self._aggregations: set[Aggregation] = set()
        self.custom_attribues = {}

        self._abbreviation = abbreviation
        if abbreviation is None:
            self._abbreviation = ""

        self._ifc_mapping = ifc_mapping
        if ifc_mapping is None:
            self._ifc_mapping = {"IfcBuildingElementProxy"}

        self.uuid = uuid
        if uuid is None:
            self.uuid = str(uuid4())

    def __str__(self):
        return f"Object {self.name}"

    def __lt__(self, other: Object):
        return self.ident_value < other.ident_value

    def __copy__(self):
        new_ident_attribute = None
        if self.is_concept:
            ident_pset = None
            new_ident_attribute = str(self.ident_attrib)
        else:
            ident_pset = self.ident_attrib.property_set

        new_property_sets = set()
        for pset in self.property_sets:
            new_pset = cp.copy(pset)
            new_property_sets.add(new_pset)
            if pset == ident_pset:
                new_ident_attribute = new_pset.get_attribute_by_name(self.ident_attrib.name)

        if new_ident_attribute is None:
            raise ValueError(f"Identifier Attribute could'nt be found")

        new_object = Object(name=self.name, ident_attrib=new_ident_attribute, uuid=str(uuid4()),
                            ifc_mapping=self.ifc_mapping,
                            description=self.description, optional=self.optional, abbreviation=self.abbreviation,
                            project=self.project, filter_matrix=self._filter_matrix)

        for pset in new_property_sets:
            new_object.add_property_set(pset)

        if self.parent is not None:
            self.parent.add_child(new_object)

        return new_object

    @property
    def project(self) -> Project | None:
        return self._project

    @property
    def abbreviation(self) -> str:
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, value) -> None:
        self._abbreviation = value

    @property
    def ifc_mapping(self) -> set[str]:
        return self._ifc_mapping

    @ifc_mapping.setter
    def ifc_mapping(self, value: set[str]):
        value_set = set()
        for item in value:  # filter empty Inputs
            if not (item == "" or item is None):
                value_set.add(item)
        self._ifc_mapping = value_set

    def add_ifc_map(self, value: str) -> None:
        self._ifc_mapping.add(value)

    def remove_ifc_map(self, value: str) -> None:
        self._ifc_mapping.remove(value)

    @property
    def aggregations(self) -> set[Aggregation]:
        return self._aggregations

    def add_aggregation(self, node: Aggregation) -> None:
        self._aggregations.add(node)

    def remove_aggregation(self, node: Aggregation) -> None:
        self._aggregations.remove(node)

    @property
    def inherited_property_sets(self) -> dict[Object, list[PropertySet]]:
        def recursion(recursion_property_sets, recursion_obj: Object):
            psets = recursion_obj.property_sets

            if psets:
                recursion_property_sets[recursion_obj] = psets

            parent = recursion_obj.parent
            if parent is not None:
                recursion_property_sets = recursion(recursion_property_sets, parent)
            return recursion_property_sets

        property_sets = dict()
        if self.parent is not None:
            inherited_property_sets = recursion(property_sets, self.parent)
        else:
            inherited_property_sets = dict()

        return inherited_property_sets

    @property
    def is_concept(self) -> bool:
        if isinstance(self.ident_attrib, Attribute):
            return False
        else:
            return True

    @property
    def ident_attrib(self) -> Attribute | str:
        return self._ident_attrib

    @ident_attrib.setter
    def ident_attrib(self, value: Attribute) -> None:
        self._ident_attrib = value

    def get_all_property_sets(self) -> list[PropertySet]:
        """returns all Propertysets even if they don't fit the current Project Phase"""
        return self._property_sets

    @property
    @filter_by_filter_dict
    def property_sets(self) -> list[PropertySet]:
        return sorted(self._property_sets, key=lambda x: x.name)

    # override name setter because of intheritance
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def add_property_set(self, property_set: PropertySet) -> None:
        self._property_sets.append(property_set)
        property_set.object = self

    def remove_property_set(self, property_set: PropertySet) -> None:
        if property_set in self._property_sets:
            self._property_sets.remove(property_set)

    def get_all_attributes(self, inherit: bool = False) -> list[Attribute]:
        attributes = list()
        for property_set in self.get_all_property_sets():
            attributes += property_set.attributes

        if inherit:
            attributes += self.parent.get_attributes(inherit=True)

        return attributes

    @filter_by_filter_dict
    def get_attributes(self, inherit: bool = False) -> list[Attribute]:
        return self.get_all_attributes(inherit)

    def delete(self, recursive: bool = False) -> None:
        super(Object, self).delete(recursive)

        for pset in self.get_all_property_sets():
            pset.delete(recursive, override_ident_deletion=True)

        for aggregation in self.aggregations.copy():
            aggregation.delete(recursive)

    def get_property_set_by_name(self, property_set_name: str) -> PropertySet | None:
        for property_set in self.get_all_property_sets():
            if property_set.name == property_set_name:
                return property_set
        return None

    @property
    def ident_value(self) -> str:
        if self.is_concept:
            return str()
        return ";".join(str(x) for x in self.ident_attrib.value)


class PropertySet(Hirarchy):
    _registry: set[PropertySet] = set()

    def __init__(self, name: str, obj: Object = None, uuid: str = None, description: None | str = None,
                 optional: None | bool = None, project: None | Project = None,
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
                               optional=self.optional, project=self.project,
                               filter_matrix=self._filter_matrix)

        for attribute in self.attributes:
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
        for attribute in [a for a in child.attributes if a.parent]:
            attribute.parent.remove_child(attribute)

    def change_parent(self, new_parent: PropertySet) -> None:
        for attribute in self.attributes:
            if attribute.parent.property_set == self._parent:
                self.remove_attribute(attribute)
        self.parent = new_parent

    def delete(self, recursive: bool = False, override_ident_deletion=False) -> None:
        ident_attrib = None
        if self.object is not None:
            ident_attrib = self.object.ident_attrib

        if ident_attrib in self.attributes and not override_ident_deletion:
            logging.error(f"Can't delete Propertyset {self.name} because it countains the identifier Attribute")
            return

        super(PropertySet, self).delete()
        [attrib.delete(recursive) for attrib in self.attributes if attrib]
        if self.object is not None:
            self.object.remove_property_set(self)

    @property
    def object(self) -> Object:
        return self._object

    @object.setter
    def object(self, value: Object):
        self._object = value

    def get_all_attributes(self) -> set[Attribute]:
        """returns all Attributes even if they don't fit the current Project Phase"""
        return self._attributes

    @property
    @filter_by_filter_dict
    def attributes(self) -> list[Attribute]:
        """returns Attributes filtered"""
        return sorted(self._attributes, key=lambda a: a.name)

    @attributes.setter
    def attributes(self, value: set[Attribute]) -> None:
        self._attributes = value

    def add_attribute(self, value: Attribute) -> None:
        if value.property_set is not None and value.property_set != self:
            value.property_set.remove_attribute(value)
        self._attributes.add(value)

        value.property_set = self
        for child in self.children:
            attrib: Attribute = cp.copy(value)
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value: Attribute, recursive=False) -> None:
        if value in self.attributes:
            self._attributes.remove(value)
            if recursive:
                for child in list(value.children):
                    child.property_set.remove_attribute(child)
        else:
            logging.warning(f"{self.name} -> {value} not in Attributes")

    def get_attribute_by_name(self, name: str):
        for attribute in self.attributes:
            if attribute.name.lower() == name.lower():
                return attribute
        return None

    def create_child(self, name) -> PropertySet:
        child = PropertySet(name=name, project=self.project)
        self._children.add(child)
        child.parent = self
        for attribute in self.attributes:
            new_attrib = attribute.create_child()
            child.add_attribute(new_attrib)
        return child


class Attribute(Hirarchy):
    _registry: set[Attribute] = set()

    def __init__(self, property_set: PropertySet | None, name: str, value: list, value_type: str,
                 data_type: str = value_constants.LABEL,
                 child_inherits_values: bool = False, uuid: str = None, description: None | str = None,
                 optional: None | bool = None, revit_mapping: None | str = None, project: Project | None = None,
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
                               description=self.description, optional=self.optional, revit_mapping=self.revit_name,
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
        for child in self.children:
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
            for child in self.children:
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
            for child in self.children:
                child._data_type = value

    @property
    def property_set(self) -> PropertySet:
        return self._property_set

    @property_set.setter
    def property_set(self, value: PropertySet) -> None:
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

    def __init__(self, obj: Object, parent_connection=value_constants.AGGREGATION, uuid: str | None = None,
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
    def project(self) -> Project | None:
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


ClassTypes = Union[Project, Object, PropertySet, Attribute, Aggregation]
