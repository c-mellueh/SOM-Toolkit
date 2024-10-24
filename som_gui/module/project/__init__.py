import logging

import som_gui
from . import prop, trigger, ui


def register():
    som_gui.ProjectProperties = prop.ProjectProperties


def load_ui_triggers():
    logging.info(f"Load Project UI Triggers")
    trigger.connect()


def on_new_project():
    pass


def retranslate_ui():
    trigger.retranslate_ui()
