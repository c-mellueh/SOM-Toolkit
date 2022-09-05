from __future__ import annotations  # make own class referencable

from typing import Iterator, List,Set

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import  QWheelEvent, QPainterPath, QMouseEvent,QContextMenuEvent,QCursor,QColor,QPen
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QGraphicsScene, QGraphicsView, \
    QApplication, QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsPathItem, QComboBox, QGraphicsRectItem, \
    QInputDialog,QMenu,QGraphicsSceneMoveEvent

from desiteRuleCreator import icons
from desiteRuleCreator.QtDesigns import ui_GraphWindow, ui_ObjectGraphWidget
from desiteRuleCreator.Widgets import property_widget
from desiteRuleCreator.data import classes, constants
from desiteRuleCreator.Windows import popups
import logging

def item_to_name(item : Node | classes.Object) -> str:
    obj = None
    if item is None:
        return "Root"
    elif isinstance(item,classes.Object):
        obj = item
    elif isinstance(item,Node):
        obj = item.object
    if obj.is_concept:
        text = f"{obj.name}"
    else:
        text = f"{obj.name} ({obj.ident_attrib.value[0]})"
    return text

## Create Tree Positions
def buchheim(tree):
    def third_walk(tree, n):
        tree.x += n
        for c in tree.children:
            third_walk(c, n)

    def firstwalk(v, distance=1.):
        if len(v.children) == 0:
            if v.lmost_sibling:
                v.x = v.lbrother().x + distance
            else:
                v.x = 0.
        else:
            default_ancestor = v.children[0]
            for w in v.children:
                firstwalk(w)
                default_ancestor = apportion(w, default_ancestor, distance)
            execute_shifts(v)

            midpoint = (v.children[0].x + v.children[-1].x) / 2

            ell = v.children[0]
            arr = v.children[-1]
            w = v.lbrother()
            if w:
                v.x = w.x + distance
                v.mod = v.x - midpoint
            else:
                v.x = midpoint
        return v

    def apportion(v, default_ancestor, distance):
        w = v.lbrother()
        if w is not None:
            # in buchheim notation:
            # i == inner; o == outer; r == right; l == left; r = +; l = -
            vir = vor = v
            vil = w
            vol = v.lmost_sibling
            sir = sor = v.mod
            sil = vil.mod
            sol = vol.mod
            while vil.right() and vir.left():
                vil = vil.right()
                vir = vir.left()
                vol = vol.left()
                vor = vor.right()
                vor.ancestor = v
                shift = (vil.x + sil) - (vir.x + sir) + distance
                if shift > 0:
                    move_subtree(ancestor(vil, v, default_ancestor), v, shift)
                    sir = sir + shift
                    sor = sor + shift
                sil += vil.mod
                sir += vir.mod
                sol += vol.mod
                sor += vor.mod
            if vil.right() and not vor.right():
                vor.thread = vil.right()
                vor.mod += sil - sor
            else:
                if vir.left() and not vol.left():
                    vol.thread = vir.left()
                    vol.mod += sir - sol
                default_ancestor = v
        return default_ancestor

    def move_subtree(wl, wr, shift):
        subtrees = wr.number - wl.number
        wr.change -= shift / subtrees
        wr.shift += shift
        wl.change += shift / subtrees
        wr.x += shift
        wr.mod += shift

    def execute_shifts(v):
        shift = change = 0
        for w in v.children[::-1]:
            w.x += shift
            w.mod += shift
            change += w.change
            shift += w.shift + change

    def ancestor(vil, v, default_ancestor):
        # the relevant text is at the bottom of page 7 of
        # "Improving Walker's Algorithm to Run in Linear Time" by Buchheim et al, (2002)
        # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.16.8757&rep=rep1&type=pdf
        if vil.ancestor in v.parent.children:
            return vil.ancestor
        else:
            return default_ancestor

    def second_walk(v, m=0, depth=0, min=None):
        v.x += m
        v.y = depth

        if min is None or v.x < min:
            min = v.x

        for w in v.children:
            min = second_walk(w, m + v.mod, depth + 1, min)

        return min

    dt = firstwalk(DrawTree(tree))
    min = second_walk(dt)
    if min < 0:
        third_walk(dt, -min)
    return dt


