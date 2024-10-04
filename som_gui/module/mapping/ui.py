from PySide6.QtWidgets import QTreeWidget, QMainWindow

from som_gui.icons import get_icon
from . import trigger
from som_gui import tool


class MappingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from .qt.window import Ui_Form
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
