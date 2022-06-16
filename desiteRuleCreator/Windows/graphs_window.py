import re
import os
import copy
from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent,QIcon,QWheelEvent,QCursor,QGuiApplication
from PySide6.QtWidgets import QWidget, QListWidgetItem,QLabel,QGraphicsScene,QGraphicsView,QApplication,QGraphicsProxyWidget,QGraphicsSceneMouseEvent

from desiteRuleCreator.QtDesigns import ui_GraphWindow, ui_ObjectGraphWidget
from desiteRuleCreator.data import classes,constants
from desiteRuleCreator import icons
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.Widgets import property_widget

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

class ObjectBox(QGraphicsProxyWidget):
    def __init__(self, obj,main_window):
        super(ObjectBox, self).__init__()
        self.object = obj
        self.test = QWidget()
        self.object_graph_rep =  ui_ObjectGraphWidget.Ui_object_graph_widget()
        self.object_graph_rep.setupUi(self.test)
        self.app = main_window.app
        self.getText()
        self.fill_table()
        self.setWidget(self.test)
        self.show()
        self.main_window = main_window
        self.child_boxes = list()
        self.parent_box = None

    def move_with_children(self,x_dif,y_dif):
        self.moveBy(x_dif,y_dif)
        for child in self.child_boxes:
            child.move_with_children(x_dif,y_dif)

    def x_max_right(self):
        x_max = self.right()
        for child in self.child_boxes:
            if child.right() > x_max:
                x_max = child.right()

        return x_max

    def x_center(self):
        return (self.left()+self.right())/2

    def left(self):
        return self.scenePos().x()

    def right(self):
        return self.scenePos().x()+self.rect().width()

    def top(self):
        return self.scenePos().y()

    def add_child(self,child):
        if len(self.child_boxes) >0:
            x_max = max([x.right() for x in self.child_boxes])
            y_min = min([y.top() for y in self.child_boxes])
            child.setPos(x_max+constants.BOX_MARGIN,y_min)
            self.child_boxes.append(child)
            x_max = max([x.right() for x in self.child_boxes])
            x_min = min([x.left() for x in self.child_boxes])
            x_center = (x_max+x_min)/2
            x_new = x_center-self.rect().width()/2
            self.setPos(x_new,self.scenePos().y())
        else:
            x_pos = self.x_center()-child.rect().width()/2
            y_pos = self.scenePos().y()+self.rect().height()+constants.BOX_MARGIN
            child.setPos(x_pos,y_pos)
            self.child_boxes.append(child)

    def mouseDoubleClickEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        pos = event.pos()
        item_pos = self.object_graph_rep.list_widget_property_sets.mapFrom(self.widget(),pos)
        selected_item = self.object_graph_rep.list_widget_property_sets.itemAt(item_pos.toPoint())
        if selected_item is not None:
            property_set = selected_item.property_set
            self.main_window.pset_window = property_widget.open_pset_window(self.main_window, property_set,
                                                                            self.main_window.active_object)

        super(ObjectBox, self).mouseDoubleClickEvent(event)


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

    def hoverLeaveEvent(self, event):
        self.app.instance().restoreOverrideCursor()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
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

        # for el in self.connections:
        #     el.update()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.app.instance().restoreOverrideCursor()

class GraphWindow(QWidget):
    def __init__(self, main_window):
        super(GraphWindow, self).__init__()
        self.widget = ui_GraphWindow.Ui_GraphView()
        self.widget.setupUi(self)
        self.main_window = main_window
        self.show()
        self.widget.gridLayout.removeWidget(self.widget.graphicsView)
        self.widget.graphicsView.deleteLater()
        main_view = MainView()
        self.widget.gridLayout.addWidget(main_view, 0, 0, 1, 1)

        self.view = main_view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        test(self)



def test(window):
    def iterate():
        sorted_objects = list()
        [sorted_objects.extend(x) for x in level_list]
        list_item = list()
        obj: classes.Object
        for obj in list(object_list):
            if obj.parent in sorted_objects:
                list_item.append(obj)
                object_list.remove(obj)
        level_list.append(list_item)
        if len(object_list)>0:
            iterate()

    def find_max_width(obj:classes.Object) -> int:
        max_width = len(obj.children)
        for child in obj.children:
            max_width+=find_max_width(child)
        return max_width

    def find_pos(children: [ObjectBox]):

        x_list = list()
        y_list = list()
        for child in children:
            x_min = child.scenePos().x()
            x_max = child.scenePos().x()+child.rect().width()

            y_min = child.scenePos().y()
            y_max = child.scenePos().y()+child.rect().height()

            x_list.append(x_min)
            x_list.append(x_max)

            y_list.append(y_min)
            y_list.append(y_max)

        x_min = min(x_list)
        x_max = max(x_list)

        y_min = min(y_list)
        y_max = max(y_list)

        return x_min,x_max,y_min,y_max


    object_list =list(classes.Object.iter)
    obj:classes.Object
    level_list = list()
    list_item = list()
    for obj in list(object_list):
        if not obj.is_child:
            list_item.append(obj)
            object_list.remove(obj)

    level_list.append(list_item)
    iterate()

    obj:classes.Object
    box_dict = dict()
    for obj in classes.Object.iter:
        box = ObjectBox(obj,window.main_window)
        box_dict[obj] = box
        window.scene.addItem(box)


    object_list = level_list[0]
    last_item = None

    for i,obj in enumerate(object_list):
        box = box_dict[obj]
        if last_item is None:
            box.setPos(0+constants.BOX_MARGIN*50,0)
        else:
            box.setPos(last_item.x_max_right()+constants.BOX_MARGIN*50,0)
        for child in obj.children:
            box.add_child(box_dict[child])
        last_item = box

