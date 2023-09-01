from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING

import SOMcreator
import ifcopenshell
from ifcopenshell.util import element
from PySide6.QtWidgets import QLineEdit,QFileDialog
from SOMcreator import classes

from .ifc_mod_window import IfcWindow, IfcRunner

if TYPE_CHECKING:
    from ..main_window import MainWindow

from .. import settings

FILE_SPLIT = "; "
ELEMENT = "Element"
GROUP = "SubGroup"
IFC_REP = "IfcRep"
DESCRIPTION = "automatisch erzeugt"
NAME = "bauteilName"


class GroupingWindow(IfcWindow):
    def __init__(self, main_window: MainWindow):
        super(GroupingWindow, self).__init__(main_window)
        self.setWindowTitle("Gruppen erzeugen")
        self.create_group_line_input()
        self.set_fixed_sizes()
        self.adjustSize()
        self.widget.label_export.setText("Export Ordner")
        if settings.get_group_folder():
            self.widget.line_edit_export.setText(settings.get_group_folder())
        else:
            self.widget.line_edit_export.setText("")

    def export_file_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "Ausgabe Ordner", settings.get_group_folder())
        if not path:
            return
        settings.set_group_folder(path)
        self.widget.line_edit_export.setText(path)


    def set_fixed_sizes(self):
        def set_line_edit_size(le: QLineEdit):
            text = le.text()
            fm = le.fontMetrics()
            width = fm.boundingRect(text).width()
            le.setMinimumSize(max(width, le.width()), le.height())

        set_line_edit_size(self.widget.line_edit_ident_pset)
        set_line_edit_size(self.widget.line_edit_ident_attribute)

    def create_group_line_input(self):
        self.line_edit_group_pset = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_pset, 1, 0, 1, 1)
        self.line_edit_group_attrib = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_attrib, 1, 1, 1, 1)
        self.line_edit_group_pset.setPlaceholderText("Gruppen PropertySet")
        self.line_edit_group_attrib.setPlaceholderText("Gruppen Attribut")
        self.line_edit_group_attrib.setText(self.main_window.project.aggregation_attribute)
        self.line_edit_group_pset.setText(self.main_window.project.aggregation_pset)
        self.line_edit_group_attrib.textEdited.connect(self.update_grouping_values)
        self.line_edit_group_pset.textEdited.connect(self.update_grouping_values)

    def start_task(self) -> tuple:
        proj, ifc, pset, attribute, export_path = super(GroupingWindow, self).start_task()
        group_pset = self.line_edit_group_pset.text()
        group_attribute = self.line_edit_group_attrib.text()
        self.runner = Grouping(ifc, proj, pset, attribute, export_path, group_pset, group_attribute, "identitaet")
        self.connect_runner(self.runner)
        self.thread_pool.start(self.runner)

        return proj, ifc, pset, attribute, export_path

    def update_grouping_values(self):
        group_pset = self.line_edit_group_pset.text()
        group_attrib = self.line_edit_group_attrib.text()
        self.main_window.project.aggregation_pset = group_pset
        self.main_window.project.aggregation_attribute = group_attrib


