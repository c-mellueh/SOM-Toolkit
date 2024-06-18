from som_gui.aggregation_window.core import modelcheck as core
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool


def connect():
    core.add_modelcheck_plugin(tool.Modelcheck, aw_tool.Modelcheck)


def on_new_project():
    pass
