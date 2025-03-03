import som_gui
from . import prop, trigger, ui


def register():
    som_gui.PropertyProperties = prop.PropertyProperties()
    som_gui.ComparePropertyProperties = prop.ComparePropertyProperties()


def load_ui_triggers():
    trigger.connect()


def retranslate_ui():
    trigger.retranslate_ui()


def on_new_project():
    trigger.on_new_project()
