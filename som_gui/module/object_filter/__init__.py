import som_gui
from som_gui.module.object_filter import ui, trigger, prop, window
import logging

def register():
    som_gui.ObjectFilterProperties = prop.ObjectFilterProperties


def load_ui_triggers():
    logging.info(f"Load Use-Case UI Triggers")
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
