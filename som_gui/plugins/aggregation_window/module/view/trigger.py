from som_gui import tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.core import view as core


def activate():
    pass

def deactivate():
    pass

def on_new_project() -> None:
    core.import_pos_from_project(aw_tool.View, tool.Project)


def view_paint_event() -> None:
    core.paint_event(aw_tool.View, aw_tool.Node, aw_tool.Connection, tool.Project)


def mouse_move_event(position) -> None:
    core.mouse_move_event(position, aw_tool.View, aw_tool.Node, aw_tool.Connection)


def mouse_press_event(position) -> None:
    core.mouse_press_event(position, aw_tool.View, aw_tool.Node, aw_tool.Connection)


def mouse_release_event(pos) -> None:
    core.mouse_release_event(pos, aw_tool.View, aw_tool.Connection, tool.Search,tool.Project)


def mouse_wheel_event(event) -> None:
    core.mouse_wheel_event(event, aw_tool.View)


def context_menu_requested(pos) -> None:
    core.context_menu_requested(pos, aw_tool.View, aw_tool.Node, tool.Search, aw_tool.Connection,aw_tool.Buchheim, tool.Project,
                                tool.Util)


def key_press_event(event) -> None:
    core.key_press_event(event, aw_tool.View, aw_tool.Connection,aw_tool.Node)

def key_release_event(event) -> None:
    core.key_release_event(event,aw_tool.View,aw_tool.Node)


def add_object_to_scene(obj, scene=None, parent_node=None, pos=None):
    return core.add_object_to_scene(obj, scene, parent_node, pos, aw_tool.View, aw_tool.Connection, aw_tool.Node)


def retranslate_ui():
    pass
