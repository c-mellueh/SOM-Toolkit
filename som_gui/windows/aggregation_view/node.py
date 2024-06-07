from __future__ import annotations  # make own class referencable

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QCursor, QPainterPath, QColor, QPen
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QStyleOptionGraphicsItem, \
    QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsEllipseItem
from SOMcreator import classes, value_constants

from ...data import constants
from som_gui.core import property_set_window as property_set_window_core
from som_gui.core import attribute as attribute_core
from som_gui import tool

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow
    from .aggregation_window import AggregationScene, AggregationWindow


class NodeProxy(QGraphicsProxyWidget):
    _registry = set()

    def __init__(self, aggregation: classes.Aggregation, pos: QPointF) -> None:

        super(NodeProxy, self).__init__()
        self._registry.add(self)
        self.aggregation: classes.Aggregation = aggregation
        self._title = str()
        self.reset_title()

        self.setWidget(NodeWidget())
        self.widget().tree_widget.fill_tree()
        self.top_connection: Connection | None = None
        self.bottom_connections: set[Connection] = set()
        self.header = Header(self)
        self.frame = Frame(self)
        self.setPos(pos)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        self.frame.setZValue(1)
        self.header.setZValue(1)
        geometry = self.geometry()
        geometry.setHeight(150)
        self.setGeometry(geometry)
        self.circle = Circle(self)
        self.title_settings: list[None] | list[str] = [None, None]

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        super().paint(painter, option, widget)
        self.update()

    def level(self) -> int:
        if self.parent_node() is not None:
            return self.parent_node().level() + 1
        return 0

    def update(self, *args) -> None:
        super(NodeProxy, self).update(*args)
        self.frame.update()
        self.header.update()

        def refresh_title():
            if self.title_settings == [None, None]:
                self.reset_title()
            else:
                self.set_title_by_attribute(self.title_settings[0], self.title_settings[1])

        refresh_title()
        self.update_connections()
        try:
            self.frame.resize()
        except AttributeError:
            pass

        try:
            self.header.resize()
        except AttributeError:
            pass

        try:
            self.update_connections()
        except AttributeError:
            pass

        try:
            self.circle.resize()
        except AttributeError:
            pass

    def reset_title(self) -> None:
        """title is set to BaseText"""

        base_text = f"{self.aggregation.name} ({self.aggregation.object.abbreviation})"

        if self.aggregation.is_root:
            self.title = base_text
        else:
            self.title = f"{base_text}\nidGruppe: {self.aggregation.id_group()}"
        self.title_settings = [None, None]

    def set_title_by_attribute(self, pset_name: str | None, attribute_name: str | None) -> None:
        """Set Title by given Attribute"""
        self.title_settings = [pset_name, attribute_name]

        undef = f"{self.aggregation.name}\n{attribute_name}: undefined"
        obj = self.aggregation.object
        pset = obj.get_property_set_by_name(pset_name)
        if pset is None:
            self.title = undef
            return
        attribute = pset.get_attribute_by_name(attribute_name)
        if attribute is None:
            self.title = undef
            return

        if len(attribute.value) == 0:
            self.title = undef
            return

        self.title = f"{self.aggregation.name}\n{attribute_name}: {attribute.value[0]}"

    def aggregation_dict(self) -> dict[classes.Aggregation, NodeProxy]:
        aggreg_window = self.aggregation_window()
        if aggreg_window is None:
            return dict()
        return aggreg_window.aggregation_dict()

    def aggregation_window(self) -> AggregationWindow | None:
        if self.scene() is None:
            return None
        return self.scene().aggregation_window

    def scene(self) -> AggregationScene:
        """for typing"""
        return super(NodeProxy, self).scene()

    def update_connections(self) -> None:
        """Update Line of connections"""
        for connection in self.bottom_connections:
            connection.update_line()
        if self.top_connection is not None:
            self.top_connection.update_line()

    def child_nodes(self) -> set[NodeProxy]:
        return set(self.aggregation_dict().get(aggreg) for aggreg in self.aggregation.children)

    def parent_node(self) -> NodeProxy | None:
        """get NodeProxy of Parent"""
        aggreg = self.aggregation.parent
        return self.aggregation_dict().get(aggreg)

    def delete(self, recursive: bool = False) -> None:
        """Delete Node and existings Connections"""

        logging.debug(f"Delete Node {self.name}")
        scene: AggregationScene = self.scene()
        scene.aggregation_window.scene_dict[scene.name][constants.NODES].remove(self.aggregation.uuid)

        for connection in list(self.bottom_connections):
            connection.delete()

        if self.top_connection is not None:
            self.top_connection.delete()

        self.aggregation.delete()
        self.deleteLater()
        self._registry.remove(self)
        if not recursive:
            return

        for child in self.child_nodes():
            child.delete(recursive)

    def bottom_anchor_point(self) -> QPointF:
        """Point where Connection will end"""
        scene_bounding_rect = self.sceneBoundingRect()
        x = scene_bounding_rect.center().x()
        y = scene_bounding_rect.y() + scene_bounding_rect.height()
        return QPointF(x, y)

    def top_anchor_point(self) -> QPointF:
        """Point where Connection will start"""
        scene_bounding_rect = self.sceneBoundingRect()
        x = scene_bounding_rect.center().x()
        y = scene_bounding_rect.y()
        return QPointF(x, y)

    @property
    def name(self) -> str:
        return self.aggregation.name

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        try:
            self.header.title = value
        except AttributeError:
            pass

    @property
    def uuid(self) -> str:
        return self.aggregation.uuid

    def __str__(self) -> str:
        return f"Node {self.aggregation.name}"

    def setZValue(self, z: float) -> None:
        super(NodeProxy, self).setZValue(z)

    def setCursor(self, cursor: QCursor) -> None:
        self.scene().views()[0].viewport().setCursor(cursor)

    def sceneBoundingRect(self) -> QRectF:
        rect = super(NodeProxy, self).sceneBoundingRect()
        return rect.adjusted(0.0, - constants.HEADER_HEIGHT, 0.0, 0.0)

    def resize_by_cursor(self, old_pos: QPointF, new_pos: QPointF, orientation: int) -> None:
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
        self.circle.show()
        super(NodeProxy, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if not self.circle.isUnderMouse():
            self.circle.hide()
        super(NodeProxy, self).hoverEnterEvent(event)

    def widget(self) -> NodeWidget:
        return super(NodeProxy, self).widget()

    def button_clicked(self) -> None:
        obj = tool.Search.search_object()
        aggregation = classes.Aggregation(obj)
        rect = self.sceneBoundingRect()
        input_point = rect.bottomLeft()
        input_point.setY(input_point.y() + constants.BOX_MARGIN)
        input_point.setX(input_point.x() + constants.BOX_MARGIN)
        proxy_node = NodeProxy(aggregation, input_point)

        self.scene().add_node(proxy_node, False)
        Connection(proxy_node, self)


class Header(QGraphicsRectItem):
    def __init__(self, node: NodeProxy) -> None:
        super(Header, self).__init__()
        self.node_proxy = node
        self.setParentItem(self.node_proxy)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.resize()

    def resize(self) -> None:
        line_width = self.pen().width()  # if ignore Linewidth: box of Node and Header won't match
        x = line_width / 2
        width = self.node_proxy.widget().width() - line_width
        height = constants.HEADER_HEIGHT
        self.setRect(QRectF(x, -height, width, height))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        painter.save()
        painter.restore()
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.node_proxy.title)
        super().paint(painter, option, widget)


