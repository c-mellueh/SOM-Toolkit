from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import use_case as core
from typing import TYPE_CHECKING
from PySide6.QtCore import QModelIndex, Qt, QPoint
from PySide6.QtGui import QMouseEvent
import SOMcreator


def connect():
    core.create_main_menu_actions(tool.UseCase, tool.MainWindow)
    pass


def retranslate_ui():
    core.retranslate_ui(tool.UseCase, tool.Util)


def on_new_project():
    pass


def open_window():
    core.open_window(tool.UseCase, tool.Project, tool.Util)


def resize_project_model():
    core.update_project_table_size(tool.UseCase)


def resize_class_model(index=QModelIndex()):
    core.update_class_tree_size(index, tool.UseCase)


def resize_property_model(index=QModelIndex()):
    core.update_property_table_size(tool.UseCase)


def class_selection_changed():
    core.update_class_selection(tool.UseCase)


def search_class():
    core.search_class(tool.UseCase, tool.Search, tool.Project)


def add_use_case():
    core.add_use_case(tool.UseCase, tool.Util)


def add_phase():
    core.add_phase(tool.UseCase, tool.Util)


def remove_use_case(logical_index: int):
    core.remove_use_case(logical_index, tool.UseCase)


def remove_phase(logical_index: int):
    core.remove_phase(logical_index, tool.UseCase)


def rename_filter(orientation: Qt.Orientation, index: QModelIndex):
    core.rename_filter(orientation, index, tool.UseCase)


def header_context_requested(pos: QPoint, orientation: Qt.Orientation):
    core.create_context_menu(pos, orientation, tool.UseCase, tool.Project)


def mouse_move_event(event: QMouseEvent, source):
    core.mouse_move_event(event, source, tool.UseCase, tool.Util)


def mouse_release_event(
    event: QMouseEvent,
    source,
):
    core.mouse_release_event(source, tool.UseCase)
