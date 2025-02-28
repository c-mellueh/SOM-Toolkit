from __future__ import annotations
__version__ = "2.14.0" #needs to be on top of som_gui import statements else ImportError

import logging
from typing import TYPE_CHECKING
from som_gui import core, tool
from som_gui.resources.icons import get_icon
import importlib
import pkgutil
if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow
    from types import ModuleType


#list all modules which are defined in the modules folder
module = importlib.import_module("som_gui.module")
#define Modules which should be initialized before the other Modules
preregister = ["logging", "project", "main_window"]

#Import Modules
modules:list[tuple[str,ModuleType]] = list()
for m in pkgutil.iter_modules(module.__path__):
    if not m.ispkg:
        continue
    logging.info(f"Importing Module '{m.name}'")
    path = f"som_gui.module.{m.name}"
    modules.append((m.name,importlib.import_module(path)))

#import Plugin Modules
for plugin_names in tool.Plugins.get_available_plugins():
    if tool.Plugins.is_plugin_active(plugin_names):
        modules += tool.Plugins.import_plugin(plugin_names)


def register():
    """
    registers the Properties of each Module
    :return:
    """
    #call the register() function in the __init__.py of every Module
    #Start with the Preregister
    for module_name in preregister:
        index = [x[0] for x in modules].index(module_name)
        modules[index][1].register()

    for name, module in modules:
        if name not in preregister:
            module.register()


def load_ui_triggers():
    """
    registers the PySide6 Signals/Slots of the Ui
    :return:
    """
    #call the load_ui_trigger() in the __init__.py of every Module
    #Start with the Preregister
    for module_name in preregister:
        index = [x[0] for x in modules].index(module_name)
        modules[index][1].load_ui_triggers()

    for name, module in modules:
        if name not in preregister:
            module.load_ui_triggers()


def retranslate_ui():
    """
    retranslates the UI to the set Language
    :return:
    """
    #call the retranslate_ui() in the __init__.py of every Module
    for name, module in modules:
        module.retranslate_ui()


def on_new_project():
    #call the on_new_project() in the __init__.py of every Module

    for name, module in modules:
        module.on_new_project()
