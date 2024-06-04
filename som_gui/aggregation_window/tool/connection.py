from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.classes import Aggregation
from SOMcreator.constants import value_constants
if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node import ui as node_ui
from som_gui.aggregation_window.module.connection import constants
import som_gui.aggregation_window.core.tool
from PySide6.QtCore import QPointF
from som_gui.aggregation_window.module.connection import ui as connection_ui
from som_gui.aggregation_window.module.connection import trigger as connection_trigger

class Connection(som_gui.aggregation_window.core.tool.Connection):
    @classmethod
    def create_connection(cls, top_node: node_ui.NodeProxy, bottom_node: node_ui.NodeProxy, connection_type: int):
        connection = connection_ui.Connection(top_node, bottom_node, connection_type)
        connection_trigger.paint_connection(connection)
        top_node.bottom_connections.add(connection)
        bottom_node.top_connection = connection
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

    @classmethod
    def get_inheritance_point_list(cls, point_bottom, point_top) -> list[QPointF]:
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

    @classmethod
    def get_combo_point_list(cls, point_bottom, point_top) -> list[QPointF]:
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

    @classmethod
    def get_node_top_anchor(cls, node: node_ui.NodeProxy):
        x = node.frame.sceneBoundingRect().center().x()
        y = node.frame.sceneBoundingRect().y()
        return QPointF(x, y)

    @classmethod
    def get_node_bottom_anchor(cls, node: node_ui.NodeProxy):
        x = node.frame.sceneBoundingRect().center().x()
        y = node.frame.sceneBoundingRect().y() + node.frame.sceneBoundingRect().height()
        return QPointF(x, y)

    @classmethod
    def get_connection_displacement(cls, connection: connection_ui.Connection) -> float:
        aggreg: Aggregation
        connections = {aggreg.parent_connection for aggreg in connection.top_node.aggregation.children}
        displacement_dict = dict()

        factor = 3
        if len(connections) == 1:
            displacement_dict = {value_constants.AGGREGATION:                               0,
                                 value_constants.INHERITANCE:                               0,
                                 value_constants.AGGREGATION + value_constants.INHERITANCE: 0}

        if len(connections) == 2:
            if {value_constants.AGGREGATION, value_constants.INHERITANCE} == connections:
                displacement_dict = {value_constants.INHERITANCE:                               -constants.ARROW_WIDTH * factor,
                                     value_constants.AGGREGATION:                               +constants.ARROW_WIDTH * factor,
                                     value_constants.AGGREGATION + value_constants.INHERITANCE: 0}

            if {value_constants.AGGREGATION, value_constants.INHERITANCE + value_constants.AGGREGATION} == connections:
                displacement_dict = {value_constants.AGGREGATION:                               -constants.ARROW_WIDTH * factor,
                                     value_constants.INHERITANCE:                               0,
                                     value_constants.AGGREGATION + value_constants.INHERITANCE: +constants.ARROW_WIDTH * factor}

            if {value_constants.INHERITANCE, value_constants.INHERITANCE + value_constants.AGGREGATION} == connections:
                displacement_dict = {value_constants.AGGREGATION:                               0,
                                     value_constants.INHERITANCE:                               +constants.ARROW_WIDTH * factor,
                                     value_constants.AGGREGATION + value_constants.INHERITANCE: -constants.ARROW_WIDTH * factor}

        if len(connections) == 3:
            displacement_dict = {value_constants.INHERITANCE:                               -constants.ARROW_WIDTH * factor,
                                 value_constants.AGGREGATION:                               0,
                                 value_constants.AGGREGATION + value_constants.INHERITANCE: +constants.ARROW_WIDTH * factor}

        return displacement_dict.get(connection.connection_type)
