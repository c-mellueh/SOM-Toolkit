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
    core.mouse_move_event(position, aw_tool.View, aw_tool.Node, aw_tool.Connection)


def mouse_press_event(position):
    core.mouse_press_event(position, aw_tool.View, aw_tool.Node, aw_tool.Connection)


def mouse_release_event(pos):
    core.mouse_release_event(pos, aw_tool.View, aw_tool.Connection, tool.Search)


def mouse_wheel_event(event):
    core.mouse_wheel_event(event, aw_tool.View)


def context_menu_requested(pos):
    core.context_menu_requested(pos, aw_tool.View, aw_tool.Node, tool.Search)



def selection_changed():
    print("Selection changed")
