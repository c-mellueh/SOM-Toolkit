from __future__ import annotations      #make own class referencable
import re
import os
import copy
from PySide6.QtCore import Qt,QRectF,QPointF
from PySide6.QtGui import QShowEvent,QIcon,QWheelEvent,QCursor,QGuiApplication,QPainterPath,QHideEvent
from PySide6.QtWidgets import QWidget, QListWidgetItem,QLabel,QGraphicsScene,QGraphicsView,QApplication,QGraphicsProxyWidget,QGraphicsSceneMouseEvent,QGraphicsPathItem,QComboBox,QGraphicsRectItem,QCompleter

from desiteRuleCreator.QtDesigns import ui_GraphWindow, ui_ObjectGraphWidget
from desiteRuleCreator.data import classes,constants
from desiteRuleCreator import icons
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.Widgets import property_widget

class DrawTree(object):
    _registry = list()
    def __init__(self, tree, parent=None, depth=0, number=1):
        self.x = -1.
        self.y = depth
        self.tree = tree
        self.children = [DrawTree(c, self, depth+1, i+1) for i, c in enumerate(tree.children)]
        self.parent = parent
        self.thread = None
        self.mod = 0
        self.ancestor = self
        self.change = self.shift = 0
        self._lmost_sibling = None
        self._registry.append(self)
        #this is the number of the node in its group of siblings 1..n
        self.number = number

    def left(self):
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

    def lbrother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self: return n
                else:            n = node
        return n

    @property
    def lmost_sibling(self):
        if not self._lmost_sibling and self.parent and self != \
        self.parent.children[0]:
            self._lmost_sibling = self.parent.children[0]
        return self._lmost_sibling

    def __str__(self): return f"DrawTree x={self.x}, mod={self.mod}"
    def __repr__(self): return self.__str__()

def buchheim(tree):
    dt = firstwalk(DrawTree(tree))
    min = second_walk(dt)
    if min < 0:
        third_walk(dt, -min)
    return dt

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
        #in buchheim notation:
        #i == inner; o == outer; r == right; l == left; r = +; l = -
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
    #the relevant text is at the bottom of page 7 of
    #"Improving Walker's Algorithm to Run in Linear Time" by Buchheim et al, (2002)
    #http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.16.8757&rep=rep1&type=pdf
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
        min = second_walk(w, m + v.mod, depth+1, min)

    return min



class MainView(QGraphicsView):
    def __init__(self):
        super(MainView, self).__init__()
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
        self.setDragMode(self.DragMode.ScrollHandDrag)


class Connection:
    liste = []

    def __init__(self, bottom_node, top_node):

        self.label = None
        self.bottom_node:Node = bottom_node
        self.top_node: Node = top_node
        self.scene = self.top_node.scene()

        self.create_line()

        Connection.liste.append(self)

    def __str__(self):
        return "Connection [{0}->{1}]".format(self.bottom_node, self.top_node)

    def create_line(self):
        self.points = self.get_pos()
        self.path = QPainterPath()
        self.path.moveTo(self.points[0])
        self.path.lineTo(self.points[1])
        self.path.lineTo(self.points[2])
        self.path.lineTo(self.points[3])
        self.line = QGraphicsPathItem()
        self.line.setPath(self.path)
        self.scene.addItem(self.line)

    def get_pos(self) -> list:
        def top_center(rect: QRectF):
            x = rect.x() + rect.width() / 2
            y = rect.y()
            point = QPointF(x, y)
            return point

        def bottom_center(rect: QRectF):
            x = rect.x() + rect.width() / 2
            y = rect.y() + rect.height()
            point = QPointF(x, y)
            return point
        pstart =top_center(self.bottom_node.sceneBoundingRect())  #top center of Bottom Node
        p2 = QPointF()
        p3 = QPointF()
        pend =bottom_center(self.top_node.sceneBoundingRect())   # bottom center of Top Node

        mid_y = (pstart.y()-pend.y())/2+pend.y()

        p2.setX(pstart.x())
        p2.setY(mid_y)

        p3.setX(pend.x())
        p3.setY(mid_y)

        return [pstart, p2, p3, pend]

    def update(self):
        # Update Curve Position
        self.points = self.get_pos()

        self.path = QPainterPath()
        self.path.moveTo(self.points[0])
        self.path.lineTo(self.points[1])
        self.path.lineTo(self.points[2])
        self.path.lineTo(self.points[3])
        self.line.setPath(self.path)

        self.line.setPos(0.0, 0.0)
        return self.points

    def hide(self):
        self.line.hide()

    def show(self):
        self.line.show()


