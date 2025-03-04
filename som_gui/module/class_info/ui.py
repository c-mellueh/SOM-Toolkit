from PySide6.QtWidgets import QDialog

from som_gui.module import class_
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ObjectInfo
from . import trigger


class ClassInfoDialog(QDialog):
    def __init__(self):
        super(ClassInfoDialog, self).__init__()
        self.ui = Ui_ObjectInfo()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        trigger.object_info_paint_event()
        super().paintEvent(event)
