from __future__ import annotations
from som_gui import icons
from som_gui.core import object_filter as core
from som_gui import tool
from PySide6.QtWidgets import QTreeView, QWidget
from PySide6.QtGui import QMouseEvent
from som_gui.module import object_filter
from .qt import settings
class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = settings.Ui_Form()
        self.ui.setupUi(self)
        object_filter.trigger.settings_widget_created(self)


class ObjectFilterWindow(QWidget):
    def __init__(self):
        from .qt import widget
        super().__init__()
        self.widget = widget.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle(f"Anwendungsfälle | {tool.Util.get_status_text()}")

class ObjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        object_filter.trigger.refresh_object_tree()

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
