from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Type
import os
import SOMcreator
from PySide6.QtCore import Qt, QThread

from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtGui import QStandardItem
    from PySide6.QtCore import QItemSelectionModel, QModelIndex, QRunnable


def open_window(modelcheck_window: Type[tool.ModelcheckWindow], ifc_importer: Type[tool.IfcImporter]):
    if modelcheck_window.is_window_allready_build():
        modelcheck_window.get_window().show()
        return

    window = modelcheck_window.create_window()
    check_box_widget = modelcheck_window.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()
    export_button, export_line_edit = ifc_importer.create_export_line(ifc_import_widget)
    modelcheck_window.get_properties().export_button = export_button
    modelcheck_window.get_properties().export_line_edit = export_line_edit
    modelcheck_window.autofill_export_path()

    modelcheck_window.set_importer_widget(ifc_import_widget)
    modelcheck_window.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck_window.connect_buttons(modelcheck_window.get_buttons())
    modelcheck_window.connect_check_widget(check_box_widget)
    window.show()


def cancel_clicked(modelcheck_window: Type[tool.ModelcheckWindow], modelcheck: Type[tool.Modelcheck]):
    if modelcheck_window.modelcheck_is_running():
        modelcheck.abort()
        modelcheck_window.set_abort_button_text(f"Close")
    else:
        modelcheck_window.close_window()

def run_clicked(modelcheck_window: Type[tool.ModelcheckWindow],
                modelcheck: Type[tool.Modelcheck], modelcheck_results: Type[tool.ModelcheckResults],
                ifc_importer: Type[tool.IfcImporter], project: Type[tool.Project], ):

    ifc_paths, export_path, main_pset, main_attribute = modelcheck_window.read_inputs()
    inputs_are_valid = ifc_importer.check_inputs(ifc_paths, main_pset, main_attribute)
    export_path_is_valid = modelcheck_window.check_export_path(export_path)

    if not inputs_are_valid or not export_path_is_valid:
        return

    modelcheck_window.set_run_button_enabled(False)
    modelcheck_window.set_abort_button_text(f"Abbrechen")
    ifc_import_widget = modelcheck_window.get_ifc_import_widget()
    modelcheck.reset_abort()
    modelcheck.set_main_pset_name(main_pset)
    modelcheck.set_main_attribute_name(main_attribute)
    modelcheck_results.set_export_path(export_path)

    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)

    modelcheck.create_new_sql_database()
    modelcheck.reset_guids()
    modelcheck.build_ident_dict(set(project.get().objects))

    ifc_importer.set_progressbar_visible(ifc_import_widget, True)
    ifc_importer.set_progress(ifc_import_widget, 0)
    for path in ifc_paths:
        modelcheck_window.set_status(f"Import '{os.path.basename(path)}'")
        runner = modelcheck_window.create_import_runner(path)
        modelcheck_window.connect_ifc_import_runner(runner)
        pool.start(runner)


def ifc_import_started(runner: QRunnable, modelcheck_window: Type[tool.ModelcheckWindow],
                       ifc_importer: Type[tool.IfcImporter]):
    widget = modelcheck_window.get_ifc_import_widget()
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def ifc_import_finished(runner: QRunnable, modelcheck_window: Type[tool.ModelcheckWindow],
                        modelcheck: Type[tool.Modelcheck]):
    """
    creates and runs Modelcheck Runnable
    """

    modelcheck_window.destroy_import_runner(runner)
    modelcheck_window.set_status(f"Import Abgeschlossen")

    modelcheck.set_ifc_name(os.path.basename(runner.path))
    modelcheck_runner = modelcheck.create_modelcheck_runner(runner.ifc)

    modelcheck_window.connect_modelcheck_runner(modelcheck_runner)
    modelcheck.set_current_runner(modelcheck_runner)
    modelcheck_window.get_modelcheck_threadpool().start(modelcheck_runner)


def modelcheck_finished(modelcheck_window: Type[tool.ModelcheckWindow], modelcheck: Type[tool.Modelcheck],
                        modelcheck_results: Type[tool.ModelcheckResults], ifc_importer: Type[tool.IfcImporter]):
    if modelcheck.is_aborted():
        ifc_import_widget = modelcheck_window.get_ifc_import_widget()
        ifc_importer.set_progressbar_visible(ifc_import_widget, False)
        modelcheck_window.set_abort_button_text(f"Close")
        modelcheck_window.set_run_button_enabled(True)
        return

    time.sleep(0.2)
    if not modelcheck_window.modelcheck_is_running():
        modelcheck_results.last_modelcheck_finished()
        modelcheck_window.set_abort_button_text(f"Close")
        modelcheck_window.set_run_button_enabled(True)
    else:
        logging.info(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")


def export_selection_clicked(modelcheck_window: Type[tool.ModelcheckWindow],
                             settings: Type[tool.Settings]):
    old_path = settings.get_issue_path()
    new_path = modelcheck_window.open_export_dialog(old_path, "Excel File (*.xlsx);;")
    if not new_path:
        return
    settings.set_issue_path(new_path)
    modelcheck_window.set_export_line_text(new_path)


def paint_object_tree(modelcheck_window: Type[tool.ModelcheckWindow], project: Type[tool.Project]):
    logging.debug(f"Repaint Modelcheck Object Tree")
    root_objects = set(project.get_root_objects(True))
    tree = modelcheck_window.get_object_tree()
    invisible_root_entity = tree.model().invisibleRootItem()
    modelcheck_window.fill_object_tree(root_objects, invisible_root_entity, tree.model(), tree)
    if modelcheck_window.is_initial_paint:
        modelcheck_window.resize_object_tree()

def object_check_changed(item: QStandardItem, modelcheck_window: Type[tool.ModelcheckWindow]):
    obj = item.data(CLASS_REFERENCE)
    if item.column() != 0:
        return

    modelcheck_window.set_item_check_state(obj, item.checkState())
    paint_pset_tree(modelcheck_window)


def object_selection_changed(selection_model: QItemSelectionModel, modelcheck_window: Type[tool.ModelcheckWindow]):
    selected_indexes = selection_model.selectedIndexes()
    if not selected_indexes:
        return
    index: QModelIndex = selected_indexes[0]
    obj: SOMcreator.Object = index.data(CLASS_REFERENCE)
    modelcheck_window.set_selected_object(obj)
    paint_pset_tree(modelcheck_window)
    if obj.ident_value:
        text = f"{obj.name} [{obj.ident_value}]"
    else:
        text = obj.name
    modelcheck_window.set_pset_tree_title(text)
    modelcheck_window.show_pset_tree_title(True)


def paint_pset_tree(modelcheck_window: Type[tool.ModelcheckWindow]):
    logging.debug(f"Repaint Modelcheck Pset Tree")
    obj = modelcheck_window.get_selected_object()
    if obj is None:
        return
    cs = modelcheck_window.get_item_check_state(obj)
    enabled = True if cs == Qt.CheckState.Checked else False
    modelcheck_window.fill_pset_tree(set(obj.property_sets), enabled, modelcheck_window.get_pset_tree())


def object_tree_conect_menu_requested(pos, widget, modelcheck_window: Type[tool.ModelcheckWindow]):
    actions = [
        ["Ausklappen", lambda: modelcheck_window.expand_selection(widget)],
        ["Einklappen", lambda: modelcheck_window.collapse_selection(widget)],
        ["Aktivieren", lambda: modelcheck_window.check_selection(widget)],
        ["Deaktivieren", lambda: modelcheck_window.uncheck_selection(widget)]
    ]

    modelcheck_window.create_context_menu(pos, actions, widget)
