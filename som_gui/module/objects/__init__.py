import logging
from . import ui, trigger, prop
import som_gui


def register():
    som_gui.ObjectProperties = prop.ObjectProperties


def load_ui_triggers():
    logging.info(f"Load Objects UI Triggers")
    ui.load_triggers()


def on_new_project():
    pass
