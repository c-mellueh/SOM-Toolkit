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
    core.connect_signals(tool.ClassTree,tool.Class)
    pass

def connect_new_class_tree(tree:ui.ClassView):
    core.connect_new_class_tree(tree,tool.ClassTree,tool.Class)

def search_class(tree: ui.ClassView):
    core.search_class(tree, tool.Search, tool.ClassTree, tool.Project)


def on_new_project():
    core.update_class_trees(tool.ClassTree,tool.Project)


def retranslate_ui():
    core.retranslate_ui(tool.ClassTree)


def create_mime_data(items: list[QTreeWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.ClassTree)


def group_selection(tree: ui.ClassView):
    core.create_group(tree, tool.ClassTree,tool.Class, tool.Project)

def create_context_menu(tree,pos):
    core.create_context_menu(tree,pos,tool.ClassTree)