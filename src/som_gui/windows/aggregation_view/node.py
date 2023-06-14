from __future__ import annotations  # make own class referencable

from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPen, QPainter, QBrush
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsScene, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsRectItem,QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsTextItem

from src.som_gui.data.constants import HEADER_HEIGHT

MIN_SIZE = (200, 200)


class Header(QGraphicsRectItem):
    def __init__(self, node:NodeProxy, text, pos: QPointF):
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
    def __init__(self, pos: QPointF, scene: QGraphicsScene) -> None:
        def create_header():
            self.setParentItem(self.header_rect)
            scene.addItem(self.header_rect)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
            self.header_rect.resize()
            self.setPos(0, HEADER_HEIGHT)  # put under Header
            # self.title = Title(self.header_rect)

        super(NodeProxy, self).__init__()
        self.setWidget(NodeWidget())
        self.header_rect = Header(self, "TESTBOX", pos)
        create_header()
        self.frame = Frame(self)
        # style
        self.setAcceptHoverEvents(False)
        # self.widget().setStyleSheet("background: white;border: 1px solid black")


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

class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QTreeWidget())
        self.layout().addWidget(QPushButton("PressMe"))
        # self.setStyleSheet("border: 1px solid black")


FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)
        self.begin = QPoint()
        self.end = QPoint()

        self.state = FREE_STATE

        self.setMouseTracking(True)
        self.free_cursor_on_side = 0

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QRect(self.begin, self.end))

        if not self.free_cursor_on_side:
            return

        qp.setPen(QPen(Qt.black, 5, Qt.DashLine))
        if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE:
            end = QPoint(self.end)
            end.setX(self.begin.x())
            qp.drawLine(self.begin, end)

        elif self.free_cursor_on_side == CURSOR_ON_END_SIDE:
            begin = QPoint(self.begin)
            begin.setX(self.end.x())
            qp.drawLine(self.end, begin)

    def cursor_on_side(self, e_pos) -> int:
        if not self.begin.isNull() and not self.end.isNull():
            y1, y2 = sorted([self.begin.y(), self.end.y()])
            if y1 <= e_pos.y() <= y2:

                # 5 resolution, more easy to pick than 1px
                if abs(self.begin.x() - e_pos.x()) <= 5:
                    return CURSOR_ON_BEGIN_SIDE
                elif abs(self.end.x() - e_pos.x()) <= 5:
                    return CURSOR_ON_END_SIDE

        return 0

    def mousePressEvent(self, event):
        side = self.cursor_on_side(event.pos())
        if side == CURSOR_ON_BEGIN_SIDE:
            self.state = BEGIN_SIDE_EDIT
        elif side == CURSOR_ON_END_SIDE:
            self.state = END_SIDE_EDIT
        else:
            self.state = BUILDING_SQUARE

            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def applye_event(self, event):

        if self.state == BUILDING_SQUARE:
            self.end = event.pos()
        elif self.state == BEGIN_SIDE_EDIT:
            self.begin.setX(event.x())
        elif self.state == END_SIDE_EDIT:
            self.end.setX(event.x())

    def mouseMoveEvent(self, event):
        if self.state == FREE_STATE:
            self.free_cursor_on_side = self.cursor_on_side(event.pos())
            self.update()
        else:
            self.applye_event(event)
            self.update()

    def mouseReleaseEvent(self, event):
        self.applye_event(event)
        self.state = FREE_STATE
