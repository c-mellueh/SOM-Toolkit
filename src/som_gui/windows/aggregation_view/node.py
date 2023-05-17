from __future__ import annotations  # make own class referencable
import logging
import random
from typing import Iterator, List,TYPE_CHECKING

from PySide6.QtCore import Qt, QRectF, QPointF,QPoint,QRect
from PySide6.QtGui import QWheelEvent, QPainterPath, QMouseEvent, QContextMenuEvent, QCursor, QColor,QPen,QImage,QPainter,QBrush
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout,\
    QApplication, QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsPathItem, QComboBox, QGraphicsRectItem, \
    QInputDialog, QMenu,QGraphicsItem, QGraphicsSceneMoveEvent,QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QTreeWidgetItem,QFileDialog,QFrame,QGraphicsTextItem
from PySide6.QtPrintSupport import  QPrintDialog
from SOMcreator import classes, constants
from src.som_gui import icons
from src.som_gui.qt_designs import ui_GraphWindow, ui_ObjectGraphWidget
from src.som_gui.widgets import property_widget
from src.som_gui.windows import popups
from src.som_gui.data.constants import HEADER_HEIGHT
class Header(QGraphicsRectItem):
    def __init__(self, node,text):
        super(Header, self).__init__()
        self.node = node
        self.title = text
        self.setPen(QPen(Qt.GlobalColor.black))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        super(Header, self).hoverEnterEvent(event)

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
        super(Header, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        super(Header, self).mouseReleaseEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.scene().views()[0].viewport().unsetCursor()
        super(Header, self).hoverLeaveEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print(event)

    def paint(self, painter: QPainter,option: QStyleOptionGraphicsItem, widget) -> None:
        painter.save()
        painter.restore()
        painter.drawText(self.boundingRect(),Qt.AlignmentFlag.AlignCenter,self.title)
        super().paint(painter, option, widget)

class Frame(QGraphicsRectItem):
    def __init__(self,node:NodeProxy):
        super(Frame, self).__init__()
        self.setPen(QPen(Qt.GlobalColor.red))

        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)

class NodeProxy(QGraphicsProxyWidget):
    def __init__(self,pos:QPointF,scene:QGraphicsScene) -> None:
        def create_box():
            self.setParentItem(self.frame)
            self.header_rect.setParentItem(self.frame)
            scene.addItem(self.frame)
            self.frame.show()
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
            self.header_rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)

            line_width = self.frame.pen().width() #if ignore Linewidth: box of Node and Header wont match
            x = line_width/2
            y = -HEADER_HEIGHT
            width =  self.widget().width()-line_width
            height = HEADER_HEIGHT+self.widget().height()
            self.frame.setRect(QRectF(x,y,width,height))
            self.header_rect.setRect(QRectF(x,y,width,height-self.widget().height()))

        super(NodeProxy, self).__init__()
        self.setWidget(NodeWidget())
        self.header_rect = Header(self, "TESTBOX")
        self.frame = Frame(self)

        create_box()
        #style
        self.setAcceptHoverEvents(False)
        #self.widget().setStyleSheet("background: white;border: 1px solid black")
        print(self.getContentsMargins())

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print("HIER")

class NodeWidget(QWidget):
    def __init__(self):
        super(NodeWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QTreeWidget())
        self.layout().addWidget(QPushButton("PressMe"))
        print(self.style())
        #self.setStyleSheet("border: 1px solid black")


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
            if self.free_cursor_on_side:
                print(self.graphicsProxyWidget().scene().views()[0].viewport().setCursor(Qt.CursorShape.OpenHandCursor))
            else:
                self.unsetCursor()
            self.update()
        else:
            self.applye_event(event)
            self.update()

    def mouseReleaseEvent(self, event):
        self.applye_event(event)
        self.state = FREE_STATE