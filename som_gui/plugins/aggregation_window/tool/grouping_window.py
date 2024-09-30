from __future__ import annotations
import som_gui.plugins.aggregation_window.core.tool
import som_gui
import SOMcreator
import ifcopenshell
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import QRunnable, Signal, QObject, QThreadPool
from typing import TYPE_CHECKING, Iterator
from ..module.grouping_window import ui as grouping_ui
from ..module.grouping_window import trigger
import os
import logging
from ..module.grouping_window.constants import GROUP_FOLDER, GROUP_PSET, IFC_MOD, GROUP_ATTRIBUTE
if TYPE_CHECKING:
    from ..module.grouping_window.prop import GroupingWindowProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget
from som_gui import tool
from SOMcreator.ifc_modification.grouping import GROUP, get_ifc_el_info, ELEMENT, IFC_REP, fill_existing_groups, \
    create_aggregation_structure


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class GroupingRunner(QRunnable):
    def __init__(self, ifc_file: ifcopenshell.file):
        super().__init__()
        self.file = ifc_file
        self.signaller = Signaller()

    def run(self):
        trigger.start_grouping(self.file)
        self.signaller.finished.emit()


class GroupingWindow(som_gui.plugins.aggregation_window.core.tool.GroupingWindow):
    @classmethod
    def get_properties(cls) -> GroupingWindowProperties:
        return som_gui.GroupingWindowProperties

    @classmethod
    def get(cls) -> grouping_ui.GroupingWindow:
        return cls.get_properties().grouping_window

    @classmethod
    def create_window(cls):
        widget = grouping_ui.GroupingWindow()
        cls.get_properties().grouping_window = widget
        return widget

    @classmethod
    def create_grouping_line_edits(cls):
        layout = QHBoxLayout()
        pset_le = QLineEdit()
        pset_le.setPlaceholderText(pset_le.tr(f"Gruppen PropertySet"))
        attribute_le = QLineEdit()
        attribute_le.setPlaceholderText(pset_le.tr(f"Gruppen Attribut"))

        cls.get_properties().grouping_pset_line_edit = pset_le
        cls.get_properties().grouping_attribute_line_edit = attribute_le
        layout.addWidget(pset_le)
        layout.addWidget(attribute_le)
        cls.get().layout().addLayout(layout)

        return layout

    @classmethod
    def autofill_export_path(cls):
        export_path = tool.Appdata.get_path(GROUP_FOLDER)
        if export_path:
            cls.get_properties().export_line_edit.setText(export_path)

    @classmethod
    def add_ifc_importer_to_window(cls, ifc_importer: IfcImportWidget):
        cls.get_properties().ifc_importer = ifc_importer
        cls.get_properties().ifc_button = ifc_importer.widget.button_ifc
        cls.get_properties().run_button = ifc_importer.widget.button_run
        cls.get_properties().abort_button = ifc_importer.widget.button_close
        cls.get_properties().status_label = ifc_importer.widget.label_status
        cls.get().layout().addWidget(ifc_importer)

    @classmethod
    def add_export_line(cls, export_button, export_line_edit):
        cls.get_properties().export_button = export_button
        cls.get_properties().export_line_edit = export_line_edit

    @classmethod
    def autofill_grouping_attributes(cls):
        group_attribute = tool.Appdata.get_string_setting(IFC_MOD, GROUP_ATTRIBUTE)
        group_pset = tool.Appdata.get_string_setting(IFC_MOD, GROUP_PSET)
        if group_attribute:
            cls.get_properties().grouping_attribute_line_edit.setText(group_attribute)
        if group_pset:
            cls.get_properties().grouping_pset_line_edit.setText(group_pset)

    @classmethod
    def get_buttons(cls) -> tuple[QPushButton, QPushButton, QPushButton, QPushButton]:
        ifc = cls.get_properties().ifc_button
        export = cls.get_properties().export_button
        run = cls.get_properties().run_button
        abort = cls.get_properties().abort_button
        return ifc, export, run, abort

    @classmethod
    def connect_buttons(cls, buttons):
        trigger.connect_buttons(*buttons)

    @classmethod
    def open_export_dialog(cls, base_path: os.PathLike | str):
        path = QFileDialog.getExistingDirectory(cls.get(), "Export", base_path)
        return path

    @classmethod
    def set_export_line_text(cls, text: str):
        cls.get_properties().export_line_edit.setText(text)

    @classmethod
    def read_inputs(cls):
        group_pset_name = cls.get_properties().grouping_pset_line_edit.text()
        group_attribute_name = cls.get_properties().grouping_attribute_line_edit.text()
        export_path = cls.get_properties().export_line_edit.text()

        widget = cls.get_properties().ifc_importer
        ifc_paths = tool.IfcImporter.get_ifc_paths(widget)
        main_pset_name = tool.IfcImporter.get_main_pset(widget)
        main_attribute_name = tool.IfcImporter.get_main_attribute(widget)

        return group_pset_name, group_attribute_name, main_pset_name, main_attribute_name, ifc_paths, export_path

    @classmethod
    def check_export_path(cls, export_path: str):
        export_folder_path = os.path.dirname(export_path)
        if not os.path.isdir(export_folder_path):
            tool.Popups.create_folder_dne_warning(export_folder_path)
            return False
        return True



    @classmethod
    def reset_abort(cls) -> None:
        cls.get_properties().abort = False

    @classmethod
    def is_aborted(cls) -> bool:
        return cls.get_properties().abort

    @classmethod
    def abort(cls):
        cls.get_properties().abort = True

    @classmethod
    def set_main_attribute(cls, pset_name, attribute_name):
        cls.get_properties().main_attribute = pset_name, attribute_name

    @classmethod
    def set_grouping_attribute(cls, pset_name, attribute_name):
        cls.get_properties().grouping_attribute = pset_name, attribute_name
        tool.Appdata.set_setting(IFC_MOD, GROUP_PSET, pset_name)
        tool.Appdata.set_setting(IFC_MOD, GROUP_ATTRIBUTE, attribute_name)

    @classmethod
    def set_export_path(cls, path):
        cls.get_properties().export_path = path
        tool.Appdata.set_path(GROUP_FOLDER, path)

    @classmethod
    def get_export_path(cls):
        return cls.get_properties().export_path

    @classmethod
    def get_ifc_importer(cls) -> IfcImportWidget:
        return cls.get_properties().ifc_importer

    @classmethod
    def set_status(cls, text: str):
        cls.get_properties().status_label.setText(text)

    @classmethod
    def set_progress(cls, value: int):
        cls.get_ifc_importer().widget.progress_bar.setValue(value)

    @classmethod
    def create_import_runner(cls, ifc_import_path: str):
        status_label = cls.get_properties().status_label
        runner = tool.IfcImporter.create_runner(status_label, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def connect_ifc_import_runner(cls, runner: QRunnable):
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def destroy_import_runner(cls, runner: QRunnable):
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def set_ifc_name(cls, value):
        cls.get_properties().ifc_name = value

    @classmethod
    def get_ifc_name(cls):
        return cls.get_properties().ifc_name

    @classmethod
    def create_grouping_runner(cls, ifc_file) -> GroupingRunner:
        return GroupingRunner(ifc_file)

    @classmethod
    def connect_grouping_runner(cls, runner: GroupingRunner):
        trigger.connect_grouping_runner(runner)

    @classmethod
    def set_current_runner(cls, runner: QRunnable):
        cls.get_properties().runner = runner

    @classmethod
    def get_grouping_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def is_running(cls):
        return cls.get_properties().is_running

    @classmethod
    def set_is_running(cls, value: bool):
        cls.get_properties().is_running = value

    @classmethod
    def get_attribute_bundle(cls):
        main_pset_name, main_attribute_name = cls.get_properties().main_attribute
        group_pset_name, group_attribute_name = cls.get_properties().grouping_attribute
        identity_attribute = cls.get_properties().identity_attribute
        return (main_pset_name, main_attribute_name, group_pset_name,
                group_attribute_name, main_pset_name, identity_attribute)

    # Grouping Functions
    @classmethod
    def create_structure_dict(cls, ifc_file: ifcopenshell.file, project: SOMcreator.Project) -> dict:
        """Iterate over all Entities, build the targeted Datastructure"""

        targeted_group_structure = {GROUP: {}, ELEMENT: {}, IFC_REP: None}
        bk_dict = {obj.ident_value: obj for obj in project.get_objects(filter=True)}

        for index, el in enumerate(list(ifc_file.by_type("IfcElement"))):
            if cls.is_aborted():
                return dict()
            attrib, gruppe, identity = get_ifc_el_info(el, cls.get_attribute_bundle())
            if attrib is None or gruppe is None:
                continue

            parts = gruppe.upper().split("_")
            focus_dict = targeted_group_structure
            for part in parts:
                if part not in focus_dict[GROUP]:
                    focus_dict[GROUP][part] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
                focus_dict = focus_dict[GROUP][part]

            obj: SOMcreator.Object = bk_dict.get(attrib)
            if obj is None:
                logging.warning(
                    f"Die Entität '{el.GlobalId}' besitzt einen unbekannten identifier ({attrib}) und kann dadurch nicht ausgewertet werden!")
                continue
            abbrev = obj.abbreviation
            if abbrev.upper() not in focus_dict[GROUP]:
                focus_dict[GROUP][abbrev] = {GROUP: {}, ELEMENT: list(), IFC_REP: None}
            focus_dict[GROUP][abbrev][ELEMENT].append(el)
        return targeted_group_structure

    @classmethod
    def fill_existing_groups(cls, ifc_file: ifcopenshell.file, structure_dict):
        fill_existing_groups(ifc_file, structure_dict, cls.get_attribute_bundle())

    @classmethod
    def get_first_owner_history(cls, ifc_file):
        possible_owner_histories = list(ifc_file.by_type("IfcOwnerHistory"))
        if possible_owner_histories:
            owner_history = possible_owner_histories[0]
        else:
            owner_history = ifc_file.create_entity("IfcOwnerHistory")
            logging.warning(f"IfcOwnerHistory Existiert nicht. -> neue IfcOwnerHistory wird erzeugt.")
        return owner_history

    @classmethod
    def create_new_grouping_strictures(cls, ifc_file, structure_dict, owner_history,
                                       objects_list: Iterator[SOMcreator.Object]):
        attribute_bundle = cls.get_attribute_bundle()
        kuerzel_dict = {obj.abbreviation.upper(): obj for obj in objects_list}
        create_empty = cls.get_properties().create_empty_attribues
        create_aggregation_structure(ifc_file, structure_dict, [], None, True, attribute_bundle, owner_history,
                                     kuerzel_dict, create_empty, None)

    @classmethod
    def close_window(cls):
        cls.get().close()
