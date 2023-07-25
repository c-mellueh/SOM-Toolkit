from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsScene, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsView
from SOMcreator import constants, classes

from src.som_gui.data.constants import HEADER_HEIGHT
from src.som_gui.qt_designs import ui_GraphWindow

LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 6
TOLERANCE = 5

CURSOR_DICT = {
    1: Qt.CursorShape.SizeHorCursor,  # Left
    2: Qt.CursorShape.SizeHorCursor,  # right
    3: Qt.CursorShape.SizeVerCursor,  # Top
    6: Qt.CursorShape.SizeVerCursor,  # Bottom
    4: Qt.CursorShape.SizeFDiagCursor,  # TOP Left
    7: Qt.CursorShape.SizeBDiagCursor,  # Bottom Left
    5: Qt.CursorShape.SizeBDiagCursor,  # Top Right
    8: Qt.CursorShape.SizeFDiagCursor,  # Bottom Right
    9: Qt.CursorShape.OpenHandCursor,
    10: Qt.CursorShape.ClosedHandCursor
}

if TYPE_CHECKING:
    from src.som_gui.main_window import MainWindow


class AggregationScene(QGraphicsScene):
    def __init__(self):
        super(AggregationScene, self).__init__()
        self.node_pos = QPointF(0, 0)

    def get_nodes(self):
        return set(node for node in self.items() if isinstance(node, NodeProxy))

    def add_aggregation(self, aggregation: classes.Aggregation, point: QPointF):
        node_proxy = NodeProxy(aggregation, point, self)
        node_proxy.setZValue(self.max_z_value() + 1)

        for child in aggregation.children:
            self.node_pos = self.node_pos + QPointF(30, 30)
            self.add_aggregation(child, self.node_pos)

    def max_z_value(self):
        return max((item.zValue() for item in self.items()), default=0)


