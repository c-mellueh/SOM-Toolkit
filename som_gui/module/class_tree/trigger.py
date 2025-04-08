from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.class_.prop import ClassDataDict
    from . import ui
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import QModelIndex
from som_gui import tool
from som_gui.core import class_tree as core
import SOMcreator


def connect():
    core.connect_signals(tool.ClassTree)
    pass


def search_class(tree: ui.ClassTreeWidget):
    core.search_class(tree, tool.Search, tool.ClassTree, tool.Project)


def init_tree(tree: ui.ClassView):
    core.init_tree(tree, tool.ClassTree,tool.Project)


def repaint_event(tree: ui.ClassTreeWidget):
    core.refresh_class_tree(tree, tool.ClassTree, tool.Project)


def drop_event(event, target: ui.ClassTreeWidget):
    core.drop_event(event, target, tool.ClassTree, tool.Project)


def on_new_project():
    return


def retranslate_ui():
    core.retranslate_ui(tool.ClassTree)


def create_mime_data(items: list[QTreeWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.ClassTree)


def group_selection(tree: ui.ClassTreeWidget):
    core.create_group(tree, tool.ClassTree, tool.Project)

def resize_tree(index:QModelIndex,tree:ui.ClassView):
    core.resize_tree(index,tree,tool.ClassTree)