class Frame(QGraphicsRectItem):
    def __init__(self, node: NodeProxy) -> None:
        super(Frame, self).__init__()
        self.setParentItem(node)
        self.node_proxy = node
        self.resize()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)

    def resize(self) -> None:
        rect = self.node_proxy.rect()
        rect.setWidth(rect.width() - self.pen().width() / 2)
        rect.setY(rect.y() - constants.HEADER_HEIGHT)
        rect.setHeight(rect.height())
        rect.setX(self.x() + self.pen().width() / 2)
        self.setRect(rect)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        if self.node_proxy.isSelected():
            width = self.pen().widthF() * 2
            color = QColor("blue")
            painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.boundingRect())
        else:
            super(Frame, self).paint(painter, option, widget)


class Circle(QGraphicsEllipseItem):
    DIAMETER = 25

    def __init__(self, node_proxy: NodeProxy) -> None:
        super(Circle, self).__init__(0, 0, self.DIAMETER, self.DIAMETER)
        self.node_proxy = node_proxy
        self.setParentItem(node_proxy)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)
        self.setZValue(2)
        self.hide()
        self.setAcceptHoverEvents(True)
        self.resize()

    def resize(self) -> None:
        x = self.node_proxy.rect().center().x() - self.DIAMETER / 2
        y = self.node_proxy.rect().bottom() - self.DIAMETER / 2
        self.setPos(x, y)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        self.resize()
        painter.save()
        painter.restore()
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(0, 0, self.DIAMETER, self.DIAMETER)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "+")
        super().paint(painter, option, widget)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if not self.node_proxy.isUnderMouse():
            self.hide()
        super(Circle, self).hoverLeaveEvent(event)


