from som_gui.aggregation_window.core import view as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool
def connect():
    pass


def on_new_project():
    core.import_positions(aw_tool.View, tool.Project)


def view_paint_event():
    core.paint_event(aw_tool.View, aw_tool.Node, tool.Project)
