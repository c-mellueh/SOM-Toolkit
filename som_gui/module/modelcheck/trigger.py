from som_gui import tool
from som_gui.core import modelcheck as core


def connect():
    pass


def start_modelcheck(ifc_file):
    core.check_file(ifc_file, tool.Modelcheck, tool.ModelcheckWindow)


def on_new_project():
    pass


def retranslate_ui():
    pass
