from __future__ import annotations
import SOMcreator
from uuid import uuid4
from typing import Iterator
from .base import filterable, Hirarchy
import copy as cp


class SOMClass(Hirarchy):
    _registry: set[SOMClass] = set()

    def __init__(
        self,
        name: str,
        identifier_property: SOMcreator.SOMProperty | str,
        uuid: str = None,
        ifc_mapping: set[str] | None = None,
        description: None | str = None,
        optional: None | bool = None,
        abbreviation: None | str = None,
        project: None | SOMcreator.SOMProject = None,
        filter_matrix: list[list[bool]] = None,
    ) -> None:
        super(SOMClass, self).__init__(
            name, description, optional, project, filter_matrix
        )
        self._registry.add(self)
        self._property_sets: list[SOMcreator.SOMPropertySet] = list()
        self._ident_attrib = identifier_property
        self._aggregations: set[SOMcreator.SOMAggregation] = set()
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

    def __lt__(self, other: SOMClass):
        return self.ident_value < other.ident_value

    def __copy__(self):
        new_ident_property = None
        if self.is_concept:
            ident_pset = None
            new_ident_property = str(self.identifier_property)
        else:
            ident_pset = self.identifier_property.property_set

        new_property_sets = set()
        for pset in self.get_property_sets(filter=False):
            new_pset = cp.copy(pset)
            new_property_sets.add(new_pset)
            if pset == ident_pset:
                new_ident_property = new_pset.get_attribute_by_name(
                    self.identifier_property.name
                )

        if new_ident_property is None:
            raise ValueError(f"Identifier Attribute could'nt be found")

        new_object = SOMClass(
            name=self.name,
            identifier_property=new_ident_property,
            uuid=str(uuid4()),
            ifc_mapping=self.ifc_mapping,
            description=self.description,
            optional=self.is_optional(ignore_hirarchy=True),
            abbreviation=self.abbreviation,
            project=self.project,
            filter_matrix=self._filter_matrix,
        )

        for pset in new_property_sets:
            new_object.add_property_set(pset)

        if self.parent is not None:
            self.parent.add_child(new_object)

        return new_object

    @property
    def project(self) -> SOMcreator.SOMProject | None:
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
    def aggregations(self) -> set[SOMcreator.SOMAggregation]:
        return self._aggregations

    def add_aggregation(self, node: SOMcreator.SOMAggregation) -> None:
        self._aggregations.add(node)

    def remove_aggregation(self, node: SOMcreator.SOMAggregation) -> None:
        self._aggregations.remove(node)

    @property
    def inherited_property_sets(
        self,
    ) -> dict[SOMClass, list[SOMcreator.SOMPropertySet]]:
        def recursion(recursion_property_sets, recursion_obj: SOMClass):
            psets = recursion_obj.get_property_sets(filter=False)

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
        if isinstance(self.identifier_property, SOMcreator.SOMProperty):
            return False
        else:
            return True

    @property
    def identifier_property(self) -> SOMcreator.SOMProperty | str:
        return self._ident_attrib

    @identifier_property.setter
    def identifier_property(self, value: SOMcreator.SOMProperty) -> None:
        self._ident_attrib = value

    # override name setter because of intheritance
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def add_property_set(self, property_set: SOMcreator.SOMPropertySet) -> None:
        self._property_sets.append(property_set)
        property_set.som_class = self

    def remove_property_set(self, property_set: SOMcreator.SOMPropertySet) -> None:
        if property_set in self._property_sets:
            self._property_sets.remove(property_set)

    @filterable
    def get_property_sets(self) -> Iterator[SOMcreator.SOMPropertySet]:
        return iter(self._property_sets)

    @filterable
    def get_attributes(self, inherit: bool = False) -> Iterator[SOMcreator.SOMProperty]:
        attributes = list()
        for property_set in self.get_property_sets(filter=False):
            attributes += property_set.get_attributes(filter=False)
        if inherit:
            attributes += self.parent.get_attributes(inherit=True, filter=False)
        return iter(attributes)

    def delete(self, recursive: bool = False) -> None:
        super(SOMClass, self).delete(recursive)

        for pset in self.get_property_sets(filter=False):
            pset.delete(recursive, override_ident_deletion=True)

        for aggregation in self.aggregations.copy():
            aggregation.delete(recursive)

    def get_property_set_by_name(
        self, property_set_name: str
    ) -> SOMcreator.SOMPropertySet | None:
        for property_set in self.get_property_sets(filter=False):
            if property_set.name == property_set_name:
                return property_set
        return None

    @property
    def ident_value(self) -> str:
        if self.is_concept:
            return str()
        return ";".join(str(x) for x in self.identifier_property.value)
