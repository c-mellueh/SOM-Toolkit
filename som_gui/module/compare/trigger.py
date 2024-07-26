from som_gui.core import compare as core
from som_gui import tool


def connect():
    tool.MainWindow.add_action("Compare", lambda: core.test(tool.Compare, tool.Project))


def on_new_project():
    pass


def object_tree_selection_changed():
    core.object_tree_selection_changed(tool.Compare)
