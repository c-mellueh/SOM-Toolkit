from __future__ import annotations
import SOMcreator
from uuid import uuid4
from typing import Iterator
from .base import filterable, BaseClass
import copy as cp
from typing import TYPE_CHECKING

from SOMcreator.datastructure import ifc_schema
from SOMcreator.datastructure.ifc_schema import VERSION_TYPE


class SOMClass(BaseClass):
    def __init__(
        self,
        name: str,
        identifier_property: SOMcreator.SOMProperty | str | None = None,
        uuid: str | None = None,
        ifc_mapping: dict[VERSION_TYPE, list[str]] | None = None,
        description: None | str = None,
        optional: None | bool = None,
        abbreviation: None | str = None,
        project: None | SOMcreator.SOMProject = None,
        filter_matrix: list[list[bool]] | None = None,
    ) -> None:
        self._property_sets: list[SOMcreator.SOMPropertySet] = list()
        super(SOMClass, self).__init__(
            name, description, optional, project, filter_matrix
        )
        self._aggregations: set[SOMcreator.SOMAggregation] = set()
        self._abbreviation = "" if abbreviation is None else abbreviation
        self._ifc_mapping: dict[VERSION_TYPE, list[str]] = (
            dict() if ifc_mapping is None else ifc_mapping
        )
        self.uuid = str(uuid4()) if uuid is None else uuid
        self._ident_property = (
            str(self.uuid) if identifier_property is None else identifier_property
        )

    def __str__(self):
        return f"Class: {self.name}"

    def __lt__(self, other: SOMClass):
        return self.ident_value < other.ident_value

    def __copy__(self):
        new_ident_property = None
        ident_property_name = ""
        if self.is_concept:
            ident_pset = None
            new_ident_property = str(self.identifier_property)
            ident_property_name = new_ident_property
        else:
            if isinstance(self.identifier_property, SOMcreator.SOMProperty):
                ident_pset = self.identifier_property.property_set
                if ident_pset is None:
                    raise ValueError(f"Identifier PropertySet dne")
                ident_property_name = self.identifier_property.name
            else:
                raise ValueError(f"Identifier Property dne")

        new_property_sets = set()
        for pset in self.get_property_sets(filter=False):
            new_pset = cp.copy(pset)
            new_property_sets.add(new_pset)
            if pset == ident_pset:
                new_ident_property = new_pset.get_property_by_name(ident_property_name)

        if new_ident_property is None:
            raise ValueError(f"Identifier Property could'nt be found")

        new_class = SOMClass(
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
            new_class.add_property_set(pset)

        if self.parent is not None:
            self.parent.add_child(new_class)  # type: ignore

        return new_class

    @property
    def project(self) -> SOMcreator.SOMProject | None:
        return self._project

    @project.setter
    def project(self, value: SOMcreator.SOMProject) -> None:
        super(SOMClass, self.__class__).project.__set__(self, value)

    @property
    def abbreviation(self) -> str:
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, value) -> None:
        self._abbreviation = value

    @property
    def ifc_mapping(self) -> dict[VERSION_TYPE, list[str]]:
        return self._ifc_mapping

    @ifc_mapping.setter
    def ifc_mapping(self, mapping_dict: dict[VERSION_TYPE, list[str]]):
        self._ifc_mapping = dict()

        for version, values in mapping_dict.items():
            self._ifc_mapping[version] = list()
            classes = ifc_schema.get_all_classes(version)
            for value in values:
                if ifc_schema.PREDEFINED_SPLITTER in value:
                    class_name, predefined_type = value.split(
                        ifc_schema.PREDEFINED_SPLITTER
                    )
                else:
                    class_name, predefined_type = value, None
                if class_name not in classes:
                    continue
                if predefined_type:
                    allowed_types = ifc_schema.get_predefined_types(class_name, version)
                    if predefined_type not in allowed_types:
                        value = class_name
                self._ifc_mapping[version].append(value)

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
        def recursion(recursion_property_sets, recursion_class: SOMClass):
            psets = recursion_class.get_property_sets(filter=False)

            if psets:
                recursion_property_sets[recursion_class] = psets

            parent = recursion_class.parent
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
    def identifier_property(self) -> SOMcreator.SOMProperty | str | None:
        return self._ident_property

    @identifier_property.setter
    def identifier_property(self, value: SOMcreator.SOMProperty | str | None) -> None:
        self._ident_property = value

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
        property_set.project = self.project

    def remove_property_set(self, property_set: SOMcreator.SOMPropertySet) -> None:
        if property_set in self._property_sets:
            self._property_sets.remove(property_set)

    @filterable
    def get_property_sets(self) -> Iterator[SOMcreator.SOMPropertySet]:
        return iter(self._property_sets)

    @filterable
    def get_properties(self, inherit: bool = False) -> Iterator[SOMcreator.SOMProperty]:
        properties = list()
        for property_set in self.get_property_sets(filter=False):
            properties += property_set.get_properties(filter=False)
        if inherit:
            if self.parent is not None:
                properties += self.parent.get_properties(inherit=True, filter=False)
        return iter(properties)

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
        if isinstance(self.identifier_property, SOMcreator.SOMProperty):
            return ";".join(str(x) for x in self.identifier_property.allowed_values)
        else:
            return str(self.identifier_property)
