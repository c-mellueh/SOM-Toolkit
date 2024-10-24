from __future__ import annotations

__version__ = "2.13.4"

import logging
from typing import TYPE_CHECKING

from som_gui import core, tool
from som_gui.resources.icons import get_icon

if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow

import importlib
import pkgutil

module = importlib.import_module("som_gui.module")
modules = [[m.name, None] for m in pkgutil.iter_modules(module.__path__) if m.ispkg]
preregister = ["logging", "project", "main_window"]

for index, (name, _) in enumerate(modules):
    logging.info(f"Importing Module '{name}'")
    modules[index][1] = importlib.import_module(f"som_gui.module.{name}")

for plugin_names in tool.Plugins.get_available_plugins():
    if tool.Plugins.is_plugin_active(plugin_names):
        modules += tool.Plugins.import_plugin(plugin_names)


def register():
    for module_name in preregister:
        index = [x[0] for x in modules].index(module_name)
        modules[index][1].register()

    for name, module in modules:
        if name not in preregister:
            module.register()


def load_ui_triggers():
    for module_name in preregister:
        index = [x[0] for x in modules].index(module_name)
        modules[index][1].load_ui_triggers()

    for name, module in modules:
        if name not in preregister:
            module.load_ui_triggers()


def retranslate_ui():
    for name, module in modules:
        module.retranslate_ui()


def on_new_project():
    for name, module in modules:
        module.on_new_project()
