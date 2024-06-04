from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtGui import QPainter, QPainterPath
from SOMcreator.constants import value_constants

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool
    from som_gui.aggregation_window.module.connection import ui as ui_connection


def paint_connection(active_connection: ui_connection.Connection, connection: Type[tool.Connection]):
    path = QPainterPath()
    point_bottom = connection.get_node_top_anchor(active_connection.bottom_node)
    point_top = connection.get_node_bottom_anchor(active_connection.top_node)
    point_top.setX(point_top.x() + connection.get_connection_displacement(active_connection))
    if active_connection.connection_type == value_constants.AGGREGATION:
        point_list = connection.get_aggregation_point_list(point_bottom, point_top)

    elif active_connection.connection_type == value_constants.INHERITANCE:
        point_list = connection.get_inheritance_point_list(point_bottom, point_top)
    else:
        point_list = connection.get_combo_point_list(point_bottom, point_top)

    path.moveTo(point_list[0])
    for point in point_list[1:]:
        path.lineTo(point)
    active_connection.setPath(path)
    active_connection.last_anchor_points = [point_top, point_bottom]
