from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QWheelEvent, QMouseEvent, QImage, QPainter
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, \
    QApplication, QFileDialog
from SOMcreator import constants

from src.som_gui.qt_designs import ui_GraphWindow
from .node import NodeProxy, Frame, Header

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


class MainView(QGraphicsView):
    def __init__(self, graph_window: GraphWindow) -> None:
        super(MainView, self).__init__()
        self.graph_window = graph_window
        self.main_window = graph_window.main_window

        self.resize_node:NodeProxy|None = None    #which Node is being resized
        self.resize_orientation:int|None = None   #which edge of Node is being resized
        self.mouse_mode = 0                       # 0=move, 1=resize, 2 = drag
        self.last_pos:QPointF|None = None         #last mouse pos to calculate difference

    def item_under_mouse(self):
        for item in self.scene().items():
            if item.isUnderMouse():
                return item

    def scene(self) -> AggregationScene:
        return super(MainView, self).scene()

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
        self.last_pos = self.mapToScene(event.pos())
        if self.resize_node is None:
            super(MainView, self).mousePressEvent(event)
        else:
            self.mouse_mode = 1
            print("resize")

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        self.mouse_mode = 0
        super(MainView, self).mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        super(MainView, self).mouseMoveEvent(event)
        if self.mouse_mode != 1:
            self.resize_node,self.resize_orientation = self.find_border(event)
        else:

            old_pos = self.last_pos
            new_pos = self.mapToScene(event.pos())
            self.last_pos = new_pos
            delta = old_pos-new_pos

            if self.resize_orientation in (3,4,5):
                self.resize_node.resize_top(delta.y())

            if self.resize_orientation in (1,4,7):
                self.resize_node.resize_left(delta.x())

            if self.resize_orientation in (2,5,8):
                self.resize_node.resize_right(delta.x())

            if self.resize_orientation in (6,7,8):
                self.resize_node.resize_bottom(delta.y())

    def find_border(self, event:QMouseEvent) ->(NodeProxy|None,int|None) :
        pos = self.mapToScene(event.pos())
        old_cursor = self.viewport().cursor()
        pos_dict = {
            1: Qt.CursorShape.SizeHorCursor,    #Left
            2: Qt.CursorShape.SizeHorCursor,    #right
            3: Qt.CursorShape.SizeVerCursor,    #Top
            6: Qt.CursorShape.SizeVerCursor,    #Bottom
            4: Qt.CursorShape.SizeFDiagCursor,  #TOP Left
            7: Qt.CursorShape.SizeBDiagCursor,  #Bottom Left
            5: Qt.CursorShape.SizeBDiagCursor,  #Top Right
            8: Qt.CursorShape.SizeFDiagCursor}  #Bottom Right

        for frame in self.scene().get_frames():
            frame_value = frame.is_on_frame(pos)
            if frame_value != 0:
                self.viewport().setCursor(pos_dict[frame_value])
                return frame.node, frame_value
        if isinstance(self.item_under_mouse(),Header):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
            else:
                self.viewport().setCursor(Qt.CursorShape.OpenHandCursor)
            return None,None
        self.viewport().unsetCursor()
        return None,None

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
        self.nodes.add(NodeProxy(pos, self.active_scene))
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
