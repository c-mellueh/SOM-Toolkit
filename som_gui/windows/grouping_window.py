from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import SOMcreator
import ifcopenshell
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QFileDialog, QCheckBox
from SOMcreator import classes
from SOMcreator.ifc_modification import grouping

from som_gui.widgets.ifc_widget import IfcWidget, IfcRunner

if TYPE_CHECKING:
    from ..main_window import MainWindow

from .. import settings

FILE_SPLIT = "; "
ELEMENT = "Element"
GROUP = "SubGroup"
IFC_REP = "IfcRep"
DESCRIPTION = "automatisch erzeugt"
NAME = "bauteilName"


class GroupingWindow(IfcWidget):
    def __init__(self, main_window: MainWindow):
        super(GroupingWindow, self).__init__(main_window)
        self.setWindowTitle("Gruppen erzeugen")
        self.empty_attributes_checkbox = QCheckBox()
        self.create_group_line_input()
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

    def create_group_line_input(self):
        self.line_edit_group_pset = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_pset, 1, 0, 1, 1)
        self.line_edit_group_attrib = QLineEdit()
        self.widget.layout_attribute.addWidget(self.line_edit_group_attrib, 1, 1, 1, 1)
        self.widget.layout_attribute.addWidget(self.empty_attributes_checkbox, 2, 0, 1, 2)
        self.empty_attributes_checkbox.setText("Leere Attribute hinzufügen")
        self.line_edit_group_pset.setPlaceholderText("Gruppen PropertySet")
        self.line_edit_group_attrib.setPlaceholderText("Gruppen Attribut")
        self.line_edit_group_attrib.setText(self.main_window.project.aggregation_attribute)
        self.line_edit_group_pset.setText(self.main_window.project.aggregation_pset)
        self.line_edit_group_attrib.textEdited.connect(self.update_grouping_values)
        self.line_edit_group_pset.textEdited.connect(self.update_grouping_values)
        self.line_edit_group_pset.setText(settings.get_group_pset())
        self.line_edit_group_attrib.setText(settings.get_group_attribute())
        state = Qt.CheckState.Checked if settings.get_group_create_empty_attributes() else Qt.CheckState.Unchecked
        self.empty_attributes_checkbox.setCheckState(state)

    def start_task(self) -> tuple:
        proj, ifc, pset, attribute, export_path = super(GroupingWindow, self).start_task()
        group_pset = self.line_edit_group_pset.text()
        group_attribute = self.line_edit_group_attrib.text()
        settings.set_group_pset(group_pset)
        settings.set_group_attribute(group_attribute)
        empty_attributes = self.empty_attributes_checkbox.isChecked()
        settings.set_group_create_empty_attributes(empty_attributes)
        self.runner = Grouping(ifc, proj, pset, attribute, export_path, group_pset, group_attribute, "identitaet",
                               empty_attributes)
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
                 export_folder: str, group_pset: str, group_attrib: str, identity_attrib: str, empty_attributes: bool):
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
        self.create_empty_attributes = empty_attributes

    def run(self) -> None:
        super(Grouping, self).run()

    def run_file_function(self, file_path) -> ifcopenshell.file:
        ifc_file = super(Grouping, self).run_file_function(file_path)
        self.create_group_for_file(ifc_file)
        return ifc_file

    def create_group_for_file(self, ifc_file: ifcopenshell.file):
        self.signaller.progress.emit(0)
        self.signaller.status.emit("create Structure Dict")
        attribute_bundle = (self.main_pset, self.main_attribute, self.group_pset, self.group_attribute, self.main_pset,
                            self.identity_attribute)
        structure_dict = grouping.create_structure_dict(ifc_file, self.project, attribute_bundle)
        if self.is_aborted:
            return

        self.signaller.progress.emit(15)
        self.signaller.status.emit("fill existing Groups")
        grouping.fill_existing_groups(ifc_file, structure_dict, attribute_bundle)
        if self.is_aborted:
            return

        self.signaller.progress.emit(50)
        self.signaller.status.emit("create Structure")
        owner_history = list(ifc_file.by_type("IfcOwnerHistory"))[0]
        kuerzel_dict = {obj.abbreviation.upper(): obj for obj in self.project.objects}
        grouping.create_aggregation_structure(ifc_file, structure_dict, [], None, True, attribute_bundle, owner_history,
                                              kuerzel_dict, self.create_empty_attributes, None)
        if self.is_aborted:
            return

        export_name = os.path.join(self.export_path, self.base_name)
        self.signaller.progress.emit(75)
        self.signaller.status.emit(f"Write File to {export_name}")
        if self.is_aborted:
            return

        time.sleep(0.1)
        ifc_file.write(export_name)
        self.signaller.progress.emit(100)
