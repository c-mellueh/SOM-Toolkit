from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtGui import QStandardItem

def open_window(modelcheck: Type[tool.Modelcheck], ifc_importer: Type[tool.IfcImporter]):
    window = modelcheck.create_window()
    check_box_widget = modelcheck.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()

    modelcheck.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck.connect_window(window)
    window.setWindowTitle("Modellprüfung")
    window.show()


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
    modelcheck.set_object_check_state(obj, item.checkState())


def object_selection_changed(item: QStandardItem, modelcheck: Type[tool.Modelcheck]):
    obj = item.data(CLASS_REFERENCE)
    modelcheck.set_selected_object(obj)
