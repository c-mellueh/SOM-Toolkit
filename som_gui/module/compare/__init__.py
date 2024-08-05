from . import window, attribute_widget, ui, prop, trigger
import som_gui


def register():
    som_gui.CompareAttributesProperties = prop.CompareAttributesProperties()
    som_gui.CompareWindowProperties = prop.CompareWindowProperties()
    som_gui.CompareProjectSelectProperties = prop.CompareProjectSelectProperties()
    som_gui.ObjectFilterCompareProperties = prop.ObjectFilterCompareProperties()
def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
