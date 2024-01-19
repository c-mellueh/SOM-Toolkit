import logging
from . import ui, trigger, prop
import som_gui

OK = 0
IDENT_ISSUE = 1
ABBREV_ISSUE = 2


def register():
    som_gui.ObjectProperties = prop.ObjectProperties


def load_ui_triggers():
    logging.info(f"Load Objects UI Triggers")
    ui.load_triggers()


def on_new_project():
    pass
