import logging
import os
import logging


def main(name: str):
    module_path = os.path.abspath(os.path.join(os.curdir, "module", name))
    if os.path.exists(module_path):
        logging.warning("Module already exists")
    else:
        os.mkdir(module_path)
    init_path = os.path.join(module_path, "__init__.py")
    if os.path.exists(init_path):
        logging.warning("__init__.py already exists")
    with open(init_path, "w") as f:
        f.write(
            f"""import som_gui
from . import ui, prop, trigger


def register():
    som_gui.{name.title()}Properties = prop.{name.title()}Properties


def load_ui_triggers():
    trigger.connect()
    

def on_new_project():
    trigger.on_new_project()
    
""")

    prop_path = os.path.join(module_path, "prop.py")
    if os.path.exists(prop_path):
        logging.warning("prop.py already exists")
    with open(prop_path, "w") as f:
        f.write(
            f"""from __future__ import annotations

class {name.title()}Properties:
    pass
    
""")
    trigger_path = os.path.join(module_path, "trigger.py")
    if os.path.exists(trigger_path):
        logging.warning("trigger.py already exists")
    with open(trigger_path, "w") as f:
        f.write(
            f"""from __future__ import annotations
import som_gui
from som_gui.core import {name} as core
from typing import TYPE_CHECKING


def connect():
    pass
    
def on_new_project():
    pass
""")
    ui_path = os.path.join(module_path, "ui.py")
    if os.path.exists(ui_path):
        logging.warning("ui.py already exists")
    with open(ui_path, "w") as f:
        f.write(f"""

""")


if __name__ == "__main__":
    module_name = "settings"
    main(module_name)
