import som_gui
from . import prop, trigger


def register():
    som_gui.ViewProperties = prop.ViewProperties()


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
