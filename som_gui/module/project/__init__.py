import logging

import som_gui
from . import ui, trigger, prop,window


def register():
    som_gui.ProjectProperties = prop.ProjectProperties


def load_ui_triggers():
    logging.info(f"Load Project UI Triggers")
    ui.load_triggers()
