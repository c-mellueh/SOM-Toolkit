from __future__ import annotations
import som_gui.module.object_filter as object_filter
from som_gui import icons
from som_gui.core import object_filter as core
from som_gui import tool
from som_gui.tool.project import Project
from PySide6.QtWidgets import QTreeView, QWidget
from PySide6.QtGui import QMouseEvent


class ObjectFilterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = object_filter.window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())


class ObjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        core.refresh_object_tree(tool.ObjectFilter, Project)

    def mousePressEvent(self, event: QMouseEvent):
        index = self.indexAt(event.pos())
        if core.tree_mouse_press_event(index, tool.ObjectFilter):
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        core.tree_mouse_move_event(self.indexAt(event.pos()), tool.ObjectFilter)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        core.tree_mouse_release_event(index, tool.ObjectFilter)
