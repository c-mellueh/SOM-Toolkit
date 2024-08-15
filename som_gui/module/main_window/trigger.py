from som_gui.core import main_window as core
from som_gui import tool


def connect():
    pass


def on_new_project():
    pass


def close_event():
    return core.close_event(tool.Project, tool.Settings, tool.Popups, tool.MainWindow)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)
