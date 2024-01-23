import som_gui.core.use_case as core
from som_gui.tool.use_case import UseCase
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/Anwendungsfälle", lambda: core.open_use_case_window(tool.UseCase, tool.Project))

def on_new_project():
    core.on_startup(UseCase)
