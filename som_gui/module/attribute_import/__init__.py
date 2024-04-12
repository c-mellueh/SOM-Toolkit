from . import prop, trigger, window, settings_window, ui
import som_gui


def register():
    som_gui.AttributeImportProperties = prop.AttributeImportProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
