import som_gui
from som_gui.module.use_case import ui, trigger, prop, window
import logging

def register():
    som_gui.UseCaseProperties = prop.UseCaseProperties


def load_ui_triggers():
    logging.info(f"Load Use-Case UI Triggers")
    ui.load_triggers()


def on_new_project():
    trigger.on_new_project()
