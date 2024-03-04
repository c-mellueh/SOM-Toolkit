from __future__ import annotations
from typing import TYPE_CHECKING
from thefuzz import fuzz

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow, Ui_MainWindow

__version__ = "2.10.3"

import importlib

modules = {
    "object_filter":           None,
    "project_filter":          None,
    "project":                 None,
    "objects":                 None,
    "search":                  None,
    "property_set":            None,
    "attribute":               None,
    "main_window":             None,
    "attribute_table":         None,
    "property_set_window":     None,
    "predefined_property_set": None,
    "modelcheck":   None,
    "ifc_importer": None,
}


class MainUi:
    ui: Ui_MainWindow = None
    window: MainWindow = None


for name in modules.keys():
    modules[name] = importlib.import_module(f"som_gui.module.{name}")


def register():
    modules["project"].register()
    for n, mod in sorted(modules.items()):
        if n != "project":
            mod.register()


def load_ui_triggers():
    modules["project"].load_ui_triggers()
    for n, mod in sorted(modules.items()):
        if n != "project":
            mod.load_ui_triggers()


def on_new_project():
    for n, mod in sorted(modules.items()):
        if n != "project":
            mod.on_new_project()