class DrawTree(object):
    _registry = list()

    def __init__(self, tree, parent=None, depth=0, number=1):
        self.x = -1.
        self.y = depth
        self.tree = tree
        self.children = [DrawTree(c, self, depth + 1, i + 1) for i, c in enumerate(tree.children)]
        self.parent = parent
        self.thread = None
        self.mod = 0
        self.ancestor = self
        self.change = self.shift = 0
        self._lmost_sibling = None
        self._registry.append(self)
        # this is the number of the node in its group of siblings 1..n
        self.number = number

    def left(self):
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

    def lbrother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

    @property
    def lmost_sibling(self):
        if not self._lmost_sibling and self.parent and self != \
                self.parent.children[0]:
            self._lmost_sibling = self.parent.children[0]
        return self._lmost_sibling

    def __str__(self):
        return f"DrawTree x={self.x}, mod={self.mod}"

    def __repr__(self):
        return self.__str__()


class MainView(QGraphicsView):
    def __init__(self,graph_window:GraphWindow) -> None:
        super(MainView, self).__init__()
        self.setDragMode(self.DragMode.ScrollHandDrag)
        self.graph_window = graph_window

    def item_under_mouse(self) -> Node:
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

    def mousePressEvent(self, event:QMouseEvent) -> None:
        super(MainView, self).mousePressEvent(event)
        popup = self.graph_window.node_popup
        item = self.itemAt(event.pos())

        if popup is not None:
            if item is not None:
                item_parent = item.parentWidget()
                proxy = popup.graphicsProxyWidget()
                if not (item == proxy or item_parent == proxy):
                    self.graph_window.active_scene.removeItem(popup.proxy)
            else:
                self.graph_window.active_scene.removeItem(popup.proxy)

    def contextMenuEvent(self, event:QContextMenuEvent) -> None:

        node = self.item_under_mouse()

        if isinstance(node,Node):
            menu = QMenu()
            action_delete = menu.addAction("delete")
            action_delete.triggered.connect(node.delete_clicked)

            if logging.DEBUG >= logging.root.level:
                action_delete = menu.addAction("Info")
                action_delete.triggered.connect(node.print_info)


            menu.exec(event.globalPos())

class AggregationScene(QGraphicsScene):
    def __init__(self, root_node) -> None:
        super(AggregationScene, self).__init__()
        self.title = item_to_name(root_node)
        self._root_node = root_node
        self.add_node(root_node)

    def add_node(self,node:Node)-> None:
        self.addItem(node)
        self.addItem(node.rect)

    def remove_node(self,node:Node)->None:
        self.removeItem(node)
        for connection in node.top_connections:
            self.removeItem(connection)
            connection.top_node.connections.remove(connection)

    def __str__(self) -> str:
        return str(self.root_node)

    @property
    def root_node(self) -> Node:
        return self._root_node

    @property
    def nodes(self) -> list[Node]:
        return [item for item in self.items() if isinstance(item,Node)]

