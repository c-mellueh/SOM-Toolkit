import som_gui
from . import ui, prop, trigger


def register():
    som_gui.AggregationModelcheckProperties = prop.AggregationModelcheckProperties()
    pass


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
