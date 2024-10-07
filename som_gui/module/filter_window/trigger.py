from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import filter_window as core
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING


def connect():
    tool.MainWindow.add_action("Filter",
                               lambda: core.open_window(tool.FilterWindow, tool.Project))


def pt_remove_usecase_clicked(index):
    core.remove_usecase_clicked(index, tool.FilterWindow, tool.Project, tool.Util)


def pt_add_usecase_clicked():
    core.add_usecase_clicked(tool.FilterWindow, tool.Project, tool.Util)


def pt_horizontal_context_requested(pos):
    core.pt_context_menu(pos, Qt.Orientation.Horizontal, tool.FilterWindow, tool.Project)
    pass


def pt_vertical_context_requested(pos):
    core.pt_context_menu(pos, Qt.Orientation.Vertical, tool.FilterWindow, tool.Project)
    pass




def on_new_project():
    pass


def tree_mouse_move_event(index):
    core.tree_mouse_move_event(index, tool.FilterWindow)


def tree_mouse_release_event(index):
    core.tree_mouse_release_event(index, tool.FilterWindow)

def update_object_tree():
    core.update_object_tree(tool.FilterWindow)


def object_tree_clicked(selected, deselected):
    core.object_tree_selection_changed(selected, tool.FilterWindow)
    pass


def update_pset_tree():
    core.update_pset_tree(tool.FilterWindow)