class Connection(QGraphicsPathItem):

    def __init__(self, bottom_node, top_node) -> None:
        super(Connection, self).__init__()
        self.bottom_node: Node = bottom_node
        self.top_node: Node = top_node

        self.setZValue(0)
        self.top_node.scene().addItem(self)
        self.create_line()

    def __str__(self) -> str:
        return f"Connection [{self.bottom_node}->{self.top_node}]"

    def add_to_scene(self, new_scene: AggregationScene) -> None:
        old_scene = self.scene()
        if old_scene is not None:
            old_scene.removeItem(self)
        new_scene.addItem(self)

    def create_line(self) -> None:
        self.path = QPainterPath()
        self.path.moveTo(self.points[0])

        for point in self.points[1:]:
            self.path.lineTo(point)

        self.setPath(self.path)

    def update_line(self) -> None:
        # Update Curve Position
        self.path = QPainterPath()
        self.path.moveTo(self.points[0])
        for point in self.points[1:]:
            self.path.lineTo(point)
        self.setPath(self.path)

        self.setPos(0.0, 0.0)

    @property
    def points(self) -> list[QPointF]:
        def top_center(rect: QRectF) -> QPointF:
            x = rect.x() + rect.width() / 2
            y = rect.y()
            point = QPointF(x, y)
            return point

        def bottom_center(rect: QRectF) -> QPointF:
            x = rect.x() + rect.width() / 2
            y = rect.y() + rect.height()
            point = QPointF(x, y)
            return point

        p0 = top_center(self.bottom_node.sceneBoundingRect())  # top center of Bottom Node
        p3 = bottom_center(self.top_node.sceneBoundingRect())  # bottom center of Top Node

        p1 = QPointF()
        p2 = QPointF()

        p1.setX(p0.x())
        p2.setX(p3.x())

        mid_y = (p3.y() + constants.BOX_BOTTOM_DISTANCE)
        p1.setY(mid_y)
        p2.setY(mid_y)

        return [p0, p1, p2, p3]


class PopUp(QWidget):
    def __init__(self, clicked_node: Node, scene_pos) -> None:
        def init_combo_box() -> None:
            self.layout().addWidget(self.combo_box)

            # List all Nodes which aren't in Scene
            node_list = [item_to_name(node) for node in clicked_node.scene().items() if isinstance(node, Node)]
            name_list = [item_to_name(obj) for obj in classes.Object if
                         item_to_name(obj) not in node_list]

            name_list.sort()

            self.combo_box.addItems(name_list)
            self.combo_box.setDuplicatesEnabled(False)
            self.combo_box.setEditable(True)
            self.combo_box.show()

        super(PopUp, self).__init__()
        self.clicked_node = clicked_node
        self.graph_window = self.clicked_node.graph_window
        self.scene:AggregationScene = self.clicked_node.scene()
        self.button = QPushButton("Add")

        self.setLayout(QHBoxLayout())
        self.combo_box = QComboBox()
        init_combo_box()
        self.layout().addWidget(self.button)
        self.graph_window.node_popup = self
        self.setContentsMargins(0, 0, 0, 0)

        self.button.clicked.connect(self.button_pressed)
        self.proxy = self.scene.addWidget(self)
        self.proxy.setZValue(2)
        self.proxy.setPos(scene_pos)
        self.proxy.setContentsMargins(0, 0, 0, 0)


    def button_pressed(self) -> None:

        text = self.combo_box.currentText()
        obj = self.graph_window.object_dict.get(text)

        node = Node(obj, self.graph_window)
        self.clicked_node.add_child(node)
        node.setX(self.clicked_node.x())
        node.setY(node.base_y)
        pos = QPointF()
        pos.setX(node.x())
        pos.setY(node.y())
        self.clicked_node.graph_window.update_combo_list()

        self.scene.removeItem(self.parent())
        self.deleteLater()
        self.graph_window.node_popup = None

class Rect(QGraphicsRectItem):
    def __init__(self,proxy:Node):
        super(Rect, self).__init__()
        self.proxy = proxy
        pen = QPen()
        pen.setColor(QColor("white"))
        self.setPen(pen)

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        super(Rect, self).mouseMoveEvent(event)
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        x_dif = updated_cursor_position.x() - orig_cursor_position.x()
        y_dif = updated_cursor_position.y() - orig_cursor_position.y()

        self.proxy.moveBy(x_dif, y_dif)

    def mousePressEvent(self, event) -> None:
        super(Rect, self).mousePressEvent(event)

