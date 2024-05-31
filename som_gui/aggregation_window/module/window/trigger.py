from som_gui import tool as mw_tool
from som_gui.aggregation_window.core import window as core
from som_gui.aggregation_window import tool


def connect():
    mw_tool.MainWindow.add_action("Test/Bauwerksstruktur",
                                  lambda: core.create_window(tool.Window, tool.View))


def on_new_project():
    pass
