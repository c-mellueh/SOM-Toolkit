from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from SOMcreator import Aggregation
from SOMcreator.constants import value_constants
import som_gui
import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window.module.connection import constants
from som_gui.plugins.aggregation_window.module.connection import ui as connection_ui
from som_gui.plugins.aggregation_window.module.connection import trigger as connection_trigger

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPalette

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.node import ui as node_ui
    from som_gui.plugins.aggregation_window.module.connection.prop import ConnectionProperties
    from som_gui.plugins.aggregation_window.module.view import ui as view_ui


class Connection(som_gui.plugins.aggregation_window.core.tool.Connection):
    @classmethod
    def get_properties(cls) -> ConnectionProperties:
        return som_gui.ConnectionProperties

    @classmethod
    def create_connection(cls, top_node: node_ui.NodeProxy, bottom_node: node_ui.NodeProxy,
                          connection_type: int) -> Connection:
        top_node.aggregation.add_child(bottom_node.aggregation, connection_type)
        connection = connection_ui.Connection(top_node, bottom_node, connection_type)
        connection_trigger.paint_connection(connection)
        top_node.bottom_connections.add(connection)
        bottom_node.top_connection = connection
        connection.setZValue(0)
        logging.debug(f"Add Con : {connection.bottom_node.aggregation.name} -> {connection.top_node.aggregation.name}")
        return connection

    @classmethod
    def _get_base_points(cls, point_bottom: QPointF, point_top: QPointF) -> list[QPointF]:
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
        return points

    @classmethod
    def get_aggregation_point_list(cls, point_bottom: QPointF, point_top: QPointF) -> list[QPointF]:
        points = cls._get_base_points(point_bottom, point_top)
        points[3].setY(point_top.y() + constants.ARROW_HEIGHT)
        points[4].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[5].setY(point_top.y())
        points[6].setY(point_top.y() + constants.ARROW_HEIGHT / 2)
        points[7].setY(point_top.y() + constants.ARROW_HEIGHT)
        return points

    @classmethod
    def get_inheritance_point_list(cls, point_bottom, point_top) -> list[QPointF]:
        points = cls._get_base_points(point_bottom, point_top)

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
        connections = {aggreg.parent_connection for aggreg in connection.top_node.aggregation.get_children(filter=True)}
        disp_dict = dict()
        agg = value_constants.AGGREGATION
        inh = value_constants.INHERITANCE
        factor = 3

        if len(connections) == 1:
            disp_dict = {agg: 0, inh: 0, agg + inh: 0}

        if len(connections) == 2:
            if {value_constants.AGGREGATION, value_constants.INHERITANCE} == connections:
                disp_dict = {inh: -constants.ARROW_WIDTH * factor, agg: +constants.ARROW_WIDTH * factor, agg + inh: 0}

            if {value_constants.AGGREGATION, value_constants.INHERITANCE + value_constants.AGGREGATION} == connections:
                disp_dict = {agg: -constants.ARROW_WIDTH * factor, inh: 0, agg + inh: +constants.ARROW_WIDTH * factor}

            if {value_constants.INHERITANCE, value_constants.INHERITANCE + value_constants.AGGREGATION} == connections:
                disp_dict = {agg: 0, inh: +constants.ARROW_WIDTH * factor, agg + inh: -constants.ARROW_WIDTH * factor}

        if len(connections) == 3:
            disp_dict = {inh: -constants.ARROW_WIDTH * factor, agg: 0, agg + inh: +constants.ARROW_WIDTH * factor}
        return disp_dict.get(connection.connection_type) or 0.

    @classmethod
    def set_draw_node(cls, node: node_ui.NodeProxy) -> None:
        cls.get_properties().draw_node = node

    @classmethod
    def get_draw_node(cls) -> node_ui.NodeProxy:
        return cls.get_properties().draw_node

    @classmethod
    def calculate_painter_path(cls, point_top: QPointF, point_bottom: QPointF, displacement: float,
                               connection_type: int) -> QPainterPath:
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
    def draw_connection(cls, scene: view_ui.AggregationScene, mouse_pos: QPointF) -> None:
        connection = cls.get_properties().draw_connection
        if connection is None:
            connection = QGraphicsPathItem()
            scene.addItem(connection)
        point_top = cls.get_node_bottom_anchor(cls.get_draw_node())
        point_bottom = mouse_pos
        displacement = 0.
        path = cls.calculate_painter_path(point_top, point_bottom, displacement, 1)
        connection.setPath(path)
        connection.setPen(QPalette().accent().color())
        cls.get_properties().draw_connection = connection

    @classmethod
    def delete_draw_connection(cls) -> None:
        connection = cls.get_properties().draw_connection
        cls.set_draw_started(False)
        if connection is None:
            return

        connection.scene().removeItem(connection)
        cls.get_properties().draw_connection = None

    @classmethod
    def set_draw_started(cls, value: bool) -> None:
        cls.get_properties().draw_started = value

    @classmethod
    def is_drawing_started(cls) -> bool:
        return cls.get_properties().draw_started
