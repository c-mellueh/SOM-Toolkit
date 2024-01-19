__version__ = "2.9.1"

import importlib

modules = {
    "use_case": None,
    "project": None,
    "objects": None,
    "search": None,
}


class MainUi:
    ui = None
    window = None

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

register()
