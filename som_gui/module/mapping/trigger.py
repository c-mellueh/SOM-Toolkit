from som_gui import tool
from som_gui.core import mapping as core


def connect():
    tool.MainWindow.add_action("MAPPINGS",
                               lambda: core.open_window(tool.Mapping))


def on_new_project():
    pass


def export_revit_ifc_mapping():
    core.export_revit_ifc_mapping(tool.Mapping)


def export_revit_shared_parameters():
    core.export_revit_shared_parameters(tool.Mapping)


def update_object_tree():
    core.update_object_tree(tool.Mapping, tool.Project)


def update_pset_tree():
    core.update_pset_tree(tool.Mapping)
