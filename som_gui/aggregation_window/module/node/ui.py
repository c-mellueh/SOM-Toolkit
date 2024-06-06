from __future__ import annotations
from PySide6.QtCore import QSizeF, Qt
from PySide6.QtGui import QColor, QPainter, QPen

from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QStyleOptionGraphicsItem, \
    QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsEllipseItem, QGraphicsTextItem

import som_gui.aggregation_window.tool
from . import trigger
import SOMcreator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection.ui import Connection


class NodeProxy(QGraphicsProxyWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header: Header | None = None
        self.frame: Frame | None = None
        self.circle: Circle | None = None
        self.aggregation: SOMcreator.classes.Aggregation | None = None
        self.top_connection: Connection | None = None
        self.bottom_connections: set[Connection] = set()
        self.resize_rect: ResizeRect | None = None
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

    def widget(self) -> QWidget | NodeWidget:
        return super().widget()

    def paint(self, *args, **kwargs):
        super().paint(*args, **kwargs)
        trigger.paint_node(self)


class NodeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.button = QPushButton(self.tr('Subelement hinzufügen'))
        self.layout().addWidget(self.button)
        self.button.hide()

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()


class PropertySetTree(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemDoubleClicked.connect(trigger.pset_tree_double_clicked)
        self.node: NodeProxy | None = None

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.paint_propertyset_tree(self)


class Header(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)

    def paint(self, painter, option, widget):
        trigger.paint_header(self, painter)

    def mouseMoveEvent(self, event):
        last_pos = self.pos()
        super().mouseMoveEvent(event)
        new_pos = self.pos()
        dif = new_pos - last_pos
        trigger.drag_move(self, dif)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        trigger.header_clicked(self)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        trigger.hover_enter_header(self)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        trigger.hover_leave_header(self)


class Frame(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)


class ResizeRect(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setBrush(Qt.GlobalColor.transparent)
        self.setPen(QPen(Qt.GlobalColor.transparent))
        self.node: NodeProxy | None = None
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        trigger.hover_enter_resize_rect(self)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        trigger.hover_leave_resize_rect(self)


class Circle(QGraphicsEllipseItem):
    DIAMETER = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)
        self.setAcceptHoverEvents(True)
        self.node: None | NodeProxy = None
        self.setBrush(Qt.GlobalColor.white)
        self.setPen(QPen(Qt.GlobalColor.black))
        self.text = PlusText("+")
        # self.text.font().setPointSize(self.text.font().pointSize()*2)
        self.text.document().setPageSize(QSizeF(self.DIAMETER, self.DIAMETER))
        self.text.setParentItem(self)

    def paint(self, painter, option, widget):
        trigger.paint_circle(self)
        super().paint(painter, option, widget)


class PlusText(QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node: None | NodeProxy = None
