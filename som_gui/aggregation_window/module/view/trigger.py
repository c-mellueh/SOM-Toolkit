from som_gui.aggregation_window.core import view as core
from som_gui.aggregation_window import tool as aw_tool
from som_gui import tool


def connect():
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
    core.mouse_release_event(pos, aw_tool.View, aw_tool.Connection, tool.Search)


def mouse_wheel_event(event) -> None:
    core.mouse_wheel_event(event, aw_tool.View)


def context_menu_requested(pos) -> None:
    core.context_menu_requested(pos, aw_tool.View, aw_tool.Node, tool.Search, aw_tool.Connection, tool.Project)
