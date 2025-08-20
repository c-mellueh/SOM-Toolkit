from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData, Qt, QModelIndex
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


def update_class_trees(class_tree: Type[tool.ClassTree], project: Type[tool.Project]):
    for tree in class_tree.get_trees():
        class_tree.reset_tree(tree)


def connect_signals(
    class_tree: Type[tool.ClassTree], class_tool: Type[tool.Class]
) -> None:
    class_tree.connect_trigger()
    class_tree.signaller.request_class_deletion.connect(class_tool.delete_class)


def connect_new_class_tree(
    tree: ui.ClassView, class_tree: Type[tool.ClassTree], class_tool: Type[tool.Class]
):
    class_tool.signaller.class_deleted.connect(
        lambda c: class_tree.remove_row_by_class(tree, c)
    )
    class_tool.signaller.class_created.connect(
        lambda c: class_tree.insert_row_by_class(tree, c)
    )


def retranslate_ui(class_tree: Type[tool.ClassTree]) -> None:
    return


def create_mime_data(
    indexes: QModelIndex, mime_data: QMimeData, class_tree: Type[tool.ClassTree]
):
    classes = {class_tree.get_class_from_index(i) for i in indexes}
    class_tree.write_classes_to_mimedata(classes, mime_data)
    return mime_data


def search_class(
    tree: ui.ClassView,
    search_tool: Type[Search],
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    """Open Search Window and select Class afterwards"""
    som_class = search_tool.search_class(list(project.get().get_classes(filter=True)))
    if som_class is None:
        return
    class_tree.expand_to_class(tree, som_class)


def create_group(
    tree: ui.ClassView,
    class_tree: Type[tool.ClassTree],
    class_tool: Type[tool.Class],
    project: Type[tool.Project],
):

    # TODO: aktualisieren

    d = {
        "name": QCoreApplication.translate("Class", "NewGroup"),
        "is_group": True,
        "ifc_mappings": ["IfcGroup"],
    }
    is_allowed = class_tool.check_class_creation_input(d)
    if not is_allowed:
        return
    som_class = class_tool.create_class(d, None, None)
    som_class.project = project.get()
    selected_classes = set(class_tree.get_selected_classes(tree))
    class_tree.group_classes(som_class, selected_classes)


def create_context_menu(
    tree: ui.ClassView, pos: QPoint, class_tree: Type[tool.ClassTree]
):
    menu = class_tree.create_context_menu(tree)
    menu_pos = tree.viewport().mapToGlobal(pos)
    menu.exec(menu_pos)
