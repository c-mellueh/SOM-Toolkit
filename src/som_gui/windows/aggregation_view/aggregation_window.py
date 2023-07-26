from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView
from SOMcreator import classes

from src.som_gui.qt_designs import ui_GraphWindow
from .node import NodeProxy, Header, Frame, Connection
from ...data import constants
if TYPE_CHECKING:
    from src.som_gui.main_window import MainWindow

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




class AggregationScene(QGraphicsScene):
    def __init__(self, aggregation_window: GraphWindow, name="UNDEF"):
        super(AggregationScene, self).__init__()
        self.node_pos = QPointF(50, 50)
        self._name = name
        self.aggregation_window = aggregation_window
        self.setSceneRect(1, 1, 10_000, 10_000)

    def get_items_bounding_rect(self) -> QRectF:
        b_min = [None, None]
        b_max = [None, None]
        for item in self.items():
            if not item.isVisible():
                continue
            rect = item.sceneBoundingRect()
            x_min = rect.x()
            x_max = x_min + rect.width()
            y_min = rect.y()
            y_max = y_min + rect.height()
            r_min = [x_min, y_min]
            r_max = [x_max, y_max]

            for index, (extreme, value) in enumerate(zip(b_min, r_min)):
                if extreme is None or value < extreme:
                    b_min[index] = value

            for index, (extreme, value) in enumerate(zip(b_max, r_max)):
                if extreme is None or value > extreme:
                    b_max[index] = value

        if None in b_max or None in b_min:
            return QRectF(0, 0, 0, 0)

        b1 = QPointF(b_min[0] - constants.SCENE_MARGIN, b_min[1] - constants.SCENE_MARGIN)
        b2 = QPointF(b_max[0]
                     + constants.SCENE_MARGIN, b_max[1] + constants.SCENE_MARGIN)

        return QRectF(b1, b2)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        old_name = self._name
        values = self.aggregation_window.scene_dict[old_name]
        self.aggregation_window.scene_dict[new_name] = values
        self.aggregation_window.scene_dict.pop(old_name)
        self._name = new_name

    @property
    def nodes(self) -> set[NodeProxy]:
        return set(node for node in self.items() if isinstance(node, NodeProxy))

    def add_node(self, node_proxy: NodeProxy, recursive=False):
        node_proxy.setZValue(self.max_z_value() + 1)
        self.addItem(node_proxy)

        node_proxy.show()
        self.aggregation_window.scene_dict[self.name][constants.NODES].add(node_proxy.aggregation.uuid)
        if recursive:
            uuid_dict = {node.aggregation.uuid: node for node in self.aggregation_window.nodes}
            child: classes.Aggregation
            for child in node_proxy.aggregation.children:
                child_node = uuid_dict.get(child.uuid)
                self.add_node(child_node, recursive=True)

    def remove_node(self, node_proxy: NodeProxy):
        self.removeItem(node_proxy)
        self.aggregation_window.scene_dict[self.name][constants.NODES].pop(node_proxy.aggregation.uuid)
        node_proxy.delete()

    def max_z_value(self):
        return max((item.zValue() for item in self.items()), default=0)

    def fill_connections(self):
        node_dict = {node.aggregation:node for node in self.nodes}
        for node in self.nodes:
            aggregation = node.aggregation
            sub_elements = aggregation.children
            top_aggregation = aggregation.parent or None

            for sub_aggregation in sub_elements:
                sub_node = node_dict[sub_aggregation]
                self.add_connection(node,sub_node)

            if top_aggregation is not None:
                top_node = node_dict[top_aggregation]
                self.add_connection(top_node,node)

    def add_connection(self,top_node:NodeProxy,bottom_node:NodeProxy):
        con = Connection(bottom_node,top_node)

