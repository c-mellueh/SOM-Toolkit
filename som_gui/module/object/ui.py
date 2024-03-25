from som_gui.module import object
from PySide6.QtWidgets import QTreeWidget, QWidget, QDialog
from som_gui.module.object.window import Ui_ObjectInfo
from som_gui.icons import get_icon
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
        self.setWindowTitle(f"Objektdetails")
    def paintEvent(self, event):
        object.trigger.object_info_paint_event()
        super().paintEvent(event)

