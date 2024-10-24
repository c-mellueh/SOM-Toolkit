import som_gui
from . import prop, trigger, ui


def register():
    som_gui.CompareWindowProperties = prop.CompareWindowProperties()
    som_gui.CompareProjectSelectProperties = prop.CompareProjectSelectProperties()


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
