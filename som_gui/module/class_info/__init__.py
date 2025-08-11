from . import prop, trigger, ui
import som_gui


def register():
    som_gui.ClassInfoProperties = prop.ClassInfoProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
