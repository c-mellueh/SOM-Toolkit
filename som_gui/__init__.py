__version__ = "2.9.1"

import importlib


modules = {
    "use_case": None,
    "project": None,
}

for name in modules.keys():
    modules[name] = importlib.import_module(f"som_gui.module.{name}")


def register():
    for mod in modules.values():
        mod.register()


register()
