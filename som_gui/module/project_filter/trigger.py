from som_gui import tool
from som_gui.core import project_filter as core


def connect():
    tool.MainWindow.add_action("Datei/Projektfilter",
                               lambda: core.open_project_filter_window(tool.ProjectFilter, tool.Project))


def refresh_table():
    core.refresh_table(tool.ProjectFilter, tool.Project)
def on_new_project():
    pass


def close_event():
    core.close_dialog(tool.ProjectFilter)


def uc_context_menu_requested(pos):
    core.context_menu(pos, 0, tool.ProjectFilter)


def pp_context_menu_requested(pos):
    core.context_menu(pos, 1, tool.ProjectFilter)
