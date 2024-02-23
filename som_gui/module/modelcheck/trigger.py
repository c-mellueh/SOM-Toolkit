from som_gui import tool
from som_gui.core import modelcheck as core
def connect():
    tool.MainWindow.add_action("Modelcheck/Interne Modellprüfung", lambda: core.open_window(tool.Modelcheck))


def on_new_project():
    pass
