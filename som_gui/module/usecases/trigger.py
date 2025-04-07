from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import usecases as core
from typing import TYPE_CHECKING
from PySide6.QtCore import QModelIndex, Qt, QPoint
import SOMcreator


def connect():
    core.create_main_menu_actions(tool.Usecases, tool.MainWindow)
    pass


def retranslate_ui():
    core.retranslate_ui(tool.Usecases, tool.Util)


def on_new_project():
    pass


def open_window():
    core.open_window(tool.Usecases, tool.Project, tool.Util, tool.Search)


def resize_project_model():
    core.update_project_table_size(tool.Usecases)


def resize_class_model(index=QModelIndex()):
    core.update_class_tree_size(index, tool.Usecases)


def resize_property_model(index=QModelIndex()):
    core.update_property_table_size(tool.Usecases)


def class_selection_changed():
    core.update_class_selection(tool.Usecases)


def search_class():
    core.search_class(tool.Usecases, tool.Search, tool.Project)


def add_usecase():
    core.add_usecase(tool.Usecases, tool.Util)


def add_phase():
    core.add_phase(tool.Usecases, tool.Util)


def remove_usecase(logical_index: int):
    core.remove_usecase(logical_index, tool.Usecases)


def remove_phase(logical_index: int):
    core.remove_phase(logical_index, tool.Usecases)


def rename_filter(orientation: Qt.Orientation, index: QModelIndex):
    core.rename_filter(orientation, index, tool.Usecases)

def header_context_requested(pos: QPoint, orientation: Qt.Orientation):
    core.create_context_menu(pos, orientation, tool.Usecases, tool.Project)
