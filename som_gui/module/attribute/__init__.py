import som_gui
from . import ui, prop, trigger


def register():
    som_gui.AttributeProperties = prop.AttributeProperties()
    som_gui.CompareAttributesProperties = prop.CompareAttributesProperties()


def load_ui_triggers():
    trigger.connect()


def retranslate_ui():
    trigger.retranslate_ui()

def on_new_project():
    trigger.on_new_project()
