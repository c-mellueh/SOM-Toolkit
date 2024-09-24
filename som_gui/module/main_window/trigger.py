from som_gui.core import main_window as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Bearbeiten/Toggle Console", lambda: core.toggle_console_clicked(tool.MainWindow))


def on_new_project():
    pass


def close_event():
    return core.close_event(tool.Project, tool.Appdata, tool.Popups, tool.MainWindow)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)
