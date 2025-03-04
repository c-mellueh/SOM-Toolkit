import logging

import som_gui
from . import prop, trigger, ui

OK = 0
IDENT_ISSUE = 1
IDENT_PSET_ISSUE = 3
IDENT_PROPERTY_ISSUE = 4


def register():
    som_gui.ClassProperties = prop.ClassProperties


def load_ui_triggers():
    logging.info(f"Load Objects UI Triggers")
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
