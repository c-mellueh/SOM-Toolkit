from __future__ import annotations
from PySide6.QtWidgets import QWidget, QTreeView
from PySide6.QtGui import QStandardItemModel
from som_gui.module import modelcheck_window
from som_gui.ressources.icons import get_icon
from . import qt


class ModelcheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = qt.ui_Widget.Ui_Modelcheck()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

class ObjectTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels(["Object", "Identifier"])
        modelcheck_window.trigger.connect_object_check_tree(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_object_tree(self)


class PsetTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels(["PropertySet,Attribute"])
        modelcheck_window.trigger.connect_pset_check_tree(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_pset_tree(self)
