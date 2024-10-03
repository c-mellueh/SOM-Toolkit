from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtGui import QPalette
if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window import tool
    from som_gui.plugins.aggregation_window.module.connection import ui as ui_connection


def paint_connection(active_connection: ui_connection.Connection, connection: Type[tool.Connection]) -> None:
    point_bottom = connection.get_node_top_anchor(active_connection.bottom_node)
    point_top = connection.get_node_bottom_anchor(active_connection.top_node)
    displacement = connection.get_connection_displacement(active_connection)
    path = connection.calculate_painter_path(point_top, point_bottom, displacement, active_connection.connection_type)
    active_connection.setPath(path)