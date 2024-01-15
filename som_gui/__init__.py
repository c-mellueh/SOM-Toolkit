__version__ = "2.9.1"

import importlib

modules = {
    "use_case": None,
    "project": None,
}


class MainUi:
    ui = None


for name in modules.keys():
    modules[name] = importlib.import_module(f"som_gui.module.{name}")


def register():
    for mod in modules.values():
        mod.register()


def load_ui_triggers():
    for mod in modules.values():
        mod.load_ui_triggers()


register()
