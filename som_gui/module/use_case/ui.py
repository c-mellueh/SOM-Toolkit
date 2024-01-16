from __future__ import annotations
from som_gui import MainUi
from PySide6.QtWidgets import QWidget
import som_gui.module.use_case as use_case
from som_gui import icons
from som_gui.core import use_case as core
from som_gui.tool.use_case import UseCase


class UseCaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = use_case.window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())


def load_triggers():
    MainUi.ui.action_use_cases.triggered.connect(
        use_case.operator.menu_action_use_cases
    )


from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeView, QWidget
from PySide6.QtGui import QMouseEvent, QStandardItemModel
from PySide6.QtCore import Qt, QModelIndex
from SOMcreator import classes


CLASS_REFERENCE = Qt.ItemDataRole.UserRole + 1
OBJECT_TITLES = ["Objekt", "Identifier"]
PSET_TITLES = ["PropertySet, Attribut"]


def resize_tree_view(tree: QTreeView):
    columns = tree.model().columnCount()
    for index in range(columns):
        tree.resizeColumnToContents(index)


def resize_tree(tree: QTreeView):
    for index in range(tree.model().columnCount()):
        tree.resizeColumnToContents(index)


class ObjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.is_already_pressed = False
        self.check_state = None
        self.title_count = 2

    def paintEvent(self, event):
        super().paintEvent(event)
        use_case.operator.refresh_object_tree()

    def mousePressEvent(self, event: QMouseEvent):
        index = self.indexAt(event.pos())
        if core.object_tree_mouse_press_event(index, UseCase):
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        core.object_tree_mouse_move_event(self.indexAt(event.pos()), UseCase)

    def model(self) -> QStandardItemModel:
        return super().model()

    def window(self):
        return super().window()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        core.object_tree_mouse_release_event(index, UseCase)
