from som_gui import tool
from som_gui.core import main_window as core

TOOGLE_CONSOLE_ACTION = "toggle_console"

def connect():
    core.create_main_menu_actions(tool.MainWindow)


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(tool.MainWindow)


def toggle_console():
    core.toggle_console_clicked(tool.MainWindow)


def close_event(event):
    return core.close_event(event,tool.MainWindow, tool.Popups)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)
