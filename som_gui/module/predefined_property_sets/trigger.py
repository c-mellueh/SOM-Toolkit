from som_gui.core import predefined_property_set as core
from som_gui import tool


def connect():
    pass


def edit_name(text, index):
    core.rename_pset_by_editor(text, index, tool.PropertySet)


def on_new_project():
    pass


def repaint_window():
    core.repaint_predefined_pset_window(tool.PropertySet)


def accept():
    tool.PropertySet.close_predefined_pset_window()
