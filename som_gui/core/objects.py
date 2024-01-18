from __future__ import annotations
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
import logging

import som_gui
from typing import Type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool import Objects, Project


def refresh_object_tree(object_tool: Type[Objects], project_tool: Type[Project]):
    load_objects(object_tool, project_tool)


def load_objects(object_tool: Type[Objects], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter=True)
    object_tree: QTreeWidget = object_tool.get_object_tree()
    object_tool.fill_object_tree(set(root_objects), object_tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, object_tool: Type[Objects]):
    object_tool.update_check_state(item)
