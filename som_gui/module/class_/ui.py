from PySide6.QtWidgets import QDialog, QTreeWidget, QWidget

from som_gui.module import class_
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ObjectInfo


class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        class_.trigger.repaint_event()

    def dropEvent(self, event):
        class_.trigger.drop_event(event)
        super().dropEvent(event)


class ClassInfoWidget(QDialog):
    def __init__(self):
        super(ClassInfoWidget, self).__init__()
        self.widget = Ui_ObjectInfo()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        class_.trigger.object_info_paint_event()
        super().paintEvent(event)
