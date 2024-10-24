from PySide6.QtWidgets import QDialog, QTreeWidget, QWidget

from som_gui.module import object
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ObjectInfo


class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        object.trigger.repaint_event()

    def dropEvent(self, event):
        object.trigger.drop_event(event)
        super().dropEvent(event)


class ObjectInfoWidget(QDialog):
    def __init__(self):
        super(ObjectInfoWidget, self).__init__()
        self.widget = Ui_ObjectInfo()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        object.trigger.object_info_paint_event()
        super().paintEvent(event)
