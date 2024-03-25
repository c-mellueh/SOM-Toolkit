from som_gui.core import modelcheck_external as core
from som_gui import tool
def connect():
    tool.MainWindow.add_action("Datei/Export/Modellprüfung",
                               lambda: core.open_window(tool.ModelcheckExternal, tool.ModelcheckWindow, tool.Project))


def on_new_project():
    pass
