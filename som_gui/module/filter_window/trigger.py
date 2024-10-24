from __future__ import annotations

from PySide6.QtCore import Qt

from som_gui import tool
from som_gui.core import filter_window as core
from . import constants, ui


def connect():
    core.create_main_menu_actions(tool.FilterWindow, tool.MainWindow)
    core.add_compare_widget(tool.FilterCompare, tool.AttributeCompare, tool.CompareWindow)
    tool.Settings.add_page_to_toolbox(ui.SettingsWidget, constants.SETTINGS_PAGE_NAME,
                                      lambda: core.settings_accepted(tool.FilterWindow, tool.Project, tool.Popups))


def open_window():
    core.open_window(tool.FilterWindow, tool.Project, tool.Util, tool.Search)


def retranslate_ui():
    core.retranslate_ui(tool.FilterWindow)


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


# Settings

def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.FilterWindow, tool.Project)


def settings_combobox_changed():
    core.settings_combobox_changed(tool.FilterWindow, tool.Project, tool.Util)


def filter_tab_object_tree_selection_changed(widget):
    core.filter_tab_object_tree_selection_changed(widget, tool.AttributeCompare, tool.FilterCompare)
