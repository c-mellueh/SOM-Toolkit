from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PySide6.QtGui import QStandardItemModel
from som_gui.module import modelcheck
from som_gui.icons import get_icon


class ModelcheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(get_icon())
        self.vertical_layout = QVBoxLayout(self)


class ObjectCheckWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = modelcheck.widget_object_check.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())


class ObjectTree(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = QStandardItemModel()
        self.setModel(model)
        modelcheck.trigger.connect_object_check_tree(self)
        model.setHorizontalHeaderLabels(["Objekt", "Identifier"])

    def paintEvent(self, event):
        super().paintEvent(event)
        modelcheck.trigger.paint_object_tree()


class PsetTree(QTreeView):
    pass
