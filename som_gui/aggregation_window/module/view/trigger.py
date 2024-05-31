from som_gui.aggregation_window.core import view as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool
def connect():
    pass


def on_new_project():
    core.import_positions(aw_tool.View, tool.Project)
