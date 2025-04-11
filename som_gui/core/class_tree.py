from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData,Qt,QModelIndex
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTreeView

import SOMcreator
from som_gui import tool
import som_gui.module.class_tree.constants as constants
import copy as cp

if TYPE_CHECKING:
    from som_gui.tool import Project, Search, PropertySet, MainWindow
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint
from som_gui.module.class_tree import ui

import uuid
def connect_signals(class_tree: Type[tool.ClassTree],class_tool:Type[tool.Class]) -> None:
    class_tree.connect_trigger()
    class_tree.signaller.request_class_deletion.connect(class_tool.delete_class)
    

def retranslate_ui(class_tree: Type[tool.ClassTree]) -> None:
    return

def create_mime_data(
    items: QTreeWidgetItem, mime_data: QMimeData, class_tree: Type[tool.ClassTree]
):
    classes = {class_tree.get_class_from_index(i) for i in items}
    class_tree.write_classes_to_mimedata(classes, mime_data)
    return mime_data


def search_class(
    tree: ui.ClassTreeWidget,
    search_tool: Type[Search],
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    """Open Search Window and select Class afterwards"""
    som_class = search_tool.search_class(list(project.get().get_classes(filter=True)))
    class_tree.expand_to_class(tree, som_class)


def create_group(
    tree: ui.ClassTreeWidget,
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    d = {
        "name": QCoreApplication.translate("Class", "NewGroup"),
        "is_group": True,
        "ifc_mappings": ["IfcGroup"],
    }
    is_allowed = class_tree.check_class_creation_input(d)
    if not is_allowed:
        return
    som_class = class_tree.create_class(d, None, None)
    som_class.project = project.get()
    selected_classes = set(class_tree.get_selected_classes(tree))
    class_tree.group_classes(som_class, selected_classes)


def create_context_menu(
    tree: ui.ClassTreeWidget, pos: QPoint, class_tree: Type[tool.ClassTree]
):
    menu = class_tree.create_context_menu(tree)
    menu_pos = tree.viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_class_tree(
    tree: ui.ClassTreeWidget,
    class_tree: Type[tool.ClassTree],
    project_tool: Type[Project],
):
    logging.debug(f"refresh ClassTree {tree}")




def resize_tree(index:QModelIndex,tree:ui.ClassView,class_tree:Type[tool.ClassTree]):
    """
    gets Called if Filters get Added or Removed.
    :return:
    """
    model = tree.model()
    if model is None:
        return
    model.update_data()
    old_row_count = model.row_count_dict.get(index) or 0
    old_column_count = model.old_column_count
    new_row_count = model.get_row_count(index)
    new_column_count = len(model.columns)
    model.row_count_dict[index] = new_row_count
    model.old_column_count = new_column_count
    logging.info(
        f"ClassModel Update Size rowCount: {old_row_count} -> {new_row_count} columnCount:{old_column_count} -> {new_column_count} {index}"
    )
    if old_row_count == new_row_count and old_column_count == new_column_count:
        return

    # Remove Rows (Phases)
    if old_row_count > new_row_count:
        print(f"Remove Row {new_row_count}  | {old_row_count-1}")
        model.beginRemoveRows(index, new_row_count, old_row_count - 1)
        model.endRemoveRows()

    # Insert Rows (Phases)
    if old_row_count < new_row_count:
        print(f"INsert Rows { old_row_count} | {new_row_count - 1}")
        model.beginInsertRows(index, old_row_count, new_row_count - 1)
        model.endInsertRows()

    # Remove Colums (UseCases)
    if old_column_count > new_column_count:
        print(f"Remove Rows { new_column_count} | {old_column_count - 1}")

        model.beginRemoveColumns(index, new_column_count, old_column_count - 1)
        model.endRemoveColumns()

    # Insert Colums (UseCases)
    if old_column_count < new_column_count:
        print(f"INsert Columns { old_column_count} | {new_column_count - 1}")

        model.beginInsertColumns(index, old_column_count, new_column_count - 1)
        model.endInsertColumns()
    #tree.update_requested.emit()
    