class AggregationView(QGraphicsView):
    def __init__(self) -> None:
        super(AggregationView, self).__init__()
        self.focus_node: NodeProxy | None = None  # which Node is being resized
        self.resize_orientation: int | None = None  # which edge of Node is being resized
        self.last_pos: QPointF | None = None  # last mouse pos to calculate difference
        self.mouse_mode = 0  # 0=moveCursor 1=resize 2 = drag
        self.mouse_is_pressed = False
        self.setDragMode(self.DragMode.ScrollHandDrag)

    def items_under_mouse(self) -> set[QGraphicsItem]:
        return set(item for item in self.scene().items() if item.isUnderMouse())

    def scene(self) -> AggregationScene:  # for typing
        return super(AggregationView, self).scene()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(AggregationView, self).resizeEvent(event)

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
        frames = [node.frame for node in self.scene().nodes if self.cursor_on_border(pos, node) != 0]
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
        self.last_pos = None
        super(AggregationView, self).mouseReleaseEvent(event)

    def cursor(self) -> QtGui.QCursor:
        return self.viewport().cursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mouse_mode == 0:
            cursor_style, focus_node = self.get_focus_and_cursor(self.mapToScene(event.pos()))
            if cursor_style == 0:
                self.setDragMode(self.DragMode.ScrollHandDrag)
                self.unsetCursor()
            else:
                self.setDragMode(self.DragMode.NoDrag)
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
        self.widget.gridLayout.removeWidget(self.widget.graphicsView)
        self.widget.gridLayout.addWidget(self.view, 1, 0, 1, 4)
        self.widget.graphicsView.deleteLater()
        self.scenes: set[AggregationScene] = set()
        self._proxy_nodes = set()
        self.scene_dict = {}  # used for import and export

        self._active_scene = None
        self.widget.button_add.clicked.connect(self.test)
        self.widget.combo_box.currentTextChanged.connect(self.combo_box_changed)

    @property
    def nodes(self) -> set[NodeProxy]:
        return self._proxy_nodes

    def test(self):
        scene = self.active_scene
        scene.setSceneRect(1, 1, 10_000, 10_000)
        bbox = self.view.scene().get_items_bounding_rect()
        self.view.fitInView(bbox, aspectRadioMode=Qt.AspectRatioMode.KeepAspectRatio)

    def create_missing_scenes(self):
        scene_dict = self.scene_dict
        node_dict = {node.uuid: node for node in self.nodes}
        for name, uuid_dict in scene_dict.items():
            uuid_nodes = uuid_dict.get(constants.NODES)
            for uuid in uuid_nodes:
                node_dict.pop(uuid)

        remaining_nodes: set[NodeProxy] = node_dict.values()
        root_nodes = set(node for node in remaining_nodes if node.aggregation.is_root)
        for node in sorted(root_nodes, key=lambda x: x.name):
            scene = self.create_new_scene(node.aggregation.name)
            scene.add_node(node, recursive=True)
            scene.fill_connections()

    def show(self) -> None:
        if not (self.widget.combo_box.count() == 0 and len(self.nodes) > 0):
            return super(GraphWindow, self).show()

        self.create_missing_scenes()
        super(GraphWindow, self).show()
        self.fit_view()

    def create_new_scene(self, name="UNDEF") -> AggregationScene:
        scene = AggregationScene(self, name)
        self.scenes.add(scene)
        self.scene_dict[scene.name] = {constants.NODES: set()}
        self.widget.combo_box.addItem(scene.name)
        self.widget.combo_box.model().sort(0)
        return scene

    def create_node(self, aggregation: classes.Aggregation, pos: QPointF, scene: AggregationScene = None) -> NodeProxy:
        node = NodeProxy(aggregation, pos)
        self._proxy_nodes.add(node)
        if scene is not None:
            scene.add_node(node)

    def combo_box_changed(self):
        scene = {scene.name: scene for scene in self.scenes}.get(self.widget.combo_box.currentText())
        self.active_scene = scene
        self.fit_view()

    def fit_view(self):
        bounding_rect = self.active_scene.get_items_bounding_rect()
        sr_center = self.active_scene.sceneRect().center()
        br_center = bounding_rect.center()
        dif = sr_center - br_center
        for item in self.active_scene.items():
            if isinstance(item, (Frame, Header)):
                continue
            item.moveBy(dif.x(), dif.y())
        self.view.fitInView(self.active_scene.get_items_bounding_rect(),
                            aspectRadioMode=Qt.AspectRatioMode.KeepAspectRatio)

    @property
    def active_scene(self) -> AggregationScene:
        return self._active_scene

    @active_scene.setter
    def active_scene(self, value: AggregationScene) -> None:
        self._active_scene = value
        self.view.setScene(self.active_scene)
