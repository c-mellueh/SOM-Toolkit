from . import prop, trigger, ui
import som_gui

ALL = "Alles"

def register():
    som_gui.AttributeImportProperties = prop.AttributeImportProperties()
    som_gui.AttributeImportSQLProperties = prop.AttributeImportSQLProperties()

def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
