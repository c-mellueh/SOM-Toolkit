from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QStyleOptionGraphicsItem, \
    QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QBrush, QColor
from . import trigger
import SOMcreator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node.ui import NodeProxy


class Connection(QGraphicsPathItem):
    def __init__(self, top_node: NodeProxy, bottom_node: NodeProxy, connection_type: int):
        super().__init__()
        self.top_node: NodeProxy | None = top_node
        self.bottom_node: NodeProxy | None = bottom_node
        self.connection_type = connection_type
        self.setPen(QPen(Qt.black))
        self.last_anchor_points: tuple[QPointF, QPointF] | tuple[None, None] = (None, None)

    def paint(self, painter, option, widget):
        trigger.paint_connection(self)
        super().paint(painter, option, widget)
