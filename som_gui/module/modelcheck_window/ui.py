from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PySide6.QtGui import QStandardItemModel, QMouseEvent
from som_gui.module import modelcheck_window
from som_gui.icons import get_icon
from som_gui import tool
from . import qt

class ModelcheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = qt.widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(f"Modellprüfung | {tool.Util.get_status_text()}")

class ObjectCheckWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = modelcheck_window.widget_object_check.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())


class ObjectTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels(["Objekt", "Identifier"])

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_object_tree()

class PsetTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels(["PropertySet,Attribut"])
        modelcheck_window.trigger.connect_pset_check_tree(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_pset_tree()
