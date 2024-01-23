from som_gui.core import main_window as core
from som_gui import tool


def connect():
    core.add_label_to_statusbar(tool.MainWindow)
    core.fill_old_menus(tool.MainWindow)

def on_new_project():
    pass

