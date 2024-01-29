from __future__ import annotations
from typing import TYPE_CHECKING
from thefuzz import fuzz
if TYPE_CHECKING:
    from som_gui.main_window import MainWindow, Ui_MainWindow

__version__ = "2.10.0bugfix"

import importlib

modules = {
    "use_case": None,
    "project": None,
    "objects": None,
    "search": None,
    "property_set": None,
    "attribute":   None,
    "main_window": None,
}


class MainUi:
    ui: Ui_MainWindow = None
    window: MainWindow = None

for name in modules.keys():
    modules[name] = importlib.import_module(f"som_gui.module.{name}")


def register():
    modules["project"].register()
    for name, mod in sorted(modules.items()):
        if name != "project":
            mod.register()


def load_ui_triggers():
    modules["project"].load_ui_triggers()
    for name, mod in sorted(modules.items()):
        if name != "project":
            mod.load_ui_triggers()


def on_new_project():
    for name, mod in sorted(modules.items()):
        if name != "project":
            mod.on_new_project()

