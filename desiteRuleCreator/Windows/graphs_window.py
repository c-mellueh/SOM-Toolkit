import re
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent,QIcon,QWheelEvent,QCursor,QGuiApplication
from PySide6.QtWidgets import QWidget, QListWidgetItem,QLabel,QGraphicsScene,QGraphicsView,QApplication,QGraphicsProxyWidget,QGraphicsSceneMouseEvent

from desiteRuleCreator.QtDesigns import ui_GraphWindow, ui_ObjectGraphWidget
from desiteRuleCreator.data import classes,constants
from desiteRuleCreator import icons
from desiteRuleCreator.Windows import popups


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
        self.widget = QWidget()
        self.object_graph_rep =  ui_ObjectGraphWidget.Ui_object_graph_widget()
        self.object_graph_rep.setupUi(self.widget)
        self.app = main_window.app
        self.object_graph_rep.label_object_name.setText(obj.name)

        self.setWidget(self.widget)
        self.show()


    def getText(self):
        if self.object.is_concept:
            text = f"{self.object}"
        else:
            text = f"{self.object} ({self.object.ident_attrib.value[0]}"
        self.object_graph_rep.label_object_name.setText(text)

    def hoverEnterEvent(self, event):
        print(f"{self.app} ; {self.app.instance()}")
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
    for obj in classes.Object.iter:
        print(obj)
        box = ObjectBox(obj, window.main_window)
        print(box)
        window.scene.addItem(box)
        print("--")