class Node(QGraphicsProxyWidget):
    _registry=list()
    def __init__(self, obj:classes.Object,main_window):
        super(Node, self).__init__()
        self.object = obj
        self.setWidget(QWidget())
        self.object_graph_rep =  ui_ObjectGraphWidget.Ui_object_graph_widget()
        self.object_graph_rep.setupUi(self.widget())
        self.app = main_window.app

        if self.object is None:
            self.name = "Root"
        else:
            self.name = obj.name
            self.getText()
            self.fill_table()

        self.main_window = main_window
        self.children = list()
        self.parent_box = None
        self._left_item = None
        self._right_item = None
        self._index = None
        self._registry.append(self)
        self.connections = list()
        self.base_y = 0.0
        self.button_add = self.object_graph_rep.button_add
        self.button_add.hide()
        self.button_add.clicked.connect(self.add_button_pressed)

    @property
    def is_root(self):
        if self.object is None:
            return True
        else:
            return False

    def __str__(self):
        return(f"{self.object.name}: {self.x()},{self.y()}")

    def __iter__(self): return self.children.__iter__()
    def __len__(self): return self.children.__len__()
    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.children[key]
        else:
            return None

    def add_button_pressed(self):

        cursor_pos = QCursor.pos()
        print(f"global: {cursor_pos}")
        pos = self.scene().views()[0].mapToScene(cursor_pos)
        print(f"scene {pos}")
        combo_box = QComboBox()
        proxy = self.scene().addWidget(combo_box)
        proxy.setPos(pos)

        print(QCursor.pos())

    def add_child(self,child,connect = True):
            self.children.append(child)
            if connect:
                self.connect_to_node(child)
            return child


    def mouseDoubleClickEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        pos = event.pos()
        item_pos = self.object_graph_rep.list_widget_property_sets.mapFrom(self.widget(),pos)
        selected_item = self.object_graph_rep.list_widget_property_sets.itemAt(item_pos.toPoint())
        print(selected_item)
        if selected_item is not None:
            property_set = selected_item.property_set
            self.main_window.pset_window = property_widget.open_pset_window(self.main_window, property_set,
                                                                            self.main_window.active_object)

        super(Node, self).mouseDoubleClickEvent(event)


    def getText(self):
        if self.object.is_concept:
            text = f"{self.object.name}"
        else:
            text = f"{self.object.name} ({self.object.ident_attrib.value[0]})"
        self.object_graph_rep.label_object_name.setText(text)

    def fill_table(self):
        for property_set in self.object.property_sets:
            item = classes.CustomListItem(property_set)
            self.object_graph_rep.list_widget_property_sets.addItem(item)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.button_add.show()
    def hoverLeaveEvent(self, event):
        self.app.instance().restoreOverrideCursor()
        self.button_add.hide()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.pos()
        item_pos=self.button_add.mapFrom(self.widget(),pos)
        if item_pos.x()>0 and item_pos.x()< self.button_add.rect().width():
            if item_pos.y()>0:
                self.button_add.click()
        else:
            self.app.instance().setOverrideCursor(Qt.ClosedHandCursor)
        pass

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:

        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        orig_position = self.scenePos()

        x_dif = updated_cursor_position.x() - orig_cursor_position.x()
        y_dif = updated_cursor_position.y() - orig_cursor_position.y()

        #x_dif, y_dif = self.check_for_exit(x_dif, y_dif)

        self.moveBy(x_dif, y_dif)

        for el in self.connections:
            el.update()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.app.instance().restoreOverrideCursor()

    @property
    def left_item(self)-> Node:
        return self._left_item

    @left_item.setter
    def left_item(self, item:Node)->None:
        self._left_item = item
        if item.right_item != self:
            item.right_item = self

    @property
    def right_item(self)->Node:
        return self._right_item

    @right_item.setter
    def right_item(self, item:Node)->None:
        self._right_item = item
        if item.left_item != self:
            item.left_item = self

    @property
    def index(self)->int:
        return self._index

    @index.setter
    def index(self,value)->None:
        self._index = value

    def get_child_by_index(self,index):
        for child in self.children:
            if child.index == index:
                return child
        return None

    def connect_to_node(self,node:Node):
        if node is not None:
            con = Connection(node,self)
            self.connections.append(con)
            node.connections.append(con)
            con.hide()

    def hideEvent(self, event:QHideEvent) -> None:
        super(Node, self).hideEvent(event)
        for connection in self.connections:
            connection.hide()

    def showEvent(self, event:QShowEvent) -> None:
        super(Node, self).showEvent(event)
        for connection in self.connections:
            connection.show()
            connection.update()

