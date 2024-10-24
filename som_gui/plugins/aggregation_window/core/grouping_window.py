from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING, Type

import ifcopenshell
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialogButtonBox

from som_gui import tool
from som_gui.plugins.aggregation_window.module.grouping_window.constants import GROUP_FOLDER
from .. import tool as aw_tool
from ..module.grouping_window.constants import GROUP_ATTRIBUTE, GROUP_PSET, IFC_MOD

if TYPE_CHECKING:
    from som_gui.tool.ifc_importer import IfcImportRunner


def create_main_menu_actions(grouping_window: Type[aw_tool.GroupingWindow], main_window: Type[tool.MainWindow]):
    from som_gui.plugins.aggregation_window.module.grouping_window import trigger
    action = main_window.add_action("menuModels", "create_groups", trigger.open_window)
    grouping_window.set_action("create_groups", action)


def retranslate_ui(grouping_window: Type[aw_tool.GroupingWindow], util: Type[tool.Util]):
    logging.info("Retranslate UI:{}".format(QCoreApplication.translate("Aggregation", "Create IfcGroups")))
    action = grouping_window.get_action("create_groups")
    action.setText(QCoreApplication.translate("Aggregation", "Create IfcGroups"))
    window = grouping_window.get()

    if window is None:
        return
    title = QCoreApplication.translate("Aggregation", "Create Groups")
    window.setWindowTitle(util.get_window_title(title))
    window.ui.widget_export.name = QCoreApplication.translate("Aggregation", "Export Path")
    window.ui.widget_import.name = QCoreApplication.translate("Aggregation", "IFC Path")

    group_pset, group_attribute = util.get_attribute(window.ui.widget_group_attribute)
    pset_placeholder = QCoreApplication.translate("Aggregation", "Grouping PropertySet")
    attribute_placeholder = QCoreApplication.translate("Aggregation", "Grouping PropertySet")
    util.fill_main_attribute(window.ui.widget_group_attribute, group_pset, group_attribute, pset_placeholder,
                             attribute_placeholder)


def open_window(grouping_window: Type[aw_tool.GroupingWindow], util: Type[tool.Util]):
    window = grouping_window.create_window()
    util.fill_file_selector(window.ui.widget_export, "_export", "", GROUP_FOLDER, request_folder=True,
                            request_save=True)
    util.fill_file_selector(window.ui.widget_import, "_ifc", "IFC Files (*.ifc *.IFC);;", "grouping_import")
    group_attribute = tool.Appdata.get_string_setting(IFC_MOD, GROUP_ATTRIBUTE)
    group_pset = tool.Appdata.get_string_setting(IFC_MOD, GROUP_PSET)
    util.fill_main_attribute(window.ui.widget_group_attribute, group_pset, group_attribute, "_pset", "_")
    grouping_window.connect_buttons()
    grouping_window.set_progressbar_visible(False)
    retranslate_ui(grouping_window, util)
    window.show()


def run_clicked(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter],
                util: Type[tool.Util]):
    widget = grouping_window.get()
    group_pset_name, group_attribute_name = util.get_attribute(widget.ui.widget_group_attribute)
    main_pset_name, main_attribute_name = util.get_attribute(widget.ui.widget_ident_attribute)
    export_path = util.get_path_from_fileselector(widget.ui.widget_export)[0]
    ifc_paths = util.get_path_from_fileselector(widget.ui.widget_import)

    ifc_inputs_are_valid = ifc_importer.check_inputs(ifc_paths, main_pset_name, main_attribute_name)
    export_path_is_valid = grouping_window.check_export_path(export_path)
    if not ifc_inputs_are_valid or not export_path_is_valid:
        return

    grouping_window.set_buttons(QDialogButtonBox.StandardButton.Abort)
    grouping_window.reset_abort()
    grouping_window.set_main_attribute(main_pset_name, main_attribute_name)
    grouping_window.set_grouping_attribute(group_pset_name, group_attribute_name)
    grouping_window.set_export_path(export_path)

    grouping_window.set_is_running(True)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    grouping_window.set_progressbar_visible(False)
    grouping_window.set_progress(0)

    for path in ifc_paths:
        status = QCoreApplication.translate("Aggregation", "Import '{}'".format(os.path.basename(path)))
        grouping_window.set_status(status)
        runner = grouping_window.create_import_runner(path)
        grouping_window.connect_ifc_import_runner(runner)
        pool.start(runner)


def abort_clicked(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    logging.info(f"Cancel clicked")
    if ifc_importer.import_is_running():
        for runner in grouping_window.get_properties().ifc_import_runners:
            runner.is_aborted = True
    if grouping_window.is_running():
        ifc_import_widget = grouping_window.get_ifc_importer()
        grouping_window.abort()
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        grouping_window.set_is_running(False)


def cancel_clicked(grouping_window: Type[aw_tool.GroupingWindow], ):
    grouping_window.close_window()


def ifc_import_started(runner: IfcImportRunner, grouping_window: Type[aw_tool.GroupingWindow]):
    grouping_window.set_progressbar_visible(True)
    status = QCoreApplication.translate("Aggregation", "Import '{}'".format(os.path.basename(runner.path)))
    grouping_window.set_status(status)
    grouping_window.set_progress(0)


def ifc_import_finished(runner: IfcImportRunner, grouping_window: Type[aw_tool.GroupingWindow]):
    """
    creates and runs Modelcheck Runnable
    """

    grouping_window.destroy_import_runner(runner)
    status = QCoreApplication.translate("Aggregation", "Import Done!")
    grouping_window.set_status(status)

    grouping_window.set_ifc_name(os.path.basename(runner.path))
    grouping_runner = grouping_window.create_grouping_runner(runner.ifc)

    grouping_window.connect_grouping_runner(grouping_runner)
    grouping_window.set_current_runner(grouping_runner)
    grouping_window.get_grouping_threadpool().start(grouping_runner)


def create_groups_in_file(ifc_file: ifcopenshell.file, grouping_window: Type[aw_tool.GroupingWindow],
                          project: Type[tool.Project]):
    grouping_window.set_progress(0)
    start_time = time.time()
    status = QCoreApplication.translate("Aggregation", "create Structure Dict")
    grouping_window.set_status(status)
    ifc_elements = list(ifc_file.by_type("IfcElement"))
    structure_dict = grouping_window.create_structure_dict(ifc_elements, project.get())
    logging.info(f"creating Structure dict took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    status = QCoreApplication.translate("Aggregation", "fill existing Groups")
    grouping_window.set_status(status)
    grouping_window.fill_existing_groups(ifc_file, structure_dict)

    logging.info(f"fill existing Groups took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    grouping_window.set_progress(0)
    status = QCoreApplication.translate("Aggregation", "create Structure")
    grouping_window.set_status(status)
    owner_history = grouping_window.get_first_owner_history(ifc_file)
    grouping_window.create_new_grouping_strictures(ifc_file, structure_dict, owner_history,
                                                   project.get().get_objects(filter=False))
    logging.info(f"Create Structure took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    export_name = os.path.join(grouping_window.get_export_path(), grouping_window.get_ifc_name())
    grouping_window.set_progress(0)
    status = QCoreApplication.translate("Aggregation", "Write file to '{}'").format(export_name)
    grouping_window.set_status(status)
    if grouping_window.is_aborted():
        return

    time.sleep(0.1)
    ifc_file.write(str(export_name))
    grouping_window.set_progress(100)
    logging.info(f"Export took {time.time() - start_time} seconds")


def grouping_finished(grouping_window: Type[aw_tool.GroupingWindow], popups: Type[tool.Popups]):
    grouping_window.set_progressbar_visible(False)
    if grouping_window.is_aborted():
        grouping_window.reset_buttons()
        grouping_window.set_is_running(False)
        return

    time.sleep(0.2)
    if not grouping_window.get_grouping_threadpool().activeThreadCount() > 0:
        grouping_window.reset_buttons()
        status = QCoreApplication.translate("Aggregation", "Grouping Done!")
        popups.create_info_popup(status)
        grouping_window.set_is_running(False)
    else:
        logging.info(f"Grouping of File Done! Next file!")
