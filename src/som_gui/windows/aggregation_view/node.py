from __future__ import annotations  # make own class referencable

from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPen, QPainter, QCursor
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsTextItem,QGraphicsView
from ...data import constants
from SOMcreator import classes

class Header(QGraphicsRectItem):
    def __init__(self, node: NodeProxy, text):
        super(Header, self).__init__()
        self.node = node
        self.title = text
        self.setParentItem(self.node)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.resize()

    def resize(self):
        line_width = self.pen().width()  # if ignore Linewidth: box of Node and Header won't match
        x = line_width / 2
        width = self.node.widget().width() - line_width
        height = constants.HEADER_HEIGHT
        self.setRect(QRectF(x, -height, width, height))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        painter.save()
        painter.restore()
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.title)
        super().paint(painter, option, widget)


class Frame(QGraphicsRectItem):
    def __init__(self, node: NodeProxy):
        super(Frame, self).__init__()
        self.setParentItem(node)
        self.node = node
        self.resize()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)

    def resize(self):
        rect = self.node.rect()
        rect.setWidth(rect.width() - self.pen().width() / 2)
        rect.setY(rect.y()-constants.HEADER_HEIGHT)
        rect.setHeight(rect.height())
        rect.setX(self.x() + self.pen().width() / 2)
        self.setRect(rect)


class NodeProxy(QGraphicsProxyWidget):
    """
    all Movement is controlled by the Header
    """
    def __init__(self, aggregation: classes.Aggregation, pos: QPointF) -> None:

        super(NodeProxy, self).__init__()
        self.aggregation = aggregation
        self._title = f"{self.aggregation.name} ({self.aggregation.object.ident_value})"

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)

        self.setWidget(NodeWidget())
        self.widget().tree_widget.fill_tree()

        self.header = Header(self, self.title)
        self.frame = Frame(self)
        self.setPos(pos)

    @property
    def name(self) -> str:
        return self.aggregation.name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,value):
        self._title = value
        self.header.title = value

    @property
    def uuid(self) -> str:
        return self.aggregation.uuid

    def __str__(self):
        return f"{self.aggregation.name}"

    def setZValue(self, z: float) -> None:
        super(NodeProxy, self).setZValue(z)
        self.frame.setZValue(z)
        self.header.setZValue(z)

    def setCursor(self, cursor) -> None:
        self.scene().views()[0].viewport().setCursor(cursor)

    def sceneBoundingRect(self) -> QRectF:
        rect = super(NodeProxy, self).sceneBoundingRect()
        rect.setY(rect.y() - constants.HEADER_HEIGHT)
        return rect

    def resizeEvent(self, event: QGraphicsSceneResizeEvent) -> None:
        super(NodeProxy, self).resizeEvent(event)
        try:
            self.frame.resize()
        except AttributeError:
            pass

        try:
            self.header.resize()
        except AttributeError:
            pass

    def resize_by_cursor(self, old_pos, new_pos, orientation):
        def resize_geometry(dx, dy):
            geometry = self.geometry()
            geometry.setWidth(geometry.width() + dx)
            geometry.setHeight(geometry.height() + dy)
            self.setGeometry(geometry)

        def resize_top(d: float):
            self.moveBy(0, -d)
            resize_geometry(0, d)

        def resize_left(d: float):
            self.moveBy(-d, 0)
            resize_geometry(d, 0)

        def resize_right(d: float):
            resize_geometry(-d, 0)

        def resize_bottom(d: float):
            resize_geometry(0, -d)

        delta = old_pos - new_pos

        if orientation in (3, 4, 5):
            resize_top(delta.y())

        if orientation in (1, 4, 7):
            resize_left(delta.x())

        if orientation in (2, 5, 8):
            resize_right(delta.x())

        if orientation in (6, 7, 8):
            resize_bottom(delta.y())

    def cursor(self) -> QCursor:
        return self.scene().views()[0].viewport().cursor()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.widget().button.show()
        super(NodeProxy, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.widget().button.hide()
        super(NodeProxy, self).hoverEnterEvent(event)

    def widget(self) -> NodeWidget:
        return super(NodeProxy, self).widget()

class CustomPsetTree(QTreeWidget):
    def __init__(self,node_widget:NodeWidget) -> None:
        super(CustomPsetTree, self).__init__()
        self.setExpandsOnDoubleClick(False)
        self.setColumnCount(1)
        self.setHeaderLabels(["Name"])
        self.node_widget = node_widget

    @property
    def object(self):
        return self.node_widget.object

    def fill_tree(self) -> None:
        for property_set in self.object.property_sets:
            item = CustomPSetTreeItem(self, property_set)
            for attribute in property_set.attributes:
                CustomAttribTreeItem(item, attribute)

class CustomPSetTreeItem(QTreeWidgetItem):
    def __init__(self, tree: QTreeWidget, pset: classes.PropertySet) -> None:
        super(CustomPSetTreeItem, self).__init__(tree)
        self._property_set = pset
        self.update()

    @property
    def property_set(self) -> classes.PropertySet:
        return self._property_set

    def update(self) -> None:
        self.setText(0, self.property_set.name)


class CustomAttribTreeItem(QTreeWidgetItem):
    def __init__(self, tree: CustomPSetTreeItem, attribute: classes.Attribute) -> None:
        super(CustomAttribTreeItem, self).__init__(tree)
        self._attribute = attribute
        self.update()

    @property
    def attribute(self) -> classes.Attribute:
        return self._attribute

    def update(self) -> None:
        self.setText(0, self.attribute.name)

class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.button = QPushButton("PressMe")
        self.layout().addWidget(self.button)
        self.button.hide()
        self.tree_widget = CustomPsetTree(self)
        self.layout().insertWidget(0, self.tree_widget)

    @property
    def aggregation(self):
        return self.graphicsProxyWidget().aggregation

    @property
    def object(self):
        return self.aggregation.object

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()
