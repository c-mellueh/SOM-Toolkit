from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtGui import QPainter, QPainterPath

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool


def paint_connection(connection, painter: QPainter, option, widget, node: Type[tool.Node]):
    painter.save()
    painter.restore()
    path = QPainterPath()
