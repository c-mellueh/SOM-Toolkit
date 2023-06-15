from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QWheelEvent, QMouseEvent, QImage, QPainter
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, \
    QApplication, QFileDialog
from SOMcreator import constants
from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPen, QPainter, QBrush
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsScene, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsTextItem,QGraphicsView

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

    def get_frames(self) -> set[Frame]:
        return set(frame for frame in self.items() if isinstance(frame, Frame))

class AggregationView(QGraphicsView):
    def __init__(self,parent) -> None:
        super(AggregationView, self).__init__()
        self.parent = parent
        self.resize_node: NodeProxy | None = None  # which Node is being resized
        self.resize_orientation: int | None = None  # which edge of Node is being resized
        self.mouse_mode = 0  # 0=move, 1=resize, 2 = drag
        self.last_pos: QPointF | None = None  # last mouse pos to calculate difference

    def item_under_mouse(self):
        for item in self.scene().items():
            if item.isUnderMouse():
                return item

    def scene(self) -> AggregationScene:
        return super(AggregationView, self).scene()

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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print("PRESS")
        self.last_pos = self.mapToScene(event.pos())
        if self.resize_node is None:
            super(AggregationView, self).mousePressEvent(event)
        else:
            self.mouse_mode = 1

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_mode = 0
        super(AggregationView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super(AggregationView, self).mouseMoveEvent(event)
        if self.mouse_mode != 1:
            self.resize_node, self.resize_orientation = self.find_border(event)
        else:

            old_pos = self.last_pos
            new_pos = self.mapToScene(event.pos())
            self.last_pos = new_pos
            delta = old_pos - new_pos

            if self.resize_orientation in (3, 4, 5):
                self.resize_node.resize_top(delta.y())

            if self.resize_orientation in (1, 4, 7):
                self.resize_node.resize_left(delta.x())

            if self.resize_orientation in (2, 5, 8):
                self.resize_node.resize_right(delta.x())

            if self.resize_orientation in (6, 7, 8):
                self.resize_node.resize_bottom(delta.y())

    def find_border(self, event: QMouseEvent) -> (NodeProxy | None, int | None):
        pos = self.mapToScene(event.pos())
        old_cursor = self.viewport().cursor()
        pos_dict = {
            1: Qt.CursorShape.SizeHorCursor,  # Left
            2: Qt.CursorShape.SizeHorCursor,  # right
            3: Qt.CursorShape.SizeVerCursor,  # Top
            6: Qt.CursorShape.SizeVerCursor,  # Bottom
            4: Qt.CursorShape.SizeFDiagCursor,  # TOP Left
            7: Qt.CursorShape.SizeBDiagCursor,  # Bottom Left
            5: Qt.CursorShape.SizeBDiagCursor,  # Top Right
            8: Qt.CursorShape.SizeFDiagCursor}  # Bottom Right

        for frame in self.scene().get_frames():
            frame_value = frame.is_on_frame(pos)
            if frame_value != 0:
                self.viewport().setCursor(pos_dict[frame_value])
                return frame.node, frame_value
        if isinstance(self.item_under_mouse(), Header):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
            else:
                self.viewport().setCursor(Qt.CursorShape.OpenHandCursor)
            return None, None
        self.viewport().unsetCursor()
        return None, None

    def print(self):
        rect = self.viewport().rect()
        image = QImage(rect.size() * 5, QImage.Format.Format_RGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter)
        file_text = "png Files (*.png);;"
        imagePath = QFileDialog.getSaveFileName(self, "Safe Aggregation", self.main_window.export_path, file_text)[0]
        image.save(imagePath)
        painter.end()
        print("Done")

class MainView(AggregationView):
    def __init__(self, graph_window: GraphWindow) -> None:
        super(MainView, self).__init__(graph_window)
        self.graph_window = graph_window
        self.main_window = graph_window.main_window

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
        self.nodes.add(NodeProxy(pos, self.active_scene,CollectorWidget))
        self.view.setMouseTracking(True)
        print(self.active_scene.get_frames())
        # self.node = Node()
        # self.node.setPos(pos)
        # self.re = self.scene.addRect(pos.x(),pos.y(),self.node.widget().width()-2,20,QPen(Qt.black),QBrush(Qt.darkGreen))
        #
        # self.re.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable,True)
        # self.re.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable,True)
        # self.node.setParentItem(self.re)
        # self.re.setZValue(1)
        # self.node.setZValue(-1)

MIN_SIZE = (200, 200)


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

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        super(Header, self).hoverEnterEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
        super(Header, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        super(Header, self).mouseReleaseEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.scene().views()[0].viewport().unsetCursor()
        super(Header, self).hoverLeaveEvent(event)

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

    def is_on_frame(self, pos):
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOTTOM = 6
        TOLERANCE = 5

        mouse_x = pos.x()
        mouse_y = pos.y()
        frame_x = self.scenePos().x()
        frame_y = self.scenePos().y()
        frame_height = self.rect().height()
        frame_width = self.rect().width()
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


class Title(QGraphicsTextItem):
    def __init__(self, header: Header):
        super(Title, self).__init__()
        self.setTextWidth(header.rect().width())
        self.setPlainText("Test123")
        self.setParentItem(header)


class NodeProxy(QGraphicsProxyWidget):
    def __init__(self, pos: QPointF, scene: QGraphicsScene,widget:ObjectWidget|CollectorWidget) -> None:
        def create_header():
            self.setParentItem(self.header_rect)
            scene.addItem(self.header_rect)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
            self.header_rect.resize()
            self.setPos(0, HEADER_HEIGHT)  # put under Header

        super(NodeProxy, self).__init__()
        self.setWidget(widget(self))
        self.header_rect = Header(self, "TESTBOX", pos)
        create_header()
        self.frame = Frame(self)
        self.setAcceptHoverEvents(True)

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

    def resize_geometry(self, dx, dy):
        geometry = self.geometry()
        geometry.setWidth(geometry.width() + dx)
        geometry.setHeight(geometry.height() + dy)
        self.setGeometry(geometry)

    def resize_top(self, delta: float):
        self.header_rect.moveBy(0, -delta)
        self.resize_geometry(0, delta)

    def resize_left(self, delta: float):
        self.header_rect.moveBy(-delta, 0)
        self.resize_geometry(delta, 0)

    def resize_right(self, delta: float):
        self.resize_geometry(-delta, 0)

    def resize_bottom(self, delta: float):
        self.resize_geometry(0, -delta)


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super(NodeProxy, self).hoverEnterEvent(event)
        widget:NodeWidget = self.widget()
        widget.button.show()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        super(NodeProxy, self).hoverLeaveEvent(event)
        widget:NodeWidget = self.widget()
        widget.button.hide()

class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.button = QPushButton("PressMe")
        self.layout().addWidget(self.button)
        self.button.hide()

class CollectorWidget(NodeWidget):
    def __init__(self,parent):
        super(CollectorWidget, self).__init__()
        self.view = AggregationView(parent)
        self.layout().insertWidget(0,self.view)
        self.view.setScene(AggregationScene())


class ObjectWidget(NodeWidget):
    def __init__(self):
        super(ObjectWidget, self).__init__()
        self.layout().insertWidget(0,QTreeWidget())
        pass

FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2
