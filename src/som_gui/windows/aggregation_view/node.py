from __future__ import annotations  # make own class referencable
from typing import TYPE_CHECKING
from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPen, QPainter, QCursor,QPainterPath
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsSceneMouseEvent,QGraphicsPathItem, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsTextItem,QGraphicsView,QGraphicsEllipseItem
from ...data import constants
from ...windows import popups

from SOMcreator import classes

if TYPE_CHECKING:
    from src.som_gui.main_window import MainWindow
    from .aggregation_window import AggregationScene,AggregationWindow

class Header(QGraphicsRectItem):
    def __init__(self, node: NodeProxy, text):
        super(Header, self).__init__()
        self.node_proxy = node
        self._title = text
        self.setParentItem(self.node_proxy)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.resize()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self,value) -> None:
        self._title = value
        self.update()

    def resize(self):
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
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.title)
        super().paint(painter, option, widget)


class Frame(QGraphicsRectItem):
    def __init__(self, node: NodeProxy):
        super(Frame, self).__init__()
        self.setParentItem(node)
        self.node_proxy = node
        self.resize()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, False)

    def resize(self):
        rect = self.node_proxy.rect()
        rect.setWidth(rect.width() - self.pen().width() / 2)
        rect.setY(rect.y()-constants.HEADER_HEIGHT)
        rect.setHeight(rect.height())
        rect.setX(self.x() + self.pen().width() / 2)
        self.setRect(rect)




class Circle(QGraphicsEllipseItem):
    DIAMETER = 25
    def __init__(self,node_proxy:NodeProxy):
        super(Circle, self).__init__(0,0,self.DIAMETER,self.DIAMETER)
        self.node_proxy = node_proxy
        self.setParentItem(node_proxy)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent,False)
        self.resize()
        self.setZValue(2)
        self.hide()
        self.setAcceptHoverEvents(True)

    def resize(self):
        x = self.node_proxy.rect().center().x()-self.DIAMETER/2
        y = self.node_proxy.rect().bottom()-self.DIAMETER/2
        self.setPos(x,y)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
        painter.save()
        painter.restore()
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(0,0,self.DIAMETER,self.DIAMETER)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "+")
        super().paint(painter, option, widget)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if not self.node_proxy.isUnderMouse():
            self.hide()
        super(Circle, self).hoverLeaveEvent(event)

