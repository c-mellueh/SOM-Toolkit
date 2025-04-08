from __future__ import annotations

from PySide6.QtCore import Qt

from som_gui import tool
from som_gui.core import filter_window as core
from . import constants, ui


def connect():
    core.add_compare_widget(
        tool.FilterCompare, tool.PropertyCompare, tool.CompareWindow
    )
    tool.Settings.add_page_to_toolbox(
        ui.SettingsWidget,
        constants.SETTINGS_PAGE_NAME,
        lambda: core.settings_accepted(tool.FilterWindow, tool.Project, tool.Popups),
    )

def retranslate_ui():
    core.retranslate_ui(tool.FilterWindow, tool.Util)

def on_new_project():
    pass
# Settings


def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.FilterWindow, tool.Project)


def settings_combobox_changed():
    core.settings_combobox_changed(tool.FilterWindow, tool.Project, tool.Util)


def filter_tab_class_tree_selection_changed(widget):
    core.filter_tab_class_tree_selection_changed(
        widget, tool.PropertyCompare, tool.FilterCompare
    )
