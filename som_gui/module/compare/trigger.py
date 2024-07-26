from som_gui.core import compare as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Compare", lambda: core.open_compare_window(tool.Compare, tool.Settings, tool.Project))


def on_new_project():
    pass


def project_button_clicked():
    core.project_button_clicked(tool.Compare, tool.Popups, tool.Settings)


def object_tree_selection_changed():
    core.object_tree_selection_changed(tool.Compare)


def pset_tree_selection_changed():
    core.pset_tree_selection_changed(tool.Compare)
