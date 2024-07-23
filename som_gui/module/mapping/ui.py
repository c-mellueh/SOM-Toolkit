from PySide6.QtWidgets import QTableWidget, QMainWindow, QLineEdit, QDialog, QStyledItemDelegate
from PySide6.QtCore import Qt, Signal, QModelIndex
from PySide6 import QtGui
from som_gui.module import property_set_window

from som_gui.icons import get_icon
from . import trigger


class MappingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from .window import Ui_Form
        self.widget = Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Mapping"))


class ObjectTreeWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.tr("Objekt"), self.tr("IfcMapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_object_tree()


class PropertySetTreeWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.tr("PropertySet/Attribut"), self.tr("Revit Mapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_pset_tree()