class AggregationView(QGraphicsView):
    def __init__(self) -> None:
        super(AggregationView, self).__init__()
        self.focus_node: NodeProxy | None = None  # which Node is being resized
        self.resize_orientation: int | None = None  # which edge of Node is being resized
        self.last_pos: QPointF | None = None  # last mouse pos to calculate difference
        self.mouse_mode = 0  # 0=moveCursor 1=resize 2 = drag
        self.mouse_is_pressed = False

    def items_under_mouse(self) -> set[QGraphicsItem]:
        return set(item for item in self.scene().items() if item.isUnderMouse())

    def scene(self) -> AggregationScene:  # for typing
        return super(AggregationView, self).scene()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(AggregationView, self).resizeEvent(event)
        if self.scene() is not None:
            self.scene().setSceneRect(self.contentsRect())

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

    def get_focus_and_cursor(self, pos: QPointF):
        """return cursor style and Node that will be in focus"""
        frames = [node.frame for node in self.scene().get_nodes() if self.cursor_on_border(pos, node) != 0]
        headers = [item for item in self.items_under_mouse() if isinstance(item, Header)]

        frames.sort(key=lambda x: x.zValue())
        headers.sort(key=lambda x: x.zValue())

        max_frame = max({frame.zValue() for frame in frames}, default=0)
        max_header = max({header.zValue() for header in headers}, default=0)

        if not (frames or headers):
            cursor_style = 0
            node = None

        elif max_header >= max_frame:
            header = sorted(headers, key=lambda x: x.zValue())[-1]
            node = header.node
            if self.mouse_is_pressed:
                cursor_style = 10
            else:
                cursor_style = 9

        else:
            frame: Frame = sorted(frames, key=lambda x: x.zValue())[-1]
            node = frame.node
            cursor_style = self.cursor_on_border(pos, node)

        return cursor_style, node

    def cursor_over_header(self) -> bool:
        """checks if Cursor is over Header"""
        items = self.items_under_mouse()
        frames = [item.node.zValue() for item in items if isinstance(item, Frame)]
        header = [item.node.zValue() for item in items if isinstance(item, Header)]
        return max(header, default=0) == max(frames, default=1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_is_pressed = True
        self.resize_orientation, self.focus_node = self.get_focus_and_cursor(self.mapToScene(event.pos()))

        if self.resize_orientation == 0:
            self.unsetCursor()

        elif self.resize_orientation == 10:
            self.mouse_mode = 2
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

        else:
            self.setCursor(CURSOR_DICT[self.resize_orientation])
            self.mouse_mode = 1

        super(AggregationView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_is_pressed = False
        self.mouse_mode = 0
        if self.cursor_over_header():
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.last_pos = None
        super(AggregationView, self).mouseReleaseEvent(event)

    def cursor(self) -> QtGui.QCursor:
        return self.viewport().cursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mouse_mode == 0:
            cursor_style, focus_node = self.get_focus_and_cursor(self.mapToScene(event.pos()))
            if cursor_style == 0:
                self.unsetCursor()
            else:
                self.setCursor(CURSOR_DICT[cursor_style])

        elif self.mouse_mode == 1:
            old_pos = self.last_pos
            new_pos = self.mapToScene(event.pos())
            if old_pos is None:
                old_pos = new_pos
            self.last_pos = new_pos
            self.focus_node.resize_by_cursor(old_pos, new_pos, self.resize_orientation)

        elif self.mouse_mode == 2:
            new_pos = self.mapToScene(event.pos())

            old_pos = self.last_pos or new_pos
            self.last_pos = new_pos
            delta = new_pos - old_pos
            dx = delta.x()
            dy = delta.y()
            self.focus_node.moveBy(delta.x(), delta.y())

        return super(AggregationView, self).mouseMoveEvent(event)

    def cursor_on_border(self, pos, proxy: NodeProxy):
        """checks if Cursor is on border of Node and returns the Border orientation"""

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

    def setCursor(self, arg__1: QtGui.QCursor | QtCore.Qt.CursorShape | QtGui.QPixmap) -> None:
        """the Viewport is handling the Cursor if you call setCursor as is nothing will be changing"""
        if isinstance(arg__1, Qt.CursorShape):
            self.viewport().setCursor(arg__1)
        else:
            super(AggregationView, self).setCursor(arg__1)

    def unsetCursor(self) -> None:
        self.viewport().unsetCursor()

    def set_cursor_by_int(self, border: int):
        if border == 0 or border is None:
            self.unsetCursor()
        else:
            self.setCursor(CURSOR_DICT[border])


class GraphWindow(QWidget):

    def __init__(self, main_window: MainWindow) -> None:
        super(GraphWindow, self).__init__()
        self.main_window = main_window
        self.widget = ui_GraphWindow.Ui_GraphView()
        self.widget.setupUi(self)
        self.view = AggregationView()

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

    def test(self):
        self.build_nodes()

    def build_nodes(self):
        project = self.main_window.project
        aggregations = set()
        for obj in project.objects:
            aggregations = aggregations.union(obj.aggregation_representations)

        root_aggregations: list[classes.Aggregation] = list(filter(lambda x: x.is_root, aggregations))
        root_aggregations.sort(key=lambda x: x.name)
        root_aggregation = root_aggregations[12]
        self.active_scene.add_aggregation(root_aggregation, QPointF(0, 0))


class Header(QGraphicsRectItem):
    def __init__(self, node: NodeProxy, text, pos: QPointF):
        super(Header, self).__init__()
        self.node = node
        self.title = text
        self.setPos(pos)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(True)

    def resize(self):
        line_width = self.pen().width()  # if ignore Linewidth: box of Node and Header won't match
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

    def __init__(self, aggregation: classes.Aggregation, pos: QPointF, scene: QGraphicsScene) -> None:

        def create_header():
            name = f"{aggregation.name} ({aggregation.object.ident_value})"
            header = Header(self, name, pos)

            self.setParentItem(header)
            scene.addItem(header)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
            header.resize()
            self.setPos(0, HEADER_HEIGHT)  # put below Header
            return header

        super(NodeProxy, self).__init__()
        self.aggregation = aggregation
        self.setWidget(NodeWidget())
        self.header_rect = create_header()
        self.frame = Frame(self)

    def moveBy(self, dx: float, dy: float) -> None:
        self.header_rect.moveBy(dx, dy)

    def __str__(self):
        return f"{self.aggregation.name}"

    def setZValue(self, z: float) -> None:
        super(NodeProxy, self).setZValue(z)
        self.frame.setZValue(z)
        self.header_rect.setZValue(z)

    def setCursor(self, cursor) -> None:
        self.scene().views()[0].viewport().setCursor(cursor)

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

        def resize_top(d: float):
            self.header_rect.moveBy(0, -d)
            resize_geometry(0, d)

        def resize_left(d: float):
            self.header_rect.moveBy(-d, 0)
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

    def cursor(self) -> QtGui.QCursor:
        return self.scene().views()[0].viewport().cursor()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.widget().button.show()
        super(NodeProxy, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.widget().button.hide()
        super(NodeProxy, self).hoverEnterEvent(event)

    def hoverMoveEvent(self, event) -> None:
        pass  # hoverMove fucks with CursorStyle


class TestWidget(QTreeWidget):
    def __init__(self):
        super(TestWidget, self).__init__()

    def setCursor(self, arg__1) -> None:
        return

    def unsetCursor(self) -> None:
        return


class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.button = QPushButton("PressMe")
        self.layout().addWidget(self.button)
        self.button.hide()
        self.tree_widget = TestWidget()
        self.layout().insertWidget(0, self.tree_widget)
