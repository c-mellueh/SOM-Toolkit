from som_gui.core import logging as core
from som_gui import tool
from . import ui

def connect():
    core.create_logger(tool.Logging, tool.Util, tool.MainWindow)
    tool.Settings.add_page_to_toolbox(ui.SettingsWidget, "General", "Logging",
                                      lambda: core.settings_accepted(tool.Logging))

def on_new_project():
    pass


def settings_widget_created(widget: ui.SettingsWidget):
    core.settings_widget_created(widget, tool.Logging)
    pass
