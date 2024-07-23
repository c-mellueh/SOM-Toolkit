from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import core, tool, settings
from thefuzz import fuzz
from SOMcreator.external_software.IDS import main
from SOMcreator.external_software.bim_collab_zoom import modelcheck
from SOMcreator.external_software.desite import modelcheck
if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow

__version__ = "2.12.3"

import importlib

modules = {
    "object_filter":           [None, "object_filter"],
    "project_filter":          [None, "project_filter"],
    "project":                 [None, "project"],
    "object":                  [None, "object"],
    "search":                  [None, "search"],
    "property_set":            [None, "property_set"],
    "attribute":               [None, "attribute"],
    "main_window":             [None, "main_window"],
    "attribute_table":         [None, "attribute_table"],
    "property_set_window":     [None, "property_set_window"],
    "predefined_property_set": [None, "predefined_property_set"],
    "modelcheck_window":       [None, "modelcheck_window"],
    "modelcheck_results":      [None, "modelcheck_results"],
    "modelcheck_external":     [None, "modelcheck_external"],
    "modelcheck":              [None, "modelcheck"],
    "ifc_importer":            [None, "ifc_importer"],
    "util":                    [None, "util"],
    "exports": [None, "exports"],
    "attribute_import": [None, "attribute_import"],
    "mapping": [None, 'mapping'],
    "popups":  [None, 'popups'],
}
plugins_dict = {
    "aggregation_window": {
    "window":        [None, "window"],
    "view":          [None, "view"],
    "node":          [None, "node"],
    "connection":    [None, "connection"],
    "aggregation":   [None, "aggregation"],
        "aw_modelcheck":   [None, "modelcheck"],
        "grouping_window": [None, "grouping_window"],
    },
}
for key, (_, name) in modules.items():
    modules[key][0] = importlib.import_module(f"som_gui.module.{name}")
for plugin_name, plugin_modules in plugins_dict.items():
    if not settings.get_setting_plugin_activated(plugin_name):
        continue

    for key, (_, name) in plugin_modules.items():
        text = f".{plugin_name}.module.{name}"

        plugins_dict[plugin_name][key][0] = importlib.import_module(text, f"som_gui.plugins")
    modules.update(plugin_modules)


def register():
    modules["project"][0].register()
    modules["main_window"][0].register()
    for k, (mod, _) in modules.items():
        if k not in ("project", "main_window"):
            mod.register()


def load_ui_triggers():
    modules["project"][0].load_ui_triggers()
    modules["main_window"][0].load_ui_triggers()
    for k, (mod, _) in modules.items():
        if k not in ("project", "main_window"):
            mod.load_ui_triggers()


def on_new_project():
    for k, (mod, _) in modules.items():
        if k != "project":
            mod.on_new_project()
