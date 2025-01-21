from __future__ import annotations

import logging
import os
from typing import Iterator, TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialogButtonBox

import SOMcreator
import som_gui
import som_gui.plugins.aggregation_window.core.tool
from ..module.grouping_window import trigger
from ..module.grouping_window import ui as grouping_ui
from ..module.grouping_window.constants import GROUP_ATTRIBUTE, GROUP_FOLDER, GROUP_PSET, IFC_MOD

if TYPE_CHECKING:
    from ..module.grouping_window.prop import GroupingWindowProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.util.ui import Progressbar
    from ..module.grouping_window import ui
from som_gui import tool
from SOMcreator.util.group_ifc import GROUP, get_ifc_el_info, ELEMENT, IFC_REP, fill_existing_groups, \
    create_aggregation_structure


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class GroupingRunner(QRunnable):
    def __init__(self, ifc_file: ifcopenshell.file,file_path:str,progress_bar:Progressbar):
        super().__init__()
        self.file = ifc_file
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.file_path = file_path

    def run(self):
        trigger.start_grouping(self)
        self.signaller.finished.emit()


class GroupingWindow(som_gui.plugins.aggregation_window.core.tool.GroupingWindow):
    @classmethod
    def get_properties(cls) -> GroupingWindowProperties:
        return som_gui.GroupingWindowProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def get(cls) -> grouping_ui.GroupingWindow:
        return cls.get_properties().grouping_window

    @classmethod
    def create_window(cls):
        widget = grouping_ui.GroupingWindow()
        cls.get_properties().grouping_window = widget
        return widget

    @classmethod
    def autofill_export_path(cls):
        export_path = tool.Appdata.get_path(GROUP_FOLDER)
        if export_path:
            cls.get_properties().export_line_edit.setText(export_path)

    @classmethod
    def connect_buttons(cls, ):
        cls.get().ui.buttonBox.clicked.connect(trigger.button_clicked)

    @classmethod
    def read_inputs(cls):
        group_pset_name, group_attribute_name = tool.Util.get_attribute(cls.get().ui.widget_group_attribute)
        main_pset_name, main_attribute_name = tool.Util.get_attribute(cls.get().ui.widget_ident_attribute)
        export_path = tool.Util.get_path_from_fileselector(cls.get().ui.widget_export)
        ifc_paths = tool.Util.get_path_from_fileselector(cls.get().ui.widget_import)
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
    def set_status(cls, progress_bar:Progressbar,text: str):
        progress_bar.ui.label.setText(text)

    @classmethod
    def set_progress(cls, progress_bar:Progressbar,value: int):
        logging.debug(f"SetProgress:{progress_bar} -> {value}")
        progress_bar.ui.progressBar.setValue(value)

    @classmethod
    def create_import_runner(cls, ifc_import_path: str,progress_bar:Progressbar):
        runner = tool.IfcImporter.create_runner(progress_bar, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def connect_ifc_import_runner(cls, runner: IfcImportRunner):
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def destroy_import_runner(cls, runner: IfcImportRunner):
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def set_ifc_name(cls, value):
        cls.get_properties().ifc_name = value

    @classmethod
    def get_ifc_name(cls):
        return cls.get_properties().ifc_name

    @classmethod
    def create_grouping_runner(cls, ifc_file,file_path:str,progress_bar:Progressbar) -> GroupingRunner:
        return GroupingRunner(ifc_file,file_path,progress_bar)

    @classmethod
    def connect_grouping_runner(cls, runner: GroupingRunner):
        trigger.connect_grouping_runner(runner)

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
    def create_structure_dict(cls, runner:GroupingRunner,ifc_elements: list[ifcopenshell.entity_instance],
                              project: SOMcreator.Project) -> dict:
        """Iterate over all Entities, build the targeted Datastructure"""

        targeted_group_structure = {GROUP: {}, ELEMENT: {}, IFC_REP: None}
        bk_dict = {obj.ident_value: obj for obj in project.get_objects(filter=True)}
        entity_count = len(ifc_elements)

        percentages = list()
        for index, el in enumerate(ifc_elements):
            percentage = int(index / entity_count * 100)
            if percentage % 5 == 0 and percentage not in percentages:
                runner.signaller.progress.emit(percentage)
                percentages.append(percentage)

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
        cls.get().hide()
        cls.get().close()

    @classmethod
    def set_buttons(cls, buttons):
        cls.get().ui.buttonBox.setStandardButtons(buttons)


    @classmethod
    def reset_buttons(cls):
        cls.set_buttons(QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel)

    @classmethod
    def add_progress_bar(cls,progress_bar:Progressbar):
        cls.get().ui.layout_progress_bar.addWidget(progress_bar)

    @classmethod
    def clear_progress_bars(cls,widget:ui.GroupingWindow):
        layout = widget.ui.layout_progress_bar
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    @classmethod
    def set_progress_bars_visible(cls,state:bool):
        cls.get().ui.scrollArea.setVisible(state)

    @classmethod
    def is_grouping_running(cls):
        return cls.get_grouping_threadpool().activeThreadCount() > 0