class Node(QGraphicsProxyWidget):
    _registry = list()

    def __init__(self, obj: classes.Object,graph_window:GraphWindow) -> None:

        self.rect = Rect(self)
        super(Node, self).__init__(self.rect)
        self._registry.append(self)
        self.object = obj
        self.object.add_node(self)
        self.parent_box = None
        self.children: Set[Node] = set()
        self.connections: List[Connection] = list()
        self.show()
        self.rect.show()
        self.graph_window = graph_window
        self.main_window = graph_window.main_window

        self.setWidget(QWidget())
        self.object_graph_rep = ui_ObjectGraphWidget.Ui_object_graph_widget()
        self.object_graph_rep.setupUi(self.widget())
        self.setZValue(1)
        self.button_add = self.object_graph_rep.button_add
        self.title = self.object_graph_rep.label_object_name
        self.list = self.object_graph_rep.list_widget_property_sets
        self.button_add.hide()
        self.title.setText(self.name)
        self.title.show()
        self.fill_table()
        self.rect.setFlag(self.rect.ItemIsMovable,True)
        self.setFlag(self.ItemIsMovable,True)
        fac = 0
        help_rect = self.boundingRect()
        width = help_rect.width()+fac
        height = help_rect.height()+fac
        self.rect.setRect(QRectF(0,0,width,height))
        self.setPos(fac/2,fac/2)
        self.button_add.clicked.connect(self.add_button_pressed)
        self.list.itemClicked.connect(self.select_list_item)

    def __str__(self) -> str:
        return (f"{self.object.name}: {self.x()},{self.y()}")

    def __iter__(self) -> Iterator[Node]:
        return self.children.__iter__()

    def __len__(self) -> int:
        return len(self.children)


    def print_info(self):
        print("-------------------------")
        print(f"Node: {self}")
        print(f"scene: {self.scene()}")
        print(self.isVisible())
        print(self.scenePos())
        print(f"rec_scene: {self.rect.scene()}")
        print(self.rect.isVisible())
        print(self.rect.scenePos())
        print(f"children:")
        for child in self.children:
            print(f"   {child}")

    def scene(self) -> AggregationScene:
        return super(Node, self).scene()

    ### Functions ###
    def add_button_pressed(self) -> PopUp:
        old_popup: PopUp = self.graph_window.node_popup
        if old_popup is not None:
            self.scene().removeItem(old_popup.parent())
            old_popup.deleteLater()

        view = self.graph_window.view
        origin = view.mapFromGlobal(QCursor.pos())
        relative_origin = view.mapToScene(origin)
        return PopUp(self, relative_origin)

    def add_child(self, child: Node, connect=True) -> Node:
        self.children.add(child)
        child.parent_box = self

        if connect:
            self.connect_to_node(child)
            self.scene().add_node(child)

        return child

    def connect_to_node(self, node: Node):
        if node is not None:
            con = Connection(node, self)
            self.connections.append(con)
            node.connections.append(con)

    def fill_table(self) -> None:
        for property_set in self.object.property_sets:
            item = classes.CustomListItem(property_set)
            self.object_graph_rep.list_widget_property_sets.addItem(item)

    def remove_child(self,child:Node) -> None:

        self.children.remove(child)
        self._registry.remove(child)
        for item in child.children.copy():
            child.remove_child(item)

        child.object.remove_node(child)
        self.scene().remove_node(child)



    def delete_clicked(self):
        def recursion(node:Node) -> None:
            nodes.append(node)
            for child in node.children:
                recursion(child)
        nodes = list()
        if self.is_root:
            for child in self.children:
                recursion(child)
        else:
            recursion(self)


        delete_bool = popups.msg_del_items([item_to_name(node) for node in nodes])
        if delete_bool:
            if self.is_root:
                self.object.remove_node(self)
                self.remove_all_children()
                self.graph_window.remove_scene(self.scene())
            else:
                self.parent_box.remove_child(self)

    def remove_all_children(self) -> None:
        for child in self.children.copy():
                self.remove_child(child)

    def select_list_item(self,selected_item):
        if selected_item is not None:
            property_set = selected_item.property_set
            self.main_window.pset_window = property_widget.open_pset_window(self.main_window, property_set,
                                                                            self.main_window.active_object)

    ### Properties ###
    @property
    def base_y(self) -> float:
        return self.level * (constants.BOX_HEIGHT + constants.BOX_MARGIN)

    @property
    def is_root(self) -> bool:
        if self.scene() is None:
            return False
        if self == self.scene().root_node:
            return True
        else:
            return False

    @property
    def level(self) -> int:
        def count(item: Node, index):
            if item.parent_box is not None:
                index += 1
                return count(item.parent_box, index)
            else:
                return index

        return count(self, 0)

    @property
    def name(self) -> str:
        return item_to_name(self)

    @property
    def top_connections(self) -> list[Connection]:
        return [connection for connection in self.connections if self == connection.bottom_node]

    @property
    def bottom_connections(self) -> list[Connection]:
        return [connection for connection in self.connections if self == connection.top_node]


    @property
    def movable(self):
        if self.button_add.underMouse() or self.list.underMouse():
            return False
        else:
            return True

    ### Events ###

    def hoverEnterEvent(self, event) -> None:
        self.button_add.show()


    def hoverLeaveEvent(self, event) -> None:
        self.button_add.hide()
        super(Node, self).hoverLeaveEvent(event)

    def moveEvent(self, event:QGraphicsSceneMoveEvent) -> None:
        super(Node, self).moveEvent(event)
        for connection in self.connections:
            connection.update_line()
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super(Node, self).mouseMoveEvent(event)
        for el in self.connections:
            el.update_line()

    def setX(self, x:float) -> None:
        super(Node, self).setX(x)
        self.rect.setX(x)


    def setY(self, y: float) -> None:
        super(Node, self).setY(y)
        self.rect.setY(y)

