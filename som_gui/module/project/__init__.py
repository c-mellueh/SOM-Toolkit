import som_gui
from . import ui, trigger, prop,window


def register():
    som_gui.ProjectProperties = prop.ProjectProperties


def load_ui_triggers():
    print(F"Load UI Triggers")
    ui.load_triggers()
