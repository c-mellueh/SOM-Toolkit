from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from som_gui import core, tool

if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow

__version__ = "2.13.1"

import importlib
import pkgutil

module = importlib.import_module("som_gui.module")
modules = {m.name: [None, m.name] for m in pkgutil.iter_modules(module.__path__) if m.ispkg}

plugins_dict = {
    "aggregation_window": {
        "window":      [None, "window"],
        "view":        [None, "view"],
        "node":        [None, "node"],
        "connection":  [None, "connection"],
        "aggregation": [None, "aggregation"],
        "aw_modelcheck":   [None, "modelcheck"],
        "grouping_window": [None, "grouping_window"],
    },
}
for key, (_, name) in modules.items():
    logging.info(f"Importing Module '{name}'")
    modules[key][0] = importlib.import_module(f"som_gui.module.{name}")

for plugin_name, plugin_modules in plugins_dict.items():
    if not tool.Appdata.is_plugin_activated(plugin_name):
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