class NodeProxy(QGraphicsProxyWidget):
    _registry = set()
    def __init__(self, aggregation: classes.Aggregation, pos: QPointF) -> None:

        super(NodeProxy, self).__init__()
        self._registry.add(self)
        self.aggregation:classes.Aggregation = aggregation
        self._title = str()
        self.reset_title()

        self.setWidget(NodeWidget())
        self.widget().tree_widget.fill_tree()
        self.top_connection:Connection|None = None
        self.bottom_connections :set[Connection] = set()
        self.header = Header(self, self.title)
        self.frame = Frame(self)
        self.setPos(pos)

        geometry = self.geometry()
        geometry.setHeight(150)
        self.setGeometry(geometry)
        self.circle = Circle(self)

    def reset_title(self):
        self.title = f"{self.aggregation.name}\nidentitaet: {self.aggregation.id_group()}"

    def set_title_by_attribute(self,pset_name:str,attribute_name:str):
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

        self.title =  f"{self.aggregation.name}\n{attribute_name}: {attribute.value[0]}"

    def aggregation_dict(self) -> dict[classes.Aggregation,NodeProxy]:
        return self.aggregation_window().aggregation_dict()

    def aggregation_window(self) -> AggregationWindow:
        view =  self.scene().views()[0]
        return view.window()

    def scene(self) -> AggregationScene:
        return super(NodeProxy, self).scene()

    def moveBy(self, dx: float, dy: float) -> None:
        super(NodeProxy, self).moveBy(dx,dy)
        self.update_connections()

    def update_connections(self):
        for connection in self.bottom_connections:
            connection.update_line()
        if self.top_connection is not None:
            self.top_connection.update_line()
        self.update()

    def child_nodes(self) -> set[NodeProxy]:
        return set(self.aggregation_dict().get(aggreg) for aggreg in self.aggregation.children)

    def delete(self):
        for connection in list(self.bottom_connections):
            connection.delete()
        self.top_connection.delete()
        self.aggregation.delete()
        self.deleteLater()
        self._registry.remove(self)

    def bottom_anchor_point(self) -> QPointF:
        """Point where Connection will end"""
        scene_bounding_rect = self.sceneBoundingRect()
        x = scene_bounding_rect.center().x()
        y = scene_bounding_rect.y()+scene_bounding_rect.height()
        return QPointF(x,y)

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
    def title(self):
        return self._title

    @title.setter
    def title(self,value):
        self._title = value
        try:
            self.header.title = value
        except AttributeError:
            pass

    @property
    def uuid(self) -> str:
        return self.aggregation.uuid

    def __str__(self):
        return f"{self.aggregation.name}"

    def setZValue(self, z: float) -> None:
        super(NodeProxy, self).setZValue(z)
        self.frame.setZValue(1)
        self.header.setZValue(1)

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

        try:
            self.update_connections()
        except AttributeError:
            pass

        try:
            self.circle.resize()
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
        #self.widget().button.show()
        self.circle.show()
        super(NodeProxy, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if not self.circle.isUnderMouse():
            self.circle.hide()
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
        self.itemDoubleClicked.connect(self.item_clicked)

    @property
    def object(self):
        return self.node_widget.object

    @property
    def main_window(self) -> MainWindow:
        return self.node_widget.graphicsProxyWidget().scene().views()[0].window().main_window

    def fill_tree(self) -> None:
        for property_set in self.object.property_sets:
            item = CustomPSetTreeItem(self, property_set)
            for attribute in property_set.attributes:
                CustomAttribTreeItem(item, attribute)

    def item_clicked(self,item:CustomPSetTreeItem|CustomAttribTreeItem):
        main_window = self.main_window

        if isinstance(item, CustomPSetTreeItem):
            property_set = item.property_set
            main_window.open_pset_window(property_set, self.object, None)

        if isinstance(item, CustomAttribTreeItem):
            property_set = item.attribute.property_set
            main_window.open_pset_window(property_set, self.object, None)
            main_window.pset_window.fill_with_attribute(item.attribute)

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
        self.button = QPushButton("add Subelement")
        self.layout().addWidget(self.button)
        self.button.hide()
        self.tree_widget = CustomPsetTree(self)
        self.layout().insertWidget(0, self.tree_widget)

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        main_window = self.graphicsProxyWidget().scene().views()[0].window().main_window
        search = popups.ObjectSearchWindow(main_window)

        if not search.exec():
            return
        obj = search.selected_object
        aggregation = classes.Aggregation(obj,None,obj.description,False)
        rect = self.graphicsProxyWidget().sceneBoundingRect()
        input_point = rect.bottomLeft()
        input_point.setY(input_point.y()+constants.BOX_MARGIN)
        input_point.setX(input_point.x()+constants.BOX_MARGIN)
        proxy_node = NodeProxy(aggregation,input_point)
        self.aggregation.add_child(proxy_node.aggregation)
        self.scene().add_node(proxy_node,False)
        self.scene().add_connection(self.graphicsProxyWidget(),proxy_node)

    def scene(self) -> AggregationScene:
        return self.graphicsProxyWidget().scene()

    @property
    def aggregation(self):
        return self.graphicsProxyWidget().aggregation

    @property
    def object(self):
        return self.aggregation.object

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()

class Connection(QGraphicsPathItem):

    def __init__(self, bottom_node: NodeProxy, top_node: NodeProxy) -> None:
        super(Connection, self).__init__()

        self.bottom_node: NodeProxy = bottom_node
        self.top_node: NodeProxy = top_node
        self.setZValue(0)
        self.top_node.scene().addItem(self)
        bottom_node.top_connection = self
        top_node.bottom_connections.add(self)
        self.path = QPainterPath()
        self.update_line()
        self.setAcceptHoverEvents(False)

    def __str__(self) -> str:
        return f"Connection [{self.bottom_node.name}->{self.top_node.name}]"

    def delete(self):
        self.top_node.bottom_connections.remove(self)
        self.bottom_node.top_connection = None
        self.scene().removeItem(self)

    def update_line(self) -> None:
        self.path = QPainterPath()
        self.path.moveTo(self.points[0])
        for point in self.points[1:]:
            self.path.lineTo(point)
        self.setPath(self.path)
        self.setPos(0.0, 0.0)
        self.setZValue(0)

    @property
    def connection_type(self) -> int:
        return self.bottom_node.aggregation.connection_dict[self.top_node.aggregation]

    def get_connection_displacement(self):
        aggreg:classes.Aggregation
        connections = {aggreg.parent_connection for aggreg in self.top_node.aggregation.children}
        displacement_dict = dict()

        FACTOR = 3

        if len(connections) == 1:
            displacement_dict= {constants.AGGREGATION:0,
                    constants.INHERITANCE:0,
                    constants.AGGREGATION+constants.INHERITANCE:0}

        if len(connections) == 2:
            if {constants.AGGREGATION,constants.INHERITANCE} == connections:
                displacement_dict=  {constants.INHERITANCE:-constants.ARROW_WIDTH*FACTOR,
                constants.AGGREGATION:+constants.ARROW_WIDTH*FACTOR,
                constants.AGGREGATION+constants.INHERITANCE:0}

            if {constants.AGGREGATION,constants.INHERITANCE+constants.AGGREGATION} == connections:
                displacement_dict=  {constants.AGGREGATION:-constants.ARROW_WIDTH*FACTOR,
                constants.INHERITANCE:0,
                constants.AGGREGATION+constants.INHERITANCE:+constants.ARROW_WIDTH*FACTOR}

            if {constants.INHERITANCE,constants.INHERITANCE+constants.AGGREGATION} == connections:
                displacement_dict=  {constants.AGGREGATION: 0,
                constants.INHERITANCE: +constants.ARROW_WIDTH * FACTOR,
                constants.AGGREGATION + constants.INHERITANCE:-constants.ARROW_WIDTH * FACTOR }

        if len(connections) == 3:
            displacement_dict = {constants.INHERITANCE: -constants.ARROW_WIDTH * FACTOR,
             constants.AGGREGATION: 0,
             constants.AGGREGATION + constants.INHERITANCE:+constants.ARROW_WIDTH * FACTOR }

        return displacement_dict.get(self.connection_type)

    @property
    def points(self) -> list[QPointF]:
        def aggregation_points():
            points[0] = pb

            points[1].setX(pb.x())
            points[2].setX(pt.x())
            points[3].setX(pt.x())
            points[4].setX(pt.x() - constants.ARROW_WIDTH / 2)
            points[5].setX(pt.x())
            points[6].setX(pt.x() + constants.ARROW_WIDTH / 2)
            points[7].setX(pt.x())

            points[1].setY(mid_y - constants.ARROW_WIDTH / 2)
            points[2].setY(points[1].y())
            points[3].setY(pt.y() + constants.ARROW_HEIGHT)
            points[4].setY(pt.y() + constants.ARROW_HEIGHT / 2)
            points[5].setY(pt.y())
            points[6].setY(pt.y() + constants.ARROW_HEIGHT / 2)
            points[7].setY(pt.y() + constants.ARROW_HEIGHT)

        def inheritance_points():
            points[0] = pb
            points[1].setX(pb.x())
            points[2].setX(pt.x())
            points[3].setX(pt.x())
            points[4].setX(pt.x() - constants.ARROW_WIDTH / 2)
            points[5].setX(pt.x())
            points[6].setX(pt.x() + constants.ARROW_WIDTH / 2)
            points[7].setX(pt.x())

            points[1].setY(mid_y - constants.ARROW_HEIGHT / 2)
            points[2].setY(points[1].y())
            points[3].setY(pt.y() + constants.ARROW_HEIGHT / 2)
            points[4].setY(pt.y() + constants.ARROW_HEIGHT / 2)
            points[5].setY(pt.y())
            points[6].setY(pt.y() + constants.ARROW_HEIGHT / 2)
            points[7].setY(pt.y() + constants.ARROW_HEIGHT / 2)

        def combo_points():
            points[0] = pb

            points[1].setX(pb.x())
            points[2].setX(pt.x())
            points[3].setX(pt.x())
            points[4].setX(pt.x() - constants.ARROW_WIDTH / 2)
            points[5].setX(points[3].x())
            points[6].setX(points[5].x())
            points[7].setX(points[4].x())
            points[8].setX(points[5].x())
            points[9].setX(pt.x() + constants.ARROW_WIDTH / 2)
            points[10].setX(points[5].x())
            points[11].setX(points[5].x())
            points[12].setX(points[9].x())
            points[13].setX(points[5].x())

            points[1].setY(mid_y + constants.ARROW_HEIGHT / 2)
            points[2].setY(points[1].y())
            points[3].setY(pt.y() + constants.ARROW_HEIGHT * 2)
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

        points = [QPointF() for _ in range(8)]

        pb = self.bottom_node.top_anchor_point()  # top center of Bottom Node
        pt = self.top_node.bottom_anchor_point()
        pt.setX(pt.x()+self.get_connection_displacement())
        mid_y = (pt.y() + constants.BOX_BOTTOM_DISTANCE)

        if self.connection_type == constants.AGGREGATION:
            aggregation_points()

        elif self.connection_type == constants.INHERITANCE:
            inheritance_points()
        else:
            points = [QPointF() for _ in range(14)]
            combo_points()
        return points

