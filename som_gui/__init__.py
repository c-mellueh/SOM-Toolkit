from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import core
from som_gui import tool
from thefuzz import fuzz
from SOMcreator.external_software.IDS import main
from SOMcreator.external_software.bim_collab_zoom import modelcheck
from SOMcreator.external_software.desite import modelcheck
if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow

__version__ = "2.12.1"

import importlib

modules = {
    "object_filter":           None,
    "project_filter":          None,
    "project":                 None,
    "object":              None,
    "search":                  None,
    "property_set":            None,
    "attribute":               None,
    "main_window":             None,
    "attribute_table":         None,
    "property_set_window":     None,
    "predefined_property_set": None,
    "modelcheck_window":   None,
    "modelcheck_results":  None,
    "modelcheck_external": None,
    "modelcheck":          None,
    "ifc_importer":        None,
    "util":                None,
}

aggregation_window_modules = {
    "window": None,
    "view":   None,
    "node":       None,
    "connection": None,
}

for name in modules.keys():
    modules[name] = importlib.import_module(f"som_gui.module.{name}")

for name in aggregation_window_modules.keys():
    aggregation_window_modules[name] = importlib.import_module(f"som_gui.aggregation_window.module.{name}")

modules.update(aggregation_window_modules)

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
