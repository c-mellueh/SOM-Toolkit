from PySide6.QtWidgets import QDialog, QTreeWidget, QWidget

from som_gui.module import class_
from som_gui.resources.icons import get_icon


class ClassTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        class_.trigger.repaint_event()

    def dropEvent(self, event):
        class_.trigger.drop_event(event,self)
        super().dropEvent(event)

    def mimeData(self, items):
        mime_data = super().mimeData(items)
        return class_.trigger.create_mime_data(list(items), mime_data)