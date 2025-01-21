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
    from ..tool.grouping_window import GroupingRunner


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
    grouping_window.set_progress_bars_visible(False)
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

    grouping_window.clear_progress_bars(widget)
    grouping_window.set_buttons(QDialogButtonBox.StandardButton.Abort)
    grouping_window.reset_abort()
    grouping_window.set_main_attribute(main_pset_name, main_attribute_name)
    grouping_window.set_grouping_attribute(group_pset_name, group_attribute_name)
    grouping_window.set_export_path(export_path)

    grouping_window.set_is_running(True)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(1)
    grouping_window.set_progress_bars_visible(True)
    logging.debug(f"Group {len(ifc_paths)} files")
    for path in ifc_paths:
        logging.debug(f"Create Progressbar for '{path}'")
        progress_bar = util.create_progressbar()
        grouping_window.add_progress_bar(progress_bar)
        grouping_window.set_progress(progress_bar,0)
        status = QCoreApplication.translate("Aggregation", "Import '{}'".format(os.path.basename(path)))
        grouping_window.set_status(progress_bar,status)
        runner = grouping_window.create_import_runner(path,progress_bar)
        grouping_window.connect_ifc_import_runner(runner)
        pool.start(runner)


def abort_clicked(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    logging.info(f"Cancel clicked")
    if ifc_importer.import_is_running():
        for runner in grouping_window.get_properties().ifc_import_runners:
            runner.is_aborted = True
    if grouping_window.is_running():
        grouping_window.abort()
        grouping_window.set_is_running(False)


def close_window(grouping_window: Type[aw_tool.GroupingWindow], ):
    grouping_window.close_window()


def ifc_import_started(runner: IfcImportRunner):
    logging.debug(f"Start Importing '{runner.path}'")
    status = QCoreApplication.translate("Aggregation", "Import '{}'".format(os.path.basename(runner.path)))
    runner.signaller.status.emit(status)
    runner.signaller.progress.emit(0)


def ifc_import_finished(runner: IfcImportRunner, grouping_window: Type[aw_tool.GroupingWindow]):
    """
    creates and runs Modelcheck Runnable
    """

    logging.debug(f"Ifc Importing finished of'{runner.path}'")

    grouping_window.destroy_import_runner(runner)
    status = QCoreApplication.translate("Aggregation", "Import Done!")
    runner.signaller.status.emit(status)

    grouping_window.set_ifc_name(os.path.basename(runner.path))
    logging.debug(f"Create grouping Runner of'{runner.path}'")

    grouping_runner = grouping_window.create_grouping_runner(runner.ifc,runner.path,runner.progress_bar)

    grouping_window.connect_grouping_runner(grouping_runner)
    grouping_window.get_grouping_threadpool().start(grouping_runner)


def create_groups_in_file(runner:GroupingRunner, grouping_window: Type[aw_tool.GroupingWindow],
                          project: Type[tool.Project]):
    logging.debug(f"Start grouping  of'{runner.file_path}'")

    ifc_file = runner.file
    runner.signaller.progress.emit(0)
    start_time = time.time()
    status = QCoreApplication.translate("Aggregation", "create Structure Dict")
    runner.signaller.status.emit(status)
    ifc_elements = list(ifc_file.by_type("IfcElement"))
    structure_dict = grouping_window.create_structure_dict(runner,ifc_elements, project.get())
    logging.info(f"creating Structure dict took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    status = QCoreApplication.translate("Aggregation", "fill existing Groups")
    runner.signaller.status.emit(status)
    grouping_window.fill_existing_groups(ifc_file, structure_dict)

    logging.info(f"fill existing Groups took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    runner.signaller.progress.emit(0)
    status = QCoreApplication.translate("Aggregation", "create Structure")

    runner.signaller.status.emit(status)
    owner_history = grouping_window.get_first_owner_history(ifc_file)
    grouping_window.create_new_grouping_strictures(ifc_file, structure_dict, owner_history,
                                                   project.get().get_objects(filter=False))
    logging.info(f"Create Structure took {time.time() - start_time} seconds")

    if grouping_window.is_aborted():
        return

    start_time = time.time()
    export_name = os.path.join(grouping_window.get_export_path(), grouping_window.get_ifc_name())
    runner.signaller.progress.emit(0)
    status = QCoreApplication.translate("Aggregation", "Write file to '{}'").format(export_name)
    runner.signaller.status.emit(status)
    if grouping_window.is_aborted():
        return

    time.sleep(0.1)
    logging.debug(f"Write file '{export_name}'")
    ifc_file.write(str(export_name))
    runner.signaller.progress.emit(100)
    logging.info(f"Export took {time.time() - start_time} seconds")



def grouping_finished(runner:GroupingRunner,grouping_window: Type[aw_tool.GroupingWindow],ifc_importer:Type[tool.IfcImporter], popups: Type[tool.Popups]):
    if grouping_window.is_aborted():
        grouping_window.reset_buttons()
        grouping_window.set_is_running(False)
        return
    logging.debug(f"Grouping of '{runner.file_path}' finished")


    status = QCoreApplication.translate("Aggregation", "Grouping of file '{}' Done!").format(runner.file_path)
    runner.signaller.status.emit(status)
    runner.signaller.progress.emit(100)
    time.sleep(0.2)
    if grouping_window.is_grouping_running() or ifc_importer.import_is_running():
        logging.info(f"Grouping of File Done! Next file!")
    else:
        grouping_window.reset_buttons()
        status = QCoreApplication.translate("Aggregation", "Grouping Done!")
        popups.create_info_popup(status)
        grouping_window.set_is_running(False)
        grouping_window.set_progress_bars_visible(False)


