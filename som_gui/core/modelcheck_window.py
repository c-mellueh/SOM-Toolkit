from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Type
import os
import ifcopenshell
import SOMcreator
from PySide6.QtCore import Qt

import som_gui.module.modelcheck_window.trigger
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtGui import QStandardItem
    from PySide6.QtCore import QItemSelectionModel, QModelIndex, QRunnable
    from som_gui.module.ifc_importer.ui import IfcImportWidget, IfcImportRunner
    from som_gui.core import modelcheck as mc_core


def open_window(modelcheck_window: Type[tool.ModelcheckWindow], ifc_importer: Type[tool.IfcImporter]):
    window = modelcheck_window.create_window()
    check_box_widget = modelcheck_window.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()
    som_gui.module.modelcheck_window.trigger.connect_ifc_import_widget(ifc_import_widget)
    modelcheck_window.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck_window.connect_window(window)
    window.setWindowTitle("Modellprüfung")
    modelcheck_window.show_pset_tree_title(False)
    window.show()


def run_clicked(widget: IfcImportWidget, modelcheck_window: Type[tool.ModelcheckWindow],
                modelcheck: Type[tool.Modelcheck],
                ifc_importer: Type[tool.IfcImporter], project: Type[tool.Project],
                modelcheck_core: mc_core):
    paths = ifc_importer.get_ifc_paths(widget)
    widget.pool = ifc_importer.create_thread_pool()
    widget.pool.setMaxThreadCount(3)
    db_path = modelcheck.create_new_sql_database()
    modelcheck.build_ident_dict(set(project.get().objects))
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_progress(widget, 0)

    for path in paths:
        ifc_importer.set_status(widget, f"Import '{os.path.basename(path)}'")
        time.sleep(1)

        runner = ifc_importer.create_runner(widget.widget.label_status, path)
        on_start = lambda: import_started(widget, runner, modelcheck_window, ifc_importer)
        on_finish = lambda: import_finished(widget, runner, modelcheck_window, modelcheck, ifc_importer,
                                            modelcheck_core)
        runner.signaller.started.connect(on_start)
        runner.signaller.finished.connect(on_finish)
        widget.pool.start(runner)


def import_started(widget: IfcImportWidget, runner: IfcImportRunner, modelcheck_window: Type[tool.ModelcheckWindow],
                   ifc_importer: Type[tool.IfcImporter]):
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def import_finished(widget: IfcImportWidget, runner: IfcImportRunner, modelcheck_window: Type[tool.ModelcheckWindow],
                    modelcheck: Type[tool.Modelcheck],
                    ifc_importer: Type[tool.IfcImporter], modelcheck_core: mc_core):
    ifc_importer.set_status(widget, f"Import Abgeschlossen")
    ifc_file = runner.ifc
    modelcheck.set_ifc_name(os.path.basename(runner.path))
    modelcheck_runner = modelcheck.create_modelcheck_runner(
        lambda: modelcheck_core.check_file(ifc_file, widget, modelcheck, modelcheck_window))
    modelcheck_runner.signaller.finished.connect(
        lambda: modelcheck_finished(modelcheck_runner, modelcheck, modelcheck_window))
    modelcheck.set_current_runner(modelcheck_runner)
    modelcheck_window.get_modelcheck_threadpool().start(modelcheck_runner)


def modelcheck_finished(runner: QRunnable, modelcheck: Type[tool.Modelcheck],
                        modelcheck_window: Type[tool.ModelcheckWindow]):
    thread_pool = modelcheck_window.get_modelcheck_threadpool()
    if thread_pool.activeThreadCount() < 1:
        pass
    else:
        print(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")


def export_selection_clicked(widget: IfcImportWidget, modelcheck_window: Type[tool.ModelcheckWindow],
                             settings: Type[tool.Settings]):
    old_path = settings.get_issue_path()
    new_path = modelcheck_window.open_export_dialog(widget, old_path, "Excel File (*.xlsx);;")
    if not new_path:
        return
    settings.set_issue_path(new_path)
    widget.widget.line_edit_export.setText(new_path)


def paint_object_tree(modelcheck_window: Type[tool.ModelcheckWindow], project: Type[tool.Project]):
    logging.debug(f"Repaint Modelcheck Object Tree")
    root_objects = set(project.get_root_objects(True))
    tree = modelcheck_window.get_object_tree()
    invisible_root_entity = tree.model().invisibleRootItem()
    modelcheck_window.fill_object_tree(root_objects, invisible_root_entity, tree.model(), tree)


def object_check_changed(item: QStandardItem, modelcheck_window: Type[tool.ModelcheckWindow]):
    obj = item.data(CLASS_REFERENCE)
    if item.column() != 0:
        return
    modelcheck_window.set_item_check_state(obj, item.checkState())
    paint_pset_tree(modelcheck_window)


def object_selection_changed(selection_model: QItemSelectionModel, modelcheck_window: Type[tool.ModelcheckWindow]):
    index: QModelIndex = selection_model.selectedIndexes()[0]
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
