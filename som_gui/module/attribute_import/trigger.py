from som_gui import tool
from som_gui.core import attribute_import as core
def connect():
    tool.MainWindow.add_action("Modelle/Modellinformationen Einlesen21",
                               lambda: core.open_window(tool.AttributeImport, tool.IfcImporter))


def on_new_project():
    pass
