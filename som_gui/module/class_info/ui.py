from PySide6.QtWidgets import (
    QDialog,
    QItemDelegate,
    QComboBox,
    QLineEdit,
    QCompleter,
    QStyledItemDelegate,
)
from PySide6.QtCore import QModelIndex, Qt
from som_gui.module import class_tree
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ClassInfo
from . import trigger
from som_gui import tool


class ClassInfoDialog(QDialog):
    def __init__(self):
        super(ClassInfoDialog, self).__init__()
        self.ui = Ui_ClassInfo()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        trigger.class_info_paint_event()
        super().paintEvent(event)