class GraphWindow(QWidget):

    def __init__(self, main_window):
        super(GraphWindow, self).__init__()
        self.show()
        self.widget = ui_GraphWindow.Ui_GraphView()
        self.widget.setupUi(self)
        self.main_window = main_window

        #replace view

        self.widget.gridLayout.removeWidget(self.widget.graphicsView)
        self.widget.graphicsView.deleteLater()
        self.view = MainView()
        self.widget.gridLayout.addWidget(self.view , 1, 0, 1, 3)

        self.active_scene = QGraphicsScene()
        self.view.setScene(self.active_scene)

        self.nodes = list()
        self.scenes =list()
        self.construct_all_nodes()


        self.widget.combo_box.currentIndexChanged.connect(self.combo_change)
        self.widget.button_reload.clicked.connect(self.redraw)
        self.widget.button_reload.setIcon(icons.get_reload_icon())
        self.redraw()

    @property
    def node_dict(self) -> dict[classes.Object,Node]:
        nd: dict[classes.Object,Node] = dict()
        for node in Node._registry:
            nd[node.object] = node
        return nd

    @property
    def root_objects(self) -> list[classes.Object]:
        return [obj for obj in classes.Object if len(obj.aggregates_from)==0]

    @property
    def root_nodes(self)->list[Node]:
        return [self.node_dict[obj] for obj in self.root_objects]

    @property
    def scene_dict(self)-> dict[Node,QGraphicsScene]:
        return {node:node.scene() for node in self.nodes}

    @property
    def combo_list_names(self)-> list[str]:
        names = [obj.name for obj in self.root_objects if self.node_dict[obj].children]
        names.sort()
        return names

    def find_node_by_name(self,name):
        for obj in self.root_objects:
            if obj.name == name:
                return self.node_dict[obj]

    def change_root(self,node):
            self.active_scene = self.scene_dict[node]
            self.view.setScene(self.active_scene)
            self.visible_items_bounding()

    def get_node(self):
        combo_box = self.widget.combo_box
        text = combo_box.currentText()
        node = self.find_node_by_name(text)

        return node
    def combo_change(self):
        node = self.get_node()
        self.change_root(node)

    def redraw(self):
        node = self.get_node()
        self.draw_tree(node)

    def construct_all_nodes(self):


        def create_nodes():
            """create Nodes and add them to Scenes"""
            def iterate_nodes(children:list[classes.Object], parent: Node, level:int):
                """ Recursivly Add ChildNodes to Node"""

                for obj in children:
                    node = Node(obj, self.main_window)
                    self.nodes.append(node)
                    node.setY(level * (constants.BOX_HEIGHT + constants.BOX_MARGIN))
                    node.base_y = float(node.y())

                    parent.scene().addItem(node)
                    parent.add_child(node)
                    iterate_nodes(obj.aggregates_to, node, level + 1)

            for obj in self.root_objects:
                scene = QGraphicsScene()
                self.scenes.append(scene)
                node = Node(obj, self.main_window)
                self.nodes.append(node)
                scene.addItem(node)
                iterate_nodes(obj.aggregates_to, node, 1)

        create_nodes()

        self.widget.combo_box.addItems(self.combo_list_names)

        for node in self.root_nodes:
            print(f"loop_root: {node}")
            self.draw_tree(node)

    def draw_tree(self,root:Node):
        def iter_x_pos(item:Node,drawtree): #give each element correct position
            child:Node
            for i,child in enumerate(item):
                draw_child = drawtree.children[i]
                x = draw_child.x*(constants.BOX_WIDHT+constants.BOX_MARGIN)
                child.setX(x)
                child.setY(child.base_y)
                child.show()
                iter_x_pos(child,draw_child)

        for node in root.scene().items():
            node.hide()

        self.active_scene = root.scene()
        self.view.setScene(self.active_scene)

        draw_tree = DrawTree(root)
        draw_tree = buchheim(draw_tree)

        root.setX(draw_tree.x*(constants.BOX_WIDHT+constants.BOX_MARGIN))
        root.setY(root.base_y)
        root.show()
        iter_x_pos(root,draw_tree)
        self.visible_items_bounding()
        # self.active_scene.setSceneRect(self.border_rect.rect())
        # self.view.fitInView(self.border_rect, Qt.AspectRatioMode.KeepAspectRatio)
        # self.view.centerOn(self.border_rect)


        print("--------")
        print(f"root {root}")
        node:Node
        for node in root.scene().items():
            if isinstance(node,Node):
                print(f"  {node}: {node.isVisible()}")
            # node.show()

    def visible_items_bounding(self):
        visible_items = [item for item in self.active_scene.items() if item.isVisible() and not isinstance(item, QGraphicsRectItem)]
        bounding_rect = visible_items[0].boundingRect()
        for item in visible_items:
            item_br= item.sceneBoundingRect()
            if item_br.right()>bounding_rect.right():
                bounding_rect.setRight(item_br.right())
            if item_br.left()<bounding_rect.left():
                bounding_rect.setLeft(item_br.left())
            if item_br.top()<bounding_rect.top():
                bounding_rect.setTop(item_br.top())
            if item_br.bottom()>bounding_rect.bottom():
                bounding_rect.setBottom(item_br.bottom())
        margin = 20
        bounding_rect.setRect(bounding_rect.x()-margin,bounding_rect.y()-margin,bounding_rect.width()+2*margin,bounding_rect.height()+2*margin)
        self.active_scene.setSceneRect(bounding_rect)
        self.view.fitInView(self.active_scene.sceneRect(),Qt.AspectRatioMode.KeepAspectRatio)
        self.view.centerOn(self.active_scene.sceneRect().center())

