from som_gui.core import console as core
from som_gui import tool
def connect():
    tool.MainWindow.add_action("Datei/Console", lambda: core.show(tool.Console))


def on_new_project():
    pass


def close_console():
    core.close(tool.Console)
