from som_gui import tool
from som_gui.plugins.ifc_tools.core import move as core


def connect():
    tool.MainWindow.add_action("IfcTools/Move", lambda: core.open_window())


def on_new_project():
    pass
