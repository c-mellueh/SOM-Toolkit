from PySide6.QtWidgets import QDialog, QTreeWidget, QWidget

from som_gui.module import class_
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ObjectInfo
from . import trigger
class ClassInfoWidget(QDialog):
    def __init__(self):
        super(ClassInfoWidget, self).__init__()
        self.widget = Ui_ObjectInfo()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        trigger.object_info_paint_event()
        super().paintEvent(event)