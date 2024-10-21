from som_gui.core import console as core
from som_gui import tool
def connect():
    core.create_console_trigger(tool.MainWindow, tool.Console)

def on_new_project():
    pass


def retranslate_ui():
    pass

def close_console():
    core.close(tool.Console)