class Grouping(IfcRunner):

    def __init__(self, ifc_paths: str, project: classes.Project, main_pset: str, main_attribute: str,
                 export_folder: str, group_pset: str, group_attrib: str, identity_attrib: str):
        super(Grouping, self).__init__(ifc_paths, project, main_pset, main_attribute, "Gruppierung")

        self.group_pset = group_pset
        self.group_attribute = group_attrib
        self.identity_attribute = identity_attrib
        self.kuerzel_dict = {obj.abbreviation.upper(): obj for obj in self.project.objects}
        self.bk_dict = {obj.ident_value: obj for obj in self.project.objects}
        self.structure_dict = {GROUP: {}, ELEMENT: {}, IFC_REP: None}
        self.entity_object_dict: [ifcopenshell.entity_instance, SOMcreator.Object] = dict()
        self.owner_history = None
        self.export_path = export_folder

    def run(self) -> None:
        super(Grouping, self).run()

    def run_file_function(self, file_path) -> ifcopenshell.file:
        ifc_file = super(Grouping, self).run_file_function(file_path)
        self.create_group_for_file(ifc_file)
        return ifc_file

    def create_group_for_file(self, ifc_file: ifcopenshell.file):
        self.signaller.progress.emit(0)
        self.signaller.status.emit("create Structure Dict")
        self.create_structure_dict(ifc_file)
        if self.is_aborted:
            return

        self.signaller.progress.emit(0)
        self.signaller.status.emit("fill existing Groups")
        self.fill_existing_groups(ifc_file)
        if self.is_aborted:
            return

        self.signaller.progress.emit(0)
        self.signaller.status.emit("create Structure")
        self.create_aggregation_structure(ifc_file, self.structure_dict, [], None, True, None)
        if self.is_aborted:
            return

        export_name = os.path.join(self.export_path,self.base_name)
        self.signaller.progress.emit(0)
        self.signaller.status.emit(f"Write File to {export_name}")
        if self.is_aborted:
            return

        time.sleep(0.1)
        ifc_file.write(export_name)

    def get_ifc_el_info(self, entitiy: ifcopenshell.entity_instance) -> tuple[str | None, str | None, str | None]:
        """-> Bauteilklassifikation, idGruppe"""
        psets = element.get_psets(entitiy)
        pset_ae = psets.get(self.main_pset)
        pset_gr = psets.get(self.group_pset)
        if pset_ae is None:
            return None, None, None
        attrib = pset_ae.get(self.main_attribute)
        if attrib is None:
            return None, None, None
        if pset_gr is None:
            return None, None, None
        gruppe = pset_gr.get(self.group_attribute)
        if gruppe is None:
            return None, None, None
        identity = pset_ae.get(self.identity_attribute)
        return attrib, gruppe, identity

    def create_structure_dict(self, ifc_file: ifcopenshell.file) -> None:
        self.object_count = len(ifc_file.by_type("IfcElement"))
        for index,el in enumerate(list(ifc_file.by_type("IfcElement"))):
            if self.is_aborted:
                self.set_abort_status()
                return

            if index %10== 0:
                self.increment_progress(f"Bauwerksstruktur Einlesen",10)

            attrib, gruppe, identity = self.get_ifc_el_info(el)
            self.entity_object_dict[el] = self.bk_dict.get(attrib)
            if attrib is None or gruppe is None:
                continue
            parts = gruppe.lower().split("_")
            focus_dict = self.structure_dict
            for part in parts:
                if part not in focus_dict[GROUP]:
                    focus_dict[GROUP][part] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
                focus_dict = focus_dict[GROUP][part]

            obj: SOMcreator.classes.Object = self.bk_dict.get(attrib)
            abbrev = obj.abbreviation
            if abbrev not in focus_dict[GROUP]:
                focus_dict[GROUP][abbrev] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
            focus_dict[GROUP][abbrev][ELEMENT].append(el)
            self.owner_history = el.OwnerHistory

    def fill_existing_groups(self, ifc_file: ifcopenshell.file) -> None:
        for group in ifc_file.by_type("IfcGroup"):
            if self.is_aborted:
                return
            attrib, gruppe, identity = self.get_ifc_el_info(group)
            if identity is None:
                continue
            parts = identity.lower().split("_")
            focus_dict = self.structure_dict
            skip = False
            for part in parts:
                if part in focus_dict[GROUP] and not skip:
                    focus_dict = focus_dict[GROUP][part]
                else:
                    skip = True
            if skip:
                continue

            focus_dict[IFC_REP] = group

    def create_aggregation_structure(self, ifc_file: ifcopenshell.file, structure: dict, id_gruppe: list[str],
                                     parent_group, is_sammler: bool, obj=None):


        def create_ifc_property(property_name: str, value: str):
            prop = ifc_file.create_entity("IfcPropertySingleValue", property_name, DESCRIPTION,
                                          ifc_file.create_entity("IfcLabel", value), None)
            return prop

        def create_ifc_pset(pset_name, attribute_dict: dict[str, str],
                            relating_entity: ifcopenshell.entity_instance | None = None):
            properties = list()
            for property_name, value in attribute_dict.items():
                properties.append(create_ifc_property(property_name, value))
            pset = ifc_file.create_entity("IfcPropertySet", ifcopenshell.guid.new(), self.owner_history, pset_name,
                                          DESCRIPTION, properties)
            if relating_entity is not None:
                ifc_file.create_entity("IfcRelDefinesByProperties", ifcopenshell.guid.new(), self.owner_history,
                                       f"Elationship {pset_name}", DESCRIPTION, [relating_entity], pset)
            return pset

        def create_ifc_group(group_obj: SOMcreator.Object, group_name: str, identity: list[str],
                             parent: ifcopenshell.entity_instance = None) -> ifcopenshell.entity_instance:
            logging.info(f"create_new_group: {group_name}")
            ifc_group = ifc_file.create_entity("IfcGroup", ifcopenshell.guid.new(), self.owner_history, group_name,
                                               DESCRIPTION)
            ifc_file.create_entity("IfcRelAssignsToGroup", ifcopenshell.guid.new(), self.owner_history, group_obj.name,
                                   DESCRIPTION, [], None, ifc_group)

            attributes = {self.main_attribute: group_obj.ident_value, NAME: group_obj.name,
                          self.identity_attribute: "_".join(identity)}
            create_ifc_pset(self.main_pset, attributes, ifc_group)

            if is_sammler:
                attributes = {self.group_attribute: "_".join(identity[:-1])}
            else:
                attributes = {self.group_attribute: "_".join(identity[:-2])}
            create_ifc_pset(self.group_pset, attributes, ifc_group)

            if parent is not None:
                for relation_ship in parent.IsGroupedBy:
                    relation_ship[4] = list(relation_ship[4]) + [ifc_group]
                    return ifc_group
            return ifc_group

        for abbreviation in structure[GROUP]:
            if self.is_aborted: #on Abort press
                return
            ifc_rep = structure[GROUP][abbreviation][IFC_REP]
            new_id_gruppe = id_gruppe + [abbreviation]
            if is_sammler:
                obj = self.kuerzel_dict.get(abbreviation.upper())
                if obj is None:
                    continue
                name = obj.name
            else:
                name = f"{obj.name}_{abbreviation}"
            if ifc_rep is None:
                group = create_ifc_group(obj, name, new_id_gruppe, parent_group)
                structure[GROUP][abbreviation][IFC_REP] = group
            else:
                group = ifc_rep
            self.create_aggregation_structure(ifc_file, structure[GROUP][abbreviation], new_id_gruppe, group,
                                              not is_sammler, obj)


        if not is_sammler:
            for relation_ship in parent_group.IsGroupedBy:
                relation_ship[4] = list(set(relation_ship[4]).union(set(structure[ELEMENT])))
            return
