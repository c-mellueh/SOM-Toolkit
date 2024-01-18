from som_gui import MainUi
from som_gui.module import objects
from PySide6.QtWidgets import QTreeWidget, QWidget
from PySide6.QtGui import QMouseEvent


def load_triggers():
    pass
    # MainUi.ui.action_settings.triggered.connect(objects.trigger.repaint_event())


class ObjectTreeView(QTreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        objects.trigger.repaint_event()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        objects.trigger.mouse_press_event(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        objects.trigger.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        objects.trigger.mouse_release_event(event)
