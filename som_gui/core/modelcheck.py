from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type
import os
import ifcopenshell
import SOMcreator
from PySide6.QtCore import Qt

import som_gui.module.modelcheck.trigger
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtGui import QStandardItem
    from PySide6.QtCore import QItemSelectionModel, QModelIndex
    from som_gui.module.ifc_importer.ui import IfcImportWidget, IfcImportRunner


def open_window(modelcheck: Type[tool.Modelcheck], ifc_importer: Type[tool.IfcImporter]):
    window = modelcheck.create_window()
    check_box_widget = modelcheck.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()
    som_gui.module.modelcheck.trigger.connect_ifc_import_widget(ifc_import_widget)
    modelcheck.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck.connect_window(window)
    window.setWindowTitle("Modellprüfung")
    modelcheck.show_pset_tree_title(False)
    window.show()


def run_clicked(widget: IfcImportWidget, modelcheck: Type[tool.Modelcheck], ifc_importer: Type[tool.IfcImporter]):
    paths = ifc_importer.get_ifc_paths(widget)
    widget.pool = ifc_importer.create_thread_pool()
    widget.pool.setMaxThreadCount(5)
    for path in paths:
        runner = ifc_importer.create_runner(widget.widget.label_status, path)
        on_start = lambda: import_started(widget, runner, modelcheck, ifc_importer)
        on_finish = lambda: import_finished(widget, runner, modelcheck, ifc_importer)
        runner.signaller.started.connect(on_start)
        runner.signaller.finished.connect(on_finish)
        widget.pool.start(runner)


def import_started(widget: IfcImportWidget, runner: IfcImportRunner, modelcheck: Type[tool.Modelcheck],
                   ifc_importer: Type[tool.IfcImporter]):
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def import_finished(widget: IfcImportWidget, runner: IfcImportRunner, modelcheck: Type[tool.Modelcheck],
                    ifc_importer: Type[tool.IfcImporter]):
    ifc_importer.set_status(widget, f"Import Abgeschlossen")
    ifc_file = runner.ifc
    run_modelcheck_on_ifc(ifc_file, modelcheck)


def run_modelcheck_on_ifc(file: ifcopenshell.file, modelcheck: Type[tool.Modelcheck]):
    pass


def export_selection_clicked(widget: IfcImportWidget, modelcheck: Type[tool.Modelcheck], settings: Type[tool.Settings]):
    old_path = settings.get_issue_path()
    new_path = modelcheck.open_export_dialog(widget, old_path, "Excel File (*.xlsx);;")
    if not new_path:
        return
    settings.set_issue_path(new_path)
    widget.widget.line_edit_export.setText(new_path)


def paint_object_tree(modelcheck: Type[tool.Modelcheck], project: Type[tool.Project]):
    logging.debug(f"Repaint Modelcheck Object Tree")
    root_objects = set(project.get_root_objects(True))
    tree = modelcheck.get_object_tree()
    invisible_root_entity = tree.model().invisibleRootItem()
    modelcheck.fill_object_tree(root_objects, invisible_root_entity, tree.model(), tree)


def object_check_changed(item: QStandardItem, modelcheck: Type[tool.Modelcheck]):
    obj = item.data(CLASS_REFERENCE)
    if item.column() != 0:
        return
    modelcheck.set_item_check_state(obj, item.checkState())
    paint_pset_tree(modelcheck)


def object_selection_changed(selection_model: QItemSelectionModel, modelcheck: Type[tool.Modelcheck]):
    index: QModelIndex = selection_model.selectedIndexes()[0]
    obj: SOMcreator.Object = index.data(CLASS_REFERENCE)
    modelcheck.set_selected_object(obj)
    paint_pset_tree(modelcheck)
    if obj.ident_value:
        text = f"{obj.name} [{obj.ident_value}]"
    else:
        text = obj.name
    modelcheck.set_pset_tree_title(text)
    modelcheck.show_pset_tree_title(True)


def paint_pset_tree(modelcheck: Type[tool.Modelcheck]):
    logging.debug(f"Repaint Modelcheck Pset Tree")
    obj = modelcheck.get_selected_object()
    if obj is None:
        return
    cs = modelcheck.get_item_check_state(obj)
    enabled = True if cs == Qt.CheckState.Checked else False
    modelcheck.fill_pset_tree(set(obj.property_sets), enabled, modelcheck.get_pset_tree())
