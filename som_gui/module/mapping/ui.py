from PySide6.QtWidgets import QTreeWidget, QMainWindow, QLineEdit, QDialog, QStyledItemDelegate
from PySide6.QtCore import Qt, Signal, QModelIndex
from PySide6 import QtGui
from som_gui.module import property_set_window

from som_gui.icons import get_icon
from . import trigger
from som_gui import tool


class MappingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from .window import Ui_Form
        self.widget = Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr(f"Mapping | {tool.Util.get_status_text()}"))


class ObjectTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr("Objekt"), self.tr("IfcMapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_object_tree()


class PropertySetTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr("PropertySet/Attribut"), self.tr("Revit Mapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_pset_tree()
