from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData
from PySide6.QtGui import QDropEvent

import SOMcreator
from som_gui import tool
from som_gui.core.property_set import repaint_pset_table as refresh_property_set_table
import som_gui.module.class_tree.constants as constants
import copy as cp

if TYPE_CHECKING:
    from som_gui.tool import Project, Search, PropertySet, MainWindow
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint
    from som_gui.module.class_tree import ui

import uuid


def init_tree(
    tree: ui.ClassTreeWidget,
    class_tree: Type[tool.ClassTree],
) -> None:
    class_tree.add_tree(tree)
    tree.setColumnCount(0)
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Class"),
        0,
        lambda c: getattr(c, "name"),
    )
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Identifier"),
        1,
        lambda o: (
            getattr(o, "ident_value")
            if isinstance(o.identifier_property, SOMcreator.SOMProperty)
            else ""
        ),
    )
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Optional"),
        2,
        lambda o: o.is_optional(ignore_hirarchy=True),
        class_tree.set_class_optional_by_tree_item_state,
    )

    tree.customContextMenuRequested.connect(
        lambda p: create_context_menu(tree,p, tool.ClassTree)
    )

def retranslate_ui(class_tree: Type[tool.ClassTree]) -> None:
    return


def create_mime_data(
    items: QTreeWidgetItem, mime_data: QMimeData, class_tree: Type[tool.ClassTree]
):
    classes = {class_tree.get_class_from_item(i) for i in items}
    class_tree.write_classes_to_mimedata(classes, mime_data)
    return mime_data


def search_class(tree:ui.ClassTreeWidget,
    search_tool: Type[Search],
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    """Open Search Window and select Class afterwards"""
    som_class = search_tool.search_class(list(project.get().get_classes(filter=True)))
    class_tree.select_class(tree, som_class)





def create_group(tree:ui.ClassTreeWidget,class_tree: Type[tool.ClassTree], project: Type[tool.Project]):
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


def create_context_menu(tree:ui.ClassTreeWidget,pos: QPoint, class_tree: Type[tool.ClassTree]):
    menu = class_tree.create_context_menu(tree)
    menu_pos = tree.viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_class_tree(tree:ui.ClassTreeWidget,class_tree: Type[tool.ClassTree], project_tool: Type[Project]):

    root_classes = project_tool.get_root_classes(filter_classes=True)
    if class_tree.get_properties().first_paint:
        tree.clear()
        class_tree.set_first_paint(tree,False)
        retranslate_ui(class_tree)
    class_tree.fill_class_tree(set(root_classes), tree.invisibleRootItem())

def drop_event(
    event: QDropEvent,
    target: ui.ClassTreeWidget,
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    pos = event.pos()
    source_table = event.source()
    if source_table == target:
        dropped_on_item = class_tree.get_item_from_pos(target,pos)
        class_tree.handle_class_move(target,dropped_on_item)
        return
    classes = class_tree.get_classes_from_mimedata(event.mimeData())
    if not classes:
        return
    for som_class in classes:
        project.get().add_item(som_class)


