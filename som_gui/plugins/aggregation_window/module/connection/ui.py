from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QPainter, QPalette, QPen
from PySide6.QtWidgets import QGraphicsPathItem, QStyleOptionGraphicsItem

from . import trigger

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.node.ui import NodeProxy


class Connection(QGraphicsPathItem):
    def __init__(self, top_node: NodeProxy, bottom_node: NodeProxy, connection_type: int):
        super().__init__()
        self.top_node: NodeProxy | None = top_node
        self.bottom_node: NodeProxy | None = bottom_node
        self.connection_type = connection_type
        self.setPen(QPen(QPalette().text().color()))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, *args, **kwargs):
        trigger.paint_connection(self)
        super().paint(painter, option, *args, **kwargs)
