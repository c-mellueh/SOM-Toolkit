from . import ui, prop, trigger
import som_gui

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"


def register():
    som_gui.ExportsSettings = prop.ExportsSettings


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
