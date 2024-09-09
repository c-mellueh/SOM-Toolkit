from som_gui import tool
from som_gui.core import bsdd as core
def connect():
    tool.MainWindow.add_action("Datei/Export/bsDD",
                               lambda: core.open_window(tool.Bsdd))


def on_new_project():
    pass
