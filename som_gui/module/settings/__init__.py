import som_gui
from . import ui, prop, trigger


def register():
    som_gui.SettingsProperties = prop.SettingsProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
