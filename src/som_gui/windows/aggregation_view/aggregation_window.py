from __future__ import annotations  # make own class referencable
import logging
import random
from typing import Iterator, List,TYPE_CHECKING

from PySide6.QtCore import Qt, QRectF, QPointF,QPoint,QRect
from PySide6.QtGui import QWheelEvent, QPainterPath, QMouseEvent, QContextMenuEvent, QCursor, QColor,QPen,QImage,QPainter,QBrush
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QGraphicsScene, QGraphicsView, \
    QApplication, QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsPathItem, QComboBox, QGraphicsRectItem, \
    QInputDialog, QMenu, QGraphicsSceneMoveEvent, QGraphicsSceneHoverEvent, QTreeWidget, QTreeWidgetItem,QFileDialog,QFrame
from PySide6.QtPrintSupport import  QPrintDialog
from SOMcreator import classes, constants
from src.som_gui import icons
from src.som_gui.qt_designs import ui_GraphWindow, ui_ObjectGraphWidget
from src.som_gui.widgets import property_widget
from src.som_gui.windows import popups
from .node import NodeProxy,MyWidget,Frame

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

    def get_frames(self):
        return set(frame for frame in self.items() if isinstance(frame,Frame))

class MainView(QGraphicsView):
    def __init__(self, graph_window: GraphWindow) -> None:
        super(MainView, self).__init__()
        self.graph_window = graph_window
        self.main_window = graph_window.main_window

    def item_under_mouse(self):
        for item in self.scene().items():
            if item.isUnderMouse():
                return item

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
        super(MainView, self).mousePressEvent(event)
        item = self.itemAt(event.pos())

    def mouseMoveEvent(self, event) -> None:
        super(MainView, self).mouseMoveEvent(event)
        self.find_border(event.pos())
    def find_border(self,pos):
        pass


    # def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    #
    #     node:Node = self.item_under_mouse()
    #
    #     if isinstance(node, Node):
    #         menu = QMenu()
    #         action_delete = menu.addAction("delete")
    #         action_delete.triggered.connect(node.delete)
    #         action_toggle_con = menu.addAction("toggle Connection")
    #         action_toggle_con.triggered.connect(node.toggle_connection_to_parent)
    #         action_add_attribute = menu.addAction("add Attribute")
    #         action_add_attribute.triggered.connect(node.add_attribute)
    #
    #         if logging.DEBUG >= logging.root.level:
    #             action_info = menu.addAction("Info")
    #             action_info.triggered.connect(node.print_info)
    #
    #         menu.exec(event.globalPos())
    #
    #     else:
    #         menu = QMenu()
    #         action_print = menu.addAction("Print")
    #         action_print.triggered.connect(self.print)
    #         menu.exec(event.globalPos())
    #
    # def scene(self) -> AggregationScene | QGraphicsScene:
    #     return super(MainView, self).scene()

    def print(self):
        rect = self.viewport().rect()
        image = QImage(rect.size()*5,QImage.Format.Format_RGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter)
        file_text = "png Files (*.png);;"
        imagePath = QFileDialog.getSaveFileName(self, "Safe Aggregation", self.main_window.export_path, file_text)[0]
        image.save(imagePath)
        painter.end()
        print("Done")


class GraphWindow(QWidget):

    def __init__(self, main_window:MainWindow, show=True) -> None:
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
        self.widget.button_add.clicked.connect(self.test)

    def fit_in(self):
        pass

    def test(self):
        pos = QPointF(100.0,100.0)
        self.node = NodeProxy(pos,self.active_scene)
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