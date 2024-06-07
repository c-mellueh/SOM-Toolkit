from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from SOMcreator.classes import Aggregation
from SOMcreator.constants import value_constants
import som_gui
if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node import ui as node_ui
    from som_gui.aggregation_window.module.connection.prop import ConnectionProperties
    from som_gui.aggregation_window.module.view import ui as view_ui
from som_gui.aggregation_window.module.connection import constants
import som_gui.aggregation_window.core.tool
from PySide6.QtCore import QPointF
from som_gui.aggregation_window.module.connection import ui as connection_ui
from som_gui.aggregation_window.module.connection import trigger as connection_trigger
from som_gui.aggregation_window import tool as aw_tool
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath
class Connection(som_gui.aggregation_window.core.tool.Connection):
    @classmethod
    def get_properties(cls) -> ConnectionProperties:
        return som_gui.ConnectionProperties

    @classmethod
    def create_connection(cls, top_node: node_ui.NodeProxy, bottom_node: node_ui.NodeProxy, connection_type: int):
        # if bottom_node.top_connection:
        #     aw_tool.View.remove_connection_from_scene(bottom_node.top_connection,aw_tool.View.get_active_scene())
        top_node.aggregation.add_child(bottom_node.aggregation, connection_type)
        connection = connection_ui.Connection(top_node, bottom_node, connection_type)
        connection_trigger.paint_connection(connection)
        top_node.bottom_connections.add(connection)
        bottom_node.top_connection = connection
        logging.debug(f"Add Con : {connection.bottom_node.aggregation.name} -> {connection.top_node.aggregation.name}")
        connection.setZValue(0)
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
        return displacement_dict.get(connection.connection_type) or 0

    @classmethod
    def set_draw_node(cls, node: node_ui.NodeProxy):
        cls.get_properties().draw_node = node

    @classmethod
    def get_draw_node(cls) -> node_ui.NodeProxy:
        return cls.get_properties().draw_node

    @classmethod
    def calculate_painter_path(cls, point_top: QPointF, point_bottom: QPointF, displacement, connection_type: int):
        path = QPainterPath()

        point_top.setX(point_top.x() + displacement)
        if connection_type == value_constants.AGGREGATION:
            point_list = cls.get_aggregation_point_list(point_bottom, point_top)

        elif connection_type == value_constants.INHERITANCE:
            point_list = cls.get_inheritance_point_list(point_bottom, point_top)
        else:
            point_list = cls.get_combo_point_list(point_bottom, point_top)

        path.moveTo(point_list[0])
        for point in point_list[1:]:
            path.lineTo(point)
        return path

    @classmethod
    def draw_connection(cls, scene: view_ui.AggregationScene, mouse_pos: QPointF):
        connection = cls.get_properties().draw_connection
        if connection is None:
            connection = QGraphicsPathItem()
            scene.addItem(connection)
        point_top = cls.get_node_bottom_anchor(cls.get_draw_node())
        point_bottom = mouse_pos
        displacement = 0.
        path = cls.calculate_painter_path(point_top, point_bottom, displacement, 1)
        connection.setPath(path)
        cls.get_properties().draw_connection = connection

    @classmethod
    def delete_draw_connection(cls):
        connection = cls.get_properties().draw_connection
        cls.set_draw_started(False)
        if connection is None:
            return

        connection.scene().removeItem(connection)
        cls.get_properties().draw_connection = None

    @classmethod
    def set_draw_started(cls, value: bool):
        cls.get_properties().draw_started = value

    @classmethod
    def get_draw_started(cls):
        return cls.get_properties().draw_started
