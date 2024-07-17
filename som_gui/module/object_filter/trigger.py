import som_gui.core.object_filter as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Datei/Objektfilter", lambda: core.open_use_case_window(tool.ObjectFilter))

def on_new_project():
    core.on_startup(tool.ObjectFilter)