class GraphWindow(QWidget):

    def __init__(self, main_window,show = True) -> None:
        super(GraphWindow, self).__init__()
        self.main_window = main_window
        self.widget = ui_GraphWindow.Ui_GraphView()
        self.widget.setupUi(self)
        self.view = MainView(self)
        self.active_scene = None
        self.node_popup:PopUp|None = None
        self.combo_box = self.widget.combo_box
        self.reload_button = self.widget.button_reload
        self.add_button = self.widget.button_add
        self.delete_button = self.widget.button_delete
        self.scenes: list[AggregationScene] = list()
        self.drawn_scenes: list[AggregationScene] = list()
        if show:
            self.show()

        # replace view
        self.widget.gridLayout.removeWidget(self.widget.graphicsView)
        self.widget.graphicsView.deleteLater()
        self.widget.gridLayout.addWidget(self.view, 1, 0, 1, 4)
        if show:
            self.view.show()

        # connections
        self.combo_box.currentIndexChanged.connect(self.combo_change)
        self.reload_button.clicked.connect(self.redraw)
        self.reload_button.setIcon(icons.get_reload_icon())
        self.add_button.clicked.connect(self.add_button_pressed)
        self.delete_button.clicked.connect(self.delete_button_pressed)
        self.combo_box.setCurrentIndex(0)

    ### Functions ###

    def import_excel(self,pset_dict: dict[str, (classes.PropertySet, object, classes.Object)],
                           aggregate_dict: dict[classes.Object, list[str]]) -> None:

        kuerzel_dict = {obj:kuerzel for (kuerzel,(a,b,obj)) in pset_dict.items()}
        all_children = [element for sublist in aggregate_dict.values() for element in sublist]

        def is_root(obj):
            kuerzel = kuerzel_dict[obj]
            if kuerzel  in all_children:
                return False
            else:
                return True

        def recursion(node:Node)-> None:
            scene = node.scene()
            aggregate_list = aggregate_dict[node.object]
            for kuerzel in aggregate_list:
                dic = pset_dict.get(kuerzel)
                if dic is not None:
                    obj_child = dic[2]
                    if obj is not None:
                        child_node = Node(obj_child,self)
                        node.add_child(child_node,True)
                        recursion(child_node)
                    else:
                        logging.error(f"[{obj.name}] Aggregation: Kürzel {kuerzel} existiert nicht")
                else:
                    logging.error(f"[{obj.name}] Aggregation: Kürzel {kuerzel} existiert nicht")
        self.test_dict = {obj: Node(obj,self) for obj in classes.Object}
        self.scene_list = list()

        root_objects = [obj for obj in classes.Object if is_root(obj)]


        scene = None
        for obj in root_objects:
            node = Node(obj,self)
            scene = AggregationScene(node)
            self.scenes.append(scene)
            recursion(node)

        self.update_combo_list()
        self.combo_box.setCurrentIndex(0)
    def delete_button_pressed(self) ->None:
        if not self.combo_box.currentText() == "":
            root_node = self.active_scene.root_node
            string_list = [item_to_name(item) for item in self.active_scene.items() if isinstance(item, Node)]
            delete_request = popups.msg_del_items(string_list)
            if delete_request:
                root_node.remove_all_children()
                self.remove_scene(self.active_scene)

    def remove_scene(self,scene:AggregationScene) -> None:
        self.scenes.remove(scene)
        root_node = scene.root_node
        text = item_to_name(root_node)
        index = self.combo_box.findText(text)

        if index >0:
            self.combo_box.setCurrentIndex(index + 1)
        else:
            self.combo_box.setCurrentIndex(0)
        self.combo_box.removeItem(index)

    def clear_scene(self, scene:AggregationScene)->None:
        root_node = scene.root_node
        text = item_to_name(root_node)
        index = self.combo_box.findText(text)
        self.combo_box.setCurrentIndex(index+1)

        self.combo_box.removeItem(index)
        self.drawn_scenes.remove(scene)
        for item in scene.items():
            if item not in  [root_node,root_node.rect]:
                if isinstance(item,Node):
                    scene.remove_node(item)
                else:
                    scene.removeItem(item)



    def create_scene_by_node(self,node:Node) -> AggregationScene:
        scene = AggregationScene(node)
        self.scenes.append(scene)
        return scene

    def add_button_pressed(self):
        dialog = QInputDialog()
        dialog.setWindowTitle("New Aggregation")
        dialog.setLabelText("Choose Root Object")
        dialog.setTextValue("")
        obj:classes.Object

        root_objects = set()
        for obj in classes.Object:
            if obj.nodes is None:
                root_objects.add(obj)
            else:
                for node in obj.nodes:
                    if node.parent_box is None:
                        root_objects.add(obj)


        root_objects = set(item_to_name(obj) for obj in root_objects)  #objects that don't aggregate from someone
        combo_names = set(self.combo_box.itemText(index) for index in range(self.combo_box.count()))    # items that are listed in combobox

        words = sorted(list(root_objects-combo_names))
        dialog.setComboBoxItems(words)
        combo_box:QComboBox = dialog.findChild(QComboBox)
        dialog.setComboBoxEditable(True)

        ok = (dialog.exec() == QInputDialog.Accepted)
        if ok:
            text = dialog.textValue()
            obj = {item_to_name(obj):obj for obj in classes.Object}.get(text)
            if obj is not None:
                text_pos = self.combo_box.findText(text)

                self.combo_box.addItem(str(text))
                node = Node(obj,self)
                self.create_scene_by_node(node)
                self.draw_tree(node)

                text_pos = self.combo_box.findText(text)
                self.combo_box.setCurrentIndex(text_pos)
                self.combo_box.model().sort(0, Qt.AscendingOrder)

    def find_node_by_name(self, name) -> Node:
        return {node.name:node for node in Node._registry}.get(name)

    def change_scene(self, node: Node) -> None:
        self.active_scene = self.scene_dict[node]

        if self.active_scene not in self.drawn_scenes:
            self.redraw()
            self.drawn_scenes.append(self.active_scene)
        self.fit_in()
    def get_node(self) -> Node:
        combo_box = self.widget.combo_box
        text = combo_box.currentText()
        node = self.find_node_by_name(text)
        return node

    def combo_change(self) -> None:
        node = self.get_node()
        if node is not None:
            self.change_scene(node)
        else:
            print("NODE IS NONE")

        if self.combo_box.count() == 1 and self.combo_box.currentText() =="":
            self.view.setScene(QGraphicsScene())


    def redraw(self) -> None:
        node = self.get_node()

        if node is not None:
            self.draw_tree(node)

    def update_combo_list(self) -> None:
        combo = self.combo_box

        rn_with_children = set(item_to_name(node) for node in self.root_nodes if len(node.children)>0)

        # remove old Items
        for i in range(combo.count()):
            text = combo.itemText(i)
            if text not in rn_with_children:
                combo.removeItem(i)

        # add New Items
        for item in rn_with_children:
            if combo.findText(item) == -1:
                combo.addItem(item)

        combo.model().sort(0,Qt.AscendingOrder)

    def draw_tree(self, root: Node) -> None:
        """give correct tree position and fit in View"""

        def iter_x_pos(item: Node, drawtree: DrawTree) -> None:  # give each element correct position
            child: Node
            for i, child in enumerate(item):
                draw_child = drawtree.children[i]
                x = draw_child.x * (constants.BOX_WIDHT + constants.BOX_MARGIN)
                child.setX(x)
                child.setY(child.base_y)
                if child not in root.scene().items():
                    root.scene().addItem(child)
                    for connection in child.connections:
                        connection.add_to_scene(root.scene())
                child.show()
                iter_x_pos(child, draw_child)


        self.active_scene = root.scene()
        draw_tree = DrawTree(root)
        draw_tree = buchheim(draw_tree)

        root.setX(draw_tree.x * (constants.BOX_WIDHT + constants.BOX_MARGIN))
        root.setY(root.base_y)
        root.show()
        iter_x_pos(root, draw_tree)
        self.fit_in()

        for item in root.scene().items():
            if isinstance(item,Connection):
                item.update_line()

    def fit_in(self) -> None:
        if self.active_scene is None:
            return
        visible_items = [item for item in self.active_scene.items() if
                         item.isVisible() and not isinstance(item, (QGraphicsPathItem))]
        bounding_rect = visible_items[0].boundingRect()
        visible_items.sort(key=lambda x: str(type(x)))
        for item in visible_items:
            item_br = item.sceneBoundingRect()
            if item_br.right() > bounding_rect.right():
                bounding_rect.setRight(item_br.right())
            if item_br.left() < bounding_rect.left():
                bounding_rect.setLeft(item_br.left())
            if item_br.top() < bounding_rect.top():
                bounding_rect.setTop(item_br.top())
            if item_br.bottom() > bounding_rect.bottom():
                bounding_rect.setBottom(item_br.bottom())

        y_base_margin = 20
        x_base_margin = 20
        if len(visible_items) >1:


            bounding_rect.setRect(bounding_rect.x() - x_base_margin, bounding_rect.y() - y_base_margin,
                                  bounding_rect.width() + 2 * x_base_margin, bounding_rect.height() + 2 * y_base_margin)
        else:
            y_margin = 1000

            bounding_rect.setRect(bounding_rect.x() - x_base_margin, bounding_rect.y() - y_base_margin,
                                  bounding_rect.width() + 2 * x_base_margin, bounding_rect.height() + y_margin)


        self.active_scene.setSceneRect(bounding_rect)
        self.view.fitInView(self.active_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.view.centerOn(self.active_scene.sceneRect().center())

    ### Properties ###
    @property
    def node_dict(self) -> dict[classes.Object, Node]:
        nd: dict[classes.Object, Node] = dict()
        for node in Node._registry:
            nd[node.object] = node
        return nd

    @property
    def root_nodes(self) -> list[Node]:
        return [node for node in Node._registry if node.parent_box is None]

    @property
    def scene_dict(self) -> dict[Node, AggregationScene]:
        return {scene.root_node: scene for scene in self.scenes}

    @property
    def object_dict(self)-> dict[str,classes.Object]:
        return {item_to_name(obj):obj for obj in classes.Object}

    @property
    def active_scene(self) -> AggregationScene:
        return self.view.scene()

    @active_scene.setter
    def active_scene(self, scene:AggregationScene) -> None:
        self.view.setScene(scene)