from PySide6.QtWidgets import QTreeWidget, QMainWindow

from som_gui.icons import get_icon
from . import trigger
from som_gui import tool


class MappingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from .qt.ui_Window import Ui_Mapping
        self.ui = Ui_Mapping()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())


class ObjectTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr("Object"), self.tr("IfcMapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_object_tree()


class PropertySetTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr("PropertySet/Attribute"), self.tr("Revit-Mapping")])

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_pset_tree()