class NodeWidget(QWidget):
    def __init__(self) -> None:
        super(NodeWidget, self).__init__()

        self.setLayout(QVBoxLayout())
        self.button = QPushButton("add Subelement")
        self.layout().addWidget(self.button)
        self.button.hide()
        self.tree_widget = CustomPsetTree(self)
        self.layout().insertWidget(0, self.tree_widget)

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()


class Connection(QGraphicsPathItem):
    NORMAL_MODE = 0
    DRAW_MODE = 1

    def __init__(self, bottom_node: NodeProxy, top_node: NodeProxy, mode=0,
                 connection_type=value_constants.AGGREGATION) -> None:
        super(Connection, self).__init__()
        self.mode: int = mode

        self.bottom_node: NodeProxy | None = None
        self.top_node: NodeProxy = top_node
        if self.mode != self.DRAW_MODE:
            self.add_bottom_node(bottom_node, connection_type)
            self.update_line()

        self.setZValue(0)
        self.top_node.scene().addItem(self)
        self.path = QPainterPath()
        self.setAcceptHoverEvents(False)

    def add_bottom_node(self, bottom_node: NodeProxy, connection_type) -> None:
        self.bottom_node = bottom_node
        self.bottom_node.top_connection = self
        self.top_node.bottom_connections.add(self)
        self.top_node.aggregation.add_child(bottom_node.aggregation, connection_type)
        self.mode = self.NORMAL_MODE

    def __str__(self) -> str:
        if self.mode != self.DRAW_MODE:
            return f"Connection [{self.bottom_node.name}->{self.top_node.name}]"
        else:
            return f"Connection [??? ->{self.top_node.name}]"

    def delete(self) -> None:
        if self in self.top_node.bottom_connections:
            self.top_node.bottom_connections.remove(self)
        if self.bottom_node is not None:
            self.bottom_node.aggregation.parent.remove_child(self.bottom_node.aggregation)
            self.bottom_node.aggregation.remove_parent()
            self.bottom_node.top_connection = None
        self.scene().removeItem(self)

    def update_line(self, mouse_pos=None) -> None:
        self.path = QPainterPath()
        points = self.get_points(mouse_pos)
        self.path.moveTo(points[0])
        for point in points[1:]:
            self.path.lineTo(point)
        self.setPath(self.path)
        self.setPos(0.0, 0.0)
        self.setZValue(0)

    @property
    def connection_type(self) -> int:
        con = self.bottom_node.aggregation.parent_connection
        return con




class CustomPsetTree(QTreeWidget):
    def __init__(self, node_widget: NodeWidget) -> None:
        super(CustomPsetTree, self).__init__()
        self.setExpandsOnDoubleClick(False)
        self.setColumnCount(1)
        self.setHeaderLabels(["Name"])
        self.node_widget = node_widget
        self.itemDoubleClicked.connect(self.item_clicked)

    @property
    def object(self) -> classes.Object:
        return self.node_widget.graphicsProxyWidget().aggregation.object

    @property
    def main_window(self) -> MainWindow:
        return self.node_widget.graphicsProxyWidget().scene().views()[0].window().main_window

    def fill_tree(self) -> None:
        for property_set in self.object.property_sets:
            item = CustomPSetTreeItem(self, property_set)
            for attribute in property_set.attributes:
                CustomAttribTreeItem(item, attribute)

    def item_clicked(self, item: CustomPSetTreeItem | CustomAttribTreeItem) -> None:
        if isinstance(item, CustomPSetTreeItem):
            property_set = item.property_set
            property_set_window_core.open_pset_window(property_set, tool.PropertySetWindow, tool.AttributeTable)

        if isinstance(item, CustomAttribTreeItem):
            property_set = item.attribute.property_set
            window = property_set_window_core.open_pset_window(property_set, tool.PropertySetWindow,
                                                               tool.AttributeTable)
            property_set_window_core.activate_attribute(item.attribute, window, tool.Attribute, tool.PropertySetWindow)

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
