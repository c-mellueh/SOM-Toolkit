from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node import ui as node_ui
from som_gui.aggregation_window.module.connection import constants
import som_gui.aggregation_window.core.tool
from PySide6.QtCore import QPointF


class Connection(som_gui.aggregation_window.core.tool.Connection):
    @classmethod
    def create_connection(cls, top_node: node_ui.NodeProxy, bottom_node: node_ui.NodeProxy, connection_type: int):
        connection = node_ui.Connection(top_node, bottom_node, connection_type)
        return connection

    @classmethod
    def get_aggregation_point_list(cls, point_bottom, point_top, ) -> list[QPointF]:
        points = [QPointF() for _ in range(8)]
        mid_y = (point_top.y() + constants.BOX_BOTTOM_DISTANCE)

        points[0] = point_bottom
        points[1].setX(point_bottom.x())
        points[2].setX(point_top.x())
        points[3].setX(point_top.x())
        points[4].setX(point_top.x() - constants.ARROW_WIDTH / 2)
        points[5].setX(point_top.x())
        points[6].setX(point_top.x() + constants.ARROW_WIDTH / 2)
        points[7].setX(point_top.x())

        points[1].setY(mid_y - constants.ARROW_WIDTH / 2)
        points[2].setY(points[1].y())
        points[3].setY(point_top.y() + constants.ARROW_HEIGHT)
        points[4].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[5].setY(point_top.y())
        points[6].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[7].setY(point_top.y() + constants.ARROW_HEIGHT)
        return points

    def get_inheritance_point_list(self, point_bottom, point_top) -> list[QPointF]:
        points = [QPointF() for _ in range(8)]
        mid_y = (point_top.y() + constants.BOX_BOTTOM_DISTANCE)

        points[0] = point_bottom
        points[1].setX(point_bottom.x())
        points[2].setX(point_top.x())
        points[3].setX(point_top.x())
        points[4].setX(point_top.x() - constants.ARROW_WIDTH / 2)
        points[5].setX(point_top.x())
        points[6].setX(point_top.x() + constants.ARROW_WIDTH / 2)
        points[7].setX(point_top.x())

        points[1].setY(mid_y - constants.ARROW_HEIGHT / 2)
        points[2].setY(points[1].y())
        points[3].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[4].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[5].setY(point_top.y())
        points[6].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[7].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        return points

    def get_combo_point_list(self, point_bottom, point_top) -> list[QPointF]:
        points = [QPointF() for _ in range(14)]
        mid_y = (point_top.y() + constants.BOX_BOTTOM_DISTANCE)
        points[0] = point_bottom

        points[1].setX(point_bottom.x())
        points[2].setX(point_top.x())
        points[3].setX(point_top.x())
        points[4].setX(point_top.x() - constants.ARROW_WIDTH / 2)
        points[5].setX(points[3].x())
        points[6].setX(points[5].x())
        points[7].setX(points[4].x())
        points[8].setX(points[5].x())
        points[9].setX(point_top.x() + constants.ARROW_WIDTH / 2)
        points[10].setX(points[5].x())
        points[11].setX(points[5].x())
        points[12].setX(points[9].x())
        points[13].setX(points[5].x())

        points[1].setY(mid_y + constants.ARROW_HEIGHT / 2)
        points[2].setY(points[1].y())
        points[3].setY(point_top.y() + constants.ARROW_HEIGHT * 2)
        points[4].setY(points[3].y() - constants.ARROW_HEIGHT / 2)
        points[5].setY(points[4].y() - constants.ARROW_HEIGHT / 2)
        points[6].setY(points[5].y() - constants.ARROW_HEIGHT / 2)
        points[7].setY(points[6].y())
        points[8].setY(points[6].y() - constants.ARROW_HEIGHT / 2)
        points[9].setY(points[6].y())
        points[10].setY(points[6].y())
        points[11].setY(points[5].y())
        points[12].setY(points[4].y())
        points[13].setY(points[3].y())
        return points
