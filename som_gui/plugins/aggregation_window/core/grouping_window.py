from __future__ import annotations
from typing import TYPE_CHECKING, Type
from som_gui import tool
import ifcopenshell
from .. import tool as aw_tool
import logging
import time
import os
from PySide6.QtCore import QRunnable


def open_window(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    window = grouping_window.create_window()
    grouping_window.create_grouping_line_edits()
    ifc_import_widget = ifc_importer.create_importer()
    grouping_window.add_ifc_importer_to_window(ifc_import_widget)
    export_button, export_line_edit = ifc_importer.create_export_line(ifc_import_widget)
    grouping_window.add_export_line(export_button, export_line_edit)
    grouping_window.autofill_export_path()
    grouping_window.autofill_grouping_attributes()
    grouping_window.connect_buttons(grouping_window.get_buttons())
    window.show()


def export_selection_clicked(grouping_window: Type[aw_tool.GroupingWindow], settings: Type[tool.Appdata]):
    old_path = settings.get_group_folder()
    new_path = grouping_window.open_export_dialog(old_path)
    if not new_path:
        return
    settings.set_group_folder(new_path)
    grouping_window.set_export_line_text(new_path)


def run_clicked(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    ifc_import_widget = grouping_window.get_ifc_importer()

    (group_pset_name, group_attribute_name, main_pset_name,
     main_attribute_name, ifc_paths, export_path) = grouping_window.read_inputs()
    ifc_inputs_are_valid = ifc_importer.check_inputs(ifc_paths, main_pset_name, main_attribute_name)
    export_path_is_valid = grouping_window.check_export_path(export_path)
    if not ifc_inputs_are_valid or not export_path_is_valid:
        return
    ifc_importer.set_run_button_enabled(ifc_import_widget, False)
    ifc_importer.set_close_button_text(ifc_import_widget, "Abbrechen")
    grouping_window.reset_abort()
    grouping_window.set_main_attribute(main_pset_name, main_attribute_name)
    grouping_window.set_grouping_attribute(group_pset_name, group_attribute_name)
    grouping_window.set_export_path(export_path)

    grouping_window.set_is_running(True)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    ifc_importer.set_progressbar_visible(ifc_import_widget, True)
    ifc_importer.set_progress(ifc_import_widget, 0)

    for path in ifc_paths:
        grouping_window.set_status(f"Import '{os.path.basename(path)}'")
        runner = grouping_window.create_import_runner(path)
        grouping_window.connect_ifc_import_runner(runner)
        pool.start(runner)


def cancel_clicked(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    logging.info(f"Cancel clicked")
    if grouping_window.is_running():
        ifc_import_widget = grouping_window.get_ifc_importer()
        grouping_window.abort()
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        grouping_window.set_is_running(False)
    else:
        grouping_window.close_window()


def ifc_import_started(runner: QRunnable, grouping_window: Type[aw_tool.GroupingWindow],
                       ifc_importer: Type[tool.IfcImporter]):
    widget = grouping_window.get_ifc_importer()
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def ifc_import_finished(runner: QRunnable, grouping_window: Type[aw_tool.GroupingWindow]):
    """
    creates and runs Modelcheck Runnable
    """

    grouping_window.destroy_import_runner(runner)
    grouping_window.set_status(f"Import Abgeschlossen")

    grouping_window.set_ifc_name(os.path.basename(runner.path))
    grouping_runner = grouping_window.create_grouping_runner(runner.ifc)

    grouping_window.connect_grouping_runner(grouping_runner)
    grouping_window.set_current_runner(grouping_runner)
    grouping_window.get_grouping_threadpool().start(grouping_runner)


def create_groups_in_file(ifc_file: ifcopenshell.file, grouping_window: Type[aw_tool.GroupingWindow],
                          project: Type[tool.Project]):
    grouping_window.set_progress(0)
    grouping_window.set_status("create Structure Dict")
    structure_dict = grouping_window.create_structure_dict(ifc_file, project.get())
    if grouping_window.is_aborted():
        return

    grouping_window.set_progress(15)
    grouping_window.set_status("fill existing Groups")
    grouping_window.fill_existing_groups(ifc_file, structure_dict)

    if grouping_window.is_aborted():
        return

    grouping_window.set_progress(50)
    grouping_window.set_status("create Structure")
    owner_history = grouping_window.get_first_owner_history(ifc_file)
    grouping_window.create_new_grouping_strictures(ifc_file, structure_dict, owner_history,
                                                   project.get().get_all_objects())

    if grouping_window.is_aborted():
        return

    export_name = os.path.join(grouping_window.get_export_path(), grouping_window.get_ifc_name())
    grouping_window.set_progress(75)
    grouping_window.set_status(f"Write File to {export_name}")
    if grouping_window.is_aborted():
        return

    time.sleep(0.1)
    ifc_file.write(str(export_name))
    grouping_window.set_progress(100)


def grouping_finished(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter],
                      popups: Type[tool.Popups]):
    ifc_import_widget = grouping_window.get_ifc_importer()
    if grouping_window.is_aborted():
        ifc_importer.set_progressbar_visible(ifc_import_widget, False)
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        grouping_window.set_is_running(False)
        return

    time.sleep(0.2)
    if not grouping_window.get_grouping_threadpool().activeThreadCount() > 0:
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        popups.create_info_popup(f"Gruppierung abgeschlossen")
        grouping_window.set_is_running(False)
    else:
        logging.info(f"Gruppierung von Datei abgeschlossen, nächste Datei ist dran.")
