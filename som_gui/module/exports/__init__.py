import som_gui
from . import prop, trigger, ui

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


def register():
    som_gui.ExportProperties = prop.ExportProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()


def retranslate_ui():
    trigger.retranslate_ui()
