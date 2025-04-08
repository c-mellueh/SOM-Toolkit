import som_gui
from . import prop, qt, trigger, ui


def register():
    som_gui.ProjectFilterProperties = prop.ProjectFilterProperties()
    som_gui.FilterCompareProperties = prop.FilterCompareProperties()


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
