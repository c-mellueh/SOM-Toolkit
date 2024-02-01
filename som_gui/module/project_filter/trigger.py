from som_gui import tool
from som_gui.core import project_filter as core


def connect():
    tool.MainWindow.add_action("Datei/Projektfilter",
                               lambda: core.open_project_filter_window(tool.ProjectFilter, tool.Project))


def on_new_project():
    pass
