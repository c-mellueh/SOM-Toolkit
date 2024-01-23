from som_gui.module import objects
from PySide6.QtWidgets import QTreeWidget, QWidget, QDialog
from som_gui.module.objects.window import Ui_ObjectInfo

class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        objects.trigger.repaint_event()

    def changeEvent(self, event):
        super().changeEvent(event)
        objects.trigger.change_event()

    def dropEvent(self, event):
        objects.trigger.drop_event(event)
        super().dropEvent(event)


class ObjectInfoWidget(QDialog):
    def __init__(self):
        super(ObjectInfoWidget, self).__init__()
        self.widget = Ui_ObjectInfo()
        self.widget.setupUi(self)

    def paintEvent(self, event):
        objects.trigger.object_info_paint_event()
        super().paintEvent(event)

