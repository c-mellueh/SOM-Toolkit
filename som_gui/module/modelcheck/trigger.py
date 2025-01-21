from som_gui import tool
from som_gui.core import modelcheck as core


def connect():
    pass


def start_modelcheck(runner):
    core.check_file(runner, tool.Modelcheck, tool.ModelcheckWindow)


def on_new_project():
    pass


def retranslate_ui():
    pass
