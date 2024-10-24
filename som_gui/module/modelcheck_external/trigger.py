from som_gui import tool
from som_gui.core import modelcheck_external as core


def connect():
    core.create_main_menu_actions(tool.ModelcheckExternal, tool.MainWindow)


def open_window():
    core.open_window(tool.ModelcheckExternal, tool.ModelcheckWindow)


def on_new_project():
    pass


def close_window():
    core.close_window(tool.ModelcheckExternal)


def retranslate_ui():
    core.retranslate_ui(tool.ModelcheckExternal, tool.Util)
