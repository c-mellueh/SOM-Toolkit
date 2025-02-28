from __future__ import annotations

import os
from typing import Iterator

import SOMcreator
import SOMcreator.exporter.som_json
import SOMcreator.importer.som_json
from .base import Hirarchy, filterable


class Project(object):
    def __init__(
        self,
        name: str = "",
        author: str | None = None,
        phases: list[SOMcreator.Phase] = None,
        usecase: list[SOMcreator.UseCase] = None,
        filter_matrix: list[list[bool]] = None,
    ) -> None:
        """
        filter_matrix: list[phase_index][usecase_index] = bool
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
            self._phases = [
                SOMcreator.Phase("Stand", "Standard", "Auto-Generated. Please Rename")
            ]
        else:
            self._phases = phases

        self.active_phases = [0]

        if not usecase:
            self._usecases = [
                SOMcreator.UseCase("Stand", "Standard", "Auto-Generated. Please Rename")
            ]
        else:
            self._usecases = usecase
        if filter_matrix is None:
            self._filter_matrix = self.create_filter_matrix(True)

        self.active_usecases = [0]
        self.change_log = list()

    def add_item(self, item: Hirarchy):
        self._items.add(item)

    def remove_item(self, item: Hirarchy):
        if item in self._items:
            self._items.remove(item)

    @filterable
    def get_root_objects(self) -> Iterator[SOMcreator.SOMClass]:
        return filter(lambda o: o.parent is None, self.get_objects(filter=False))

    # Item Getter Methods
    @filterable
    def get_hirarchy_items(
        self,
    ) -> Iterator[
        SOMcreator.SOMClass,
        SOMcreator.PropertySet,
        SOMcreator.SOMProperty,
        SOMcreator.SOMAggregation,
        Hirarchy,
    ]:
        return filter(
            lambda i: isinstance(
                i,
                (
                    SOMcreator.SOMClass,
                    SOMcreator.PropertySet,
                    SOMcreator.SOMProperty,
                    SOMcreator.SOMAggregation,
                ),
            ),
            self._items,
        )

    @filterable
    def get_objects(self) -> Iterator[SOMcreator.SOMClass]:
        return filter(lambda item: isinstance(item, SOMcreator.SOMClass), self._items)

    @filterable
    def get_property_sets(self) -> Iterator[SOMcreator.PropertySet]:
        return filter(
            lambda item: isinstance(item, SOMcreator.PropertySet), self._items
        )

    @filterable
    def get_attributes(self) -> Iterator[SOMcreator.SOMProperty]:
        return filter(
            lambda item: isinstance(item, SOMcreator.SOMProperty), self._items
        )

    @filterable
    def get_aggregations(self) -> Iterator[SOMcreator.SOMAggregation]:
        return filter(
            lambda item: isinstance(item, SOMcreator.SOMAggregation), self._items
        )

    @filterable
    def get_predefined_psets(self) -> Iterator[SOMcreator.PropertySet]:
        return filter(lambda p: p.is_predefined, self.get_property_sets(filter=False))

    def get_main_attribute(self) -> tuple[str, str]:
        ident_attributes = dict()
        ident_psets = dict()
        for obj in self.get_objects(filter=False):
            if not isinstance(obj.ident_attrib, SOMcreator.SOMProperty):
                continue
            ident_pset = obj.ident_attrib.property_set.name
            ident_attribute = obj.ident_attrib.name
            if ident_pset not in ident_psets:
                ident_psets[ident_pset] = 0
            if ident_attribute not in ident_attributes:
                ident_attributes[ident_attribute] = 0
            ident_psets[ident_pset] += 1
            ident_attributes[ident_attribute] += 1

        ident_attribute = sorted(ident_attributes.items(), key=lambda x: x[1])
        ident_pset = sorted(ident_psets.items(), key=lambda x: x[1])
        if ident_attribute and ident_pset:
            return ident_pset[0][0], ident_attribute[0][0]
        else:
            return "", ""

    def get_object_by_identifier(self, identifier: str) -> SOMcreator.SOMClass | None:
        return {obj.ident_value: obj for obj in self.get_objects(filter=False)}.get(
            identifier
        )

    def get_uuid_dict(self):
        pset_dict = {pset.uuid: pset for pset in self.get_property_sets(filter=False)}
        object_dict = {obj.uuid: obj for obj in self.get_objects(filter=False)}
        attribute_dict = {
            attribute.uuid: attribute for attribute in self.get_attributes(filter=False)
        }
        aggregation_dict = {
            aggreg.uuid: aggreg for aggreg in self.get_aggregations(filter=False)
        }
        full_dict = pset_dict | object_dict | attribute_dict | aggregation_dict
        if None in full_dict:
            full_dict.pop(None)
        return full_dict

    def get_element_by_uuid(
        self, uuid: str
    ) -> (
        SOMcreator.SOMProperty
        | SOMcreator.PropertySet
        | SOMcreator.SOMClass
        | SOMcreator.SOMAggregation
        | None
    ):
        """warnging: don't use in iterations will slow down code substantially"""
        if uuid is None:
            return None
        return self.get_uuid_dict().get(uuid)

    @classmethod
    def open(cls, path: str | os.PathLike) -> Project:
        return SOMcreator.importer.som_json.open_json(cls, path)

    def save(self, path: str | os.PathLike) -> dict:
        json_dict = SOMcreator.exporter.som_json.export_json(self, path)
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

    # SOMcreator.UseCase / ProjectPhase Handling

    def get_phase_by_index(self, index: int) -> SOMcreator.Phase:
        return self._phases[index]

    def get_usecase_by_index(self, index: int) -> SOMcreator.UseCase:
        return self._usecases[index]

    def create_filter_matrix(self, default_state: bool = True):
        return [
            [default_state for __ in range(len(self.get_usecases()))]
            for _ in range(len(self.get_phases()))
        ]

    def get_filter_matrix(self) -> list[list[bool]]:
        """
        [Phase][Usecase] = State
        """
        return self._filter_matrix

    def set_filter_matrix(self, matrix: list[list[bool]]):
        self._filter_matrix = matrix

    def get_filter_state(self, phase: SOMcreator.Phase, usecase: SOMcreator.UseCase):
        if phase is None or usecase is None:
            return None
        if isinstance(phase, int):
            phase = self.get_phase_by_index(phase)
        if isinstance(usecase, int):
            usecase = self.get_usecase_by_index(usecase)
        return self._filter_matrix[self.get_phase_index(phase)][
            self.get_usecase_index(usecase)
        ]

    def set_filter_state(
        self, phase: SOMcreator.Phase, usecase: SOMcreator.UseCase, value: bool
    ):
        self._filter_matrix[self.get_phase_index(phase)][
            self.get_usecase_index(usecase)
        ] = value

    def get_phase_index(self, phase: SOMcreator.Phase) -> int | None:
        if phase in self._phases:
            return self._phases.index(phase)
        return None

    def get_usecase_index(self, usecase: SOMcreator.UseCase) -> int | None:
        if usecase in self._usecases:
            return self._usecases.index(usecase)
        return None

    def get_phases(self) -> list[SOMcreator.Phase]:
        return list(self._phases)

    def get_usecases(self) -> list[SOMcreator.UseCase]:
        return list(self._usecases)

    def add_phase(self, phase: SOMcreator.Phase):

        if phase not in self._phases:
            self._phases.append(phase)
            for item in self.get_hirarchy_items(filter=False):
                item.add_phase()
            self._filter_matrix.append([True for _ in self._usecases])
        return self._phases.index(phase)

    def add_usecase(self, usecase: SOMcreator.UseCase):
        if usecase not in self._usecases:
            self._usecases.append(usecase)
            for item in self.get_hirarchy_items(filter=False):
                item.add_usecase()
            for usecase_list in self._filter_matrix:
                usecase_list.append(True)
        return self._usecases.index(usecase)

    def get_phase_by_name(self, name: str):
        for project_phase in self._phases:
            if project_phase.name == name:
                return project_phase

    def get_usecase_by_name(self, name: str):
        for usecase in self._usecases:
            if usecase.name == name:
                return usecase

    def remove_phase(self, phase: SOMcreator.Phase) -> None:
        if phase is None:
            return
        index = self.get_phase_index(phase)
        new_active_phases = [
            self.get_phase_by_index(i) for i in self.active_phases if i != index
        ]
        for item in self.get_hirarchy_items(filter=False):
            item.remove_phase(phase)
        self._phases.remove(phase)
        self._filter_matrix.pop(index)
        self.active_phases = [self.get_phase_index(ph) for ph in new_active_phases]

    def remove_usecase(self, usecase: SOMcreator.UseCase) -> None:
        if usecase is None:
            return
        index = self.get_usecase_index(usecase)

        new_active_usecases = [
            self.get_usecase_by_index(i) for i in self.active_usecases if i != index
        ]

        for item in self.get_hirarchy_items(filter=False):
            item.remove_usecase(usecase)

        self._usecases.remove(usecase)
        for usecase_list in self._filter_matrix:
            usecase_list.pop(index)
        self.active_usecases = [
            self.get_usecase_index(uc) for uc in new_active_usecases
        ]

    def export_bSDD(self, path: os.PathLike | str):
        from SOMcreator.exporter.bsdd import export

        export(self, path)
