from PySide6.QtWidgets import QDialog, QTreeWidget, QWidget

from som_gui.module import class_
from som_gui.resources.icons import get_icon


class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        class_.trigger.repaint_event()

    def dropEvent(self, event):
        class_.trigger.drop_event(event)
        super().dropEvent(event)