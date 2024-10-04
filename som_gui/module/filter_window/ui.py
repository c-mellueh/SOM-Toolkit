from random import triangular

from PySide6.QtWidgets import QTableWidget, QDialog, QTreeView, QWidget
from som_gui.icons import get_icon
import som_gui.module.project_filter as project_filter
from PySide6.QtCore import Qt
from som_gui import tool
import som_gui
from . import trigger


class FilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .qt import widget
        self.ui = widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())
        self.setWindowTitle(f"Projekt Filter {tool.Util.get_status_text()}")


class ProjectTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.pt_update()


class ObjectTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #
    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     object_filter.trigger.refresh_object_tree()
    #
    # def mousePressEvent(self, event: QMouseEvent):
    #     index = self.indexAt(event.pos())
    #     if core.tree_mouse_press_event(index, tool.ObjectFilter):
    #         super().mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     super().mouseMoveEvent(event)
    #     core.tree_mouse_move_event(self.indexAt(event.pos()), tool.ObjectFilter)
    #
    # def mouseReleaseEvent(self, event):
    #     super().mouseReleaseEvent(event)
    #     index = self.indexAt(event.pos())
    #     core.tree_mouse_release_event(index, tool.ObjectFilter)


class PsetTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
