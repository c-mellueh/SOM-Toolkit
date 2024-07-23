from som_gui.core import main_window as core
from som_gui import tool


def connect():
    core.add_label_to_statusbar(tool.MainWindow)


def on_new_project():
    pass


def close_event():
    return core.close_event(tool.Project, tool.Settings, tool.Popups)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)
