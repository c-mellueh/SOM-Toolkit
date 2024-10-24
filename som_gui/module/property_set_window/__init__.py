import som_gui
from . import prop, trigger, ui


def register():
    som_gui.PropertySetWindowProperties = prop.PropertySetWindowProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
