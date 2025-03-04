import logging

import som_gui
from . import prop, trigger, ui




def register():
    som_gui.ClassProperties = prop.ClassProperties


def load_ui_triggers():
    logging.info(f"Load Class UI Triggers")
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
