from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING, Type

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsScene, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsView
from SOMcreator import constants

from src.som_gui.data.constants import HEADER_HEIGHT
from src.som_gui.qt_designs import ui_GraphWindow

FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2

if TYPE_CHECKING:
    from src.som_gui.main_window import MainWindow


class AggregationScene(QGraphicsScene):
    def __init__(self):
        super(AggregationScene, self).__init__()

    def get_nodes(self):
        return set(node for node in self.items() if isinstance(node, NodeProxy))


class AggregationView(QGraphicsView):
    def __init__(self, parent: NodeProxy | GraphWindow) -> None:
        super(AggregationView, self).__init__()
        self.parent = parent
        self.selected_node: NodeProxy | None = None  # which Node is being resized
        self.resize_orientation: int | None = None  # which edge of Node is being resized
        self.last_pos: QPointF | None = None  # last mouse pos to calculate difference

    def item_under_mouse(self) -> set[QGraphicsItem]:
        items = set()
        for item in self.scene().items():
            if item.isUnderMouse():
                items.add(item)
        return items

    def scene(self) -> AggregationScene:  # for typing
        return super(AggregationView, self).scene()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(AggregationView, self).resizeEvent(event)
        if self.scene() is not None:
            self.scene().setSceneRect(self.contentsRect())
    @property
    def mouse_mode(self) -> int:
        """ 0=move,
            1=resize
            2 = drag
            """
        return self.main_view().mouse_mode

    @mouse_mode.setter
    def mouse_mode(self, value: int) -> None:
        self.main_view().mouse_mode = value

    def main_view(self) -> MainView | None:
        """views can be nested. This return the top View"""

        if isinstance(self, MainView):
            return self

        views = self.parent.scene().views()
        if len(views) <= 0:
            return None
        else:
            return views[0].main_view()

    def wheelEvent(self, event: QWheelEvent) -> None:

        """
        Resizes the MainView based on Scrollwheel and Keyboard Input
        :param event:
        :type event:
        :return:
        :rtype:
        """

        point = event.angleDelta() / 4
        val = point.y()

        modifier = QApplication.keyboardModifiers()

        if bool(modifier == Qt.ControlModifier):

            if val < 0:
                self.scale(1 - constants.SCALING_FACTOR, 1 - constants.SCALING_FACTOR)
            else:
                self.scale(1 + constants.SCALING_FACTOR, 1 + constants.SCALING_FACTOR)

        elif bool(modifier == Qt.ShiftModifier):
            hor = self.horizontalScrollBar()
            hor.setValue(hor.value() - val)

        else:
            ver = self.verticalScrollBar()
            ver.setValue(ver.value() - val)
        self.update()

    def viewport(self) -> QWidget:
        """views can be nested. This return the top Viewport"""
        if not isinstance(self, MainView):
            return self.main_view().viewport()

        return super(AggregationView, self).viewport()

    def cursor_over_header(self) -> bool:
        """checks if Cursor is over Header"""
        items = self.item_under_mouse()
        return bool([item for item in items if isinstance(item, Header)])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.cursor_over_header():
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.mouse_mode = 2

        self.last_pos = self.mapToScene(event.pos())
        if self.selected_node is None:
            super(AggregationView, self).mousePressEvent(event)
        else:
            self.mouse_mode = 1

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_mode = 0
        if self.cursor_over_header():
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        super(AggregationView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:

        if self.mouse_mode == 1 and self.selected_node is not None:  # resize selected Node
            old_pos = self.last_pos
            new_pos = self.mapToScene(event.pos())
            self.last_pos = new_pos
            self.selected_node: NodeProxy
            self.selected_node.resize_by_cursor(old_pos, new_pos, self.resize_orientation)
            return super(AggregationView, self).mouseMoveEvent(event)

        self.selected_node, self.resize_orientation = self.get_resize_node(event)
        self.set_cursor_by_border(self.resize_orientation)
        if not self.cursor_over_header():
            return super(AggregationView, self).mouseMoveEvent(event)
        if self.mouse_mode != 2:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return super(AggregationView, self).mouseMoveEvent(event)

    def get_resize_node(self, event) -> (NodeProxy | None, int | None):
        pos = self.mapToScene(event.pos())
        for proxy_node in self.scene().get_nodes():
            frame_value = self.cursor_on_border(pos, proxy_node)
            if frame_value != 0:
                return proxy_node, frame_value
        return None, None

    def setCursor(self, arg__1: QtGui.QCursor | QtCore.Qt.CursorShape | QtGui.QPixmap) -> None:
        if isinstance(arg__1, Qt.CursorShape):
            self.viewport().setCursor(arg__1)
        else:
            super(AggregationView, self).setCursor(arg__1)

    def unsetCursor(self) -> None:
        self.viewport().unsetCursor()

    def set_cursor_by_border(self, border: int):
        pos_dict = {
            1: Qt.CursorShape.SizeHorCursor,  # Left
            2: Qt.CursorShape.SizeHorCursor,  # right
            3: Qt.CursorShape.SizeVerCursor,  # Top
            6: Qt.CursorShape.SizeVerCursor,  # Bottom
            4: Qt.CursorShape.SizeFDiagCursor,  # TOP Left
            7: Qt.CursorShape.SizeBDiagCursor,  # Bottom Left
            5: Qt.CursorShape.SizeBDiagCursor,  # Top Right
            8: Qt.CursorShape.SizeFDiagCursor}  # Bottom Right
        if border == 0 or border is None:
            self.unsetCursor()
        else:
            self.setCursor(pos_dict[border])

    def cursor_on_border(self, pos, proxy: NodeProxy):
        """checks if Cursor is on border of Node and returns the Border orientation"""
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOTTOM = 6
        TOLERANCE = 5
        border = proxy.sceneBoundingRect()

        mouse_x = pos.x()
        mouse_y = pos.y()
        frame_x = border.x()
        frame_y = border.y()
        frame_height = border.height()
        frame_width = border.width()
        min_y = frame_y - TOLERANCE
        max_y = frame_y + TOLERANCE
        min_x = frame_x - TOLERANCE
        max_x = frame_x + TOLERANCE

        def check_vert():

            if min_y <= mouse_y <= max_y + frame_height:
                if min_x <= mouse_x <= max_x:
                    return LEFT
                elif min_x + frame_width <= mouse_x <= max_x + frame_width:
                    return RIGHT
            return 0

        def check_hor():
            if min_x <= mouse_x <= max_x + frame_width:
                if min_y <= mouse_y <= max_y:
                    return TOP
                elif min_y + frame_height <= mouse_y <= max_y + frame_height:
                    return BOTTOM
            return 0

        frame_pos = check_vert() + check_hor()
        return frame_pos


class MainView(AggregationView):
    def __init__(self, graph_window: GraphWindow) -> None:
        super(MainView, self).__init__(graph_window)
        self.graph_window = graph_window
        self.main_window = graph_window.main_window
        self._mouse_mode = 0  # 0=move, 1=resize, 2 = drag

    @property
    def mouse_mode(self) -> int:
        return self._mouse_mode

    @mouse_mode.setter
    def mouse_mode(self, value: int) -> None:
        self._mouse_mode = value


class GraphWindow(QWidget):

    def __init__(self, main_window: MainWindow, show=True) -> None:
        super(GraphWindow, self).__init__()
        self.main_window = main_window
        self.widget = ui_GraphWindow.Ui_GraphView()
        self.widget.setupUi(self)
        self.view = MainView(self)

        layout = self.widget.gridLayout
        layout.removeWidget(self.widget.graphicsView)
        layout.addWidget(self.view, 1, 0, 1, 4)
        self.widget.graphicsView.deleteLater()
        self.scenes = set()
        self.active_scene = AggregationScene()
        self.scenes.add(self.active_scene)
        self.view.setScene(self.active_scene)
        self.active_scene.setSceneRect(self.rect())
        self.widget.button_add.clicked.connect(self.test)
        self.nodes = set()

    def fit_in(self):
        pass

    def test(self):
        pos = QPointF(100.0, 100.0)
        self.nodes.add(NodeProxy(pos, self.active_scene, CollectorWidget))
        self.view.setMouseTracking(True)


class Header(QGraphicsRectItem):
    def __init__(self, node: NodeProxy, text, pos: QPointF):
        super(Header, self).__init__()
        self.node = node
        self.title = text
        self.setPos(pos)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(True)

    def resize(self):
        line_width = self.pen().width()  # if ignore Linewidth: box of Node and Header wont match
        x = line_width / 2
        width = self.node.widget().width() - line_width
        height = HEADER_HEIGHT
        self.setRect(QRectF(x, 0, width, height))

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
        self.setParentItem(node.header_rect)
        self.node = node
        self.resize()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)

    def resize(self):
        self.setRect(self.get_required_rect())

    def get_required_rect(self) -> QRectF:
        rect = self.node.rect()
        rect.setWidth(rect.width() - self.pen().width() / 2)
        rect.setY(rect.y())
        rect.setHeight(rect.height() + HEADER_HEIGHT)
        rect.setX(self.x() + self.pen().width() / 2)
        return rect


