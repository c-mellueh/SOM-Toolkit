from som_gui.module import objects
from PySide6.QtWidgets import QTreeWidget, QWidget


def load_triggers():
    objects.trigger.connect()


class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.test_bool = False

    def paintEvent(self, event):
        super().paintEvent(event)
        objects.trigger.repaint_event()

    def changeEvent(self, event):
        super().changeEvent(event)
        objects.trigger.change_event()

    def dropEvent(self, event):
        objects.trigger.drop_event(event)
        super().dropEvent(event)
