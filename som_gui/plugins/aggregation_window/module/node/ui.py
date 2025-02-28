from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QSizeF, Qt, QPointF, QPoint
from PySide6.QtGui import QPaintEvent, QPalette, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QGraphicsTextItem,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
)

import SOMcreator
from . import trigger

if TYPE_CHECKING:
    from ..connection.ui import Connection


class NodeProxy(QGraphicsProxyWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header: Header | None = None
        self.frame: Frame | None = None
        self.circle: Circle | None = None
        self.aggregation: SOMcreator.SOMAggregation | None = None
        self.top_connection: Connection | None = None
        self.bottom_connections: set[Connection] = set()
        self.resize_rect: ResizeRect | None = None
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

        self.thread = None  # needed for buchheim algorithm
        self._lmost_sibling = None  # needed for buchheim algorithm
        self.mod = 0  # needed for buchheim algorithm
        self.change = 0  # needed for buchheim algorithm
        self.shift = 0  # needed for buchheim algorithm
        self.ancestor = self  # needed for buchheim algorithm
        self.number = None  # needed for buchheim algorithm

        self.spacer = QSpacerItem(
            5, 5
        )  # used to create space in which the header can exist

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.aggregation.name

    def widget(self) -> QWidget | NodeWidget:
        return super().widget()

    def paint(self, *args, **kwargs) -> None:
        super().paint(*args, **kwargs)
        trigger.paint_node(self)


class NodeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()


class PropertySetTree(QTreeWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.itemDoubleClicked.connect(trigger.pset_tree_double_clicked)
        self.node: NodeProxy | None = None

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        trigger.paint_propertyset_tree(self)


class Header(QGraphicsRectItem):
    def __init__(self) -> None:
        super().__init__()
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)

    def paint(self, painter, *args, **kwargs) -> None:
        trigger.paint_header(self, painter)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        trigger.drag_move(self, event)
        # super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)
        trigger.header_clicked(self, event)

    def mouseDoubleClickEvent(self, event):
        trigger.header_double_clicked(self)
        return super().mouseDoubleClickEvent(event)


class Frame(QGraphicsRectItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)


class ResizeRect(QGraphicsRectItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setBrush(Qt.GlobalColor.transparent)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)


class Circle(QGraphicsEllipseItem):
    DIAMETER = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)
        self.setAcceptHoverEvents(True)
        self.node: None | NodeProxy = None
        self.setBrush(QPalette().base())
        self.setPen(QPen(QPalette().mid().color()))
        self.text: PlusText = PlusText("+")
        self.text.document().setPageSize(QSizeF(self.DIAMETER, self.DIAMETER))
        self.text.setParentItem(self)

    def paint(self, *args, **kwargs) -> None:
        trigger.paint_circle(self)
        super().paint(*args, **kwargs)


class PlusText(QGraphicsTextItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node: None | NodeProxy = None