class NodeProxy(QGraphicsProxyWidget):
    def __init__(self, pos: QPointF, scene: QGraphicsScene, widget: Type[ObjectWidget] | Type[CollectorWidget]) -> None:
        def create_header():
            header = Header(self, "TESTBOX", pos)
            self.setParentItem(header)
            scene.addItem(header)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
            header.resize()
            self.setPos(0, HEADER_HEIGHT)  # put below Header
            return header

        super(NodeProxy, self).__init__()
        self.setWidget(widget(self))
        self.header_rect = create_header()
        self.frame = Frame(self)

    def setCursor(self, cursor) -> None:
        super(NodeProxy, self).setCursor(cursor)

    def sceneBoundingRect(self) -> QtCore.QRectF:
        rect = super(NodeProxy, self).sceneBoundingRect()
        rect.setY(rect.y() - HEADER_HEIGHT)
        return rect

    def resizeEvent(self, event: QGraphicsSceneResizeEvent) -> None:
        super(NodeProxy, self).resizeEvent(event)
        try:
            self.frame.resize()
        except AttributeError:
            pass

        try:
            self.header_rect.resize()
        except AttributeError:
            pass

    def resize_by_cursor(self, old_pos, new_pos, orientation):

        def resize_geometry(dx, dy):
            geometry = self.geometry()
            geometry.setWidth(geometry.width() + dx)
            geometry.setHeight(geometry.height() + dy)
            self.setGeometry(geometry)

        def resize_top(delta: float):
            self.header_rect.moveBy(0, -delta)
            resize_geometry(0, delta)

        def resize_left(delta: float):
            self.header_rect.moveBy(-delta, 0)
            resize_geometry(delta, 0)

        def resize_right(delta: float):
            resize_geometry(-delta, 0)

        def resize_bottom(delta: float):
            resize_geometry(0, -delta)

        delta = old_pos - new_pos

        if orientation in (3, 4, 5):
            resize_top(delta.y())

        if orientation in (1, 4, 7):
            resize_left(delta.x())

        if orientation in (2, 5, 8):
            resize_right(delta.x())

        if orientation in (6, 7, 8):
            resize_bottom(delta.y())

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        widget: NodeWidget = self.widget()
        widget.button.show()
        return super(NodeProxy, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        widget: NodeWidget = self.widget()
        widget.button.hide()
        super(NodeProxy, self).hoverLeaveEvent(event)


class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.button = QPushButton("PressMe")
        self.layout().addWidget(self.button)
        self.button.hide()

class CollectorWidget(NodeWidget):
    def __init__(self, parent):
        super(CollectorWidget, self).__init__()
        self.view = AggregationView(parent)
        self.layout().insertWidget(0, self.view)
        self.scene = AggregationScene()
        self.view.setScene(self.scene)
        self.nodes = set()

    def resizeEvent(self, event) -> None:
        super(CollectorWidget, self).resizeEvent(event)
        self.view.scene().setSceneRect(self.view.contentsRect())

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        super(CollectorWidget, self).enterEvent(event)
        self.view.scene().setSceneRect(self.view.contentsRect())


class ObjectWidget(NodeWidget):
    def __init__(self, parent):
        super(ObjectWidget, self).__init__()
        self.layout().insertWidget(0, QTreeWidget())
        self.parent = parent
        pass


FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2
