from . import prop, trigger
import som_gui


def register():
    som_gui.WindowProperties = prop.WindowProperties()


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
