from som_gui.aggregation_window.core import view as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool
def connect():
    pass


def on_new_project():
    core.import_positions(aw_tool.View, tool.Project)


def view_paint_event():
    core.paint_event(aw_tool.View, aw_tool.Node, aw_tool.Connection, tool.Project)


def mouse_move_event(position):
    core.mouse_move_event(position, aw_tool.View)


def mouse_press_event(position):
    core.mouse_press_event(position, aw_tool.View)


def mouse_release_event():
    core.mouse_release_event(aw_tool.View)


def mouse_wheel_event(event):
    core.mouse_wheel_event(event, aw_tool.View)
