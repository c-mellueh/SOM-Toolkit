import som_gui
from . import qt, ui, prop, trigger


def register():
    som_gui.ModelcheckWindowProperties = prop.ModelcheckWindowProperties()


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
