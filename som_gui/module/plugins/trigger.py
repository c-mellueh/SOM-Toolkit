from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import plugins as core
from typing import TYPE_CHECKING
from . import ui

def connect():
    tool.Settings.add_page_to_toolbox(ui.SettingsWidget, "pagePlugins",
                                      lambda: core.settings_accepted(tool.Plugins, tool.Popups))


def on_new_project():
    pass


def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.Plugins)
    pass


def retranslate_ui():
    pass
