from som_gui.core import main_window as core
from som_gui import tool


def connect():
    core.add_menu_entries(tool.MainWindow)
    pass


def on_new_project():
    pass


def new_file_clicked():
    core.open_new_file(tool.Project, tool.Popups)
