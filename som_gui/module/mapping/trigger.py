from som_gui import tool
from som_gui.core import mapping as core


def connect():
    core.create_main_menu_actions(tool.Mapping, tool.MainWindow)


def open_window():
    core.open_window(tool.Mapping)


def on_new_project():
    pass


def retranslate_ui():
    core.retranslate_ui(tool.Mapping)


def export_revit_ifc_mapping():
    core.export_revit_ifc_mapping(tool.Mapping, tool.Project, tool.Popups)


def export_revit_shared_parameters():
    core.export_revit_shared_parameters(tool.Mapping, tool.Project, tool.Popups)


def update_object_tree():
    core.update_object_tree(tool.Mapping, tool.Project)


def update_pset_tree():
    core.update_pset_tree(tool.Mapping)


def tree_item_changed(item):
    core.tree_item_changed(item, tool.Mapping, tool.Util)
