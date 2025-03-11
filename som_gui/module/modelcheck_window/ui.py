from __future__ import annotations

from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QTreeView, QWidget

from som_gui.module import modelcheck_window
from som_gui.resources.icons import get_icon
from . import qt


class ModelcheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = qt.ui_Widget.Ui_Modelcheck()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())


class ClassTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels([self.tr("Class"), self.tr("Identifier")])
        modelcheck_window.trigger.connect_class_check_tree(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_class_tree(self)


class PsetTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        model.setHorizontalHeaderLabels([self.tr("PropertySet,Property")])
        modelcheck_window.trigger.connect_pset_check_tree(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck_window.trigger.paint_pset_tree(self)
