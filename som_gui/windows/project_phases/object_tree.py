from PySide6.QtWidgets import QTreeView, QWidget
from PySide6.QtGui import QMouseEvent,QStandardItemModel
from PySide6.QtCore import Qt, QModelIndex


class ObjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.is_already_pressed = False
        self.check_state = None
        self.title_count = 2

    def mousePressEvent(self, event: QMouseEvent):
        index = self.indexAt(event.pos())

        if index is None:
            return
        if index.column() <self.title_count:
            super().mousePressEvent(event)
            return
        old_check_state = index.data(Qt.ItemDataRole.CheckStateRole)
        new_check_state = Qt.CheckState.Unchecked if old_check_state in (
        2, Qt.CheckState.Checked) else Qt.CheckState.Checked
        self.model().setData(index, new_check_state, Qt.ItemDataRole.CheckStateRole)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if not self.is_already_pressed:
            self.is_already_pressed = True
            index = self.indexAt(event.pos())
            cs = index.data(Qt.ItemDataRole.CheckStateRole)
            self.check_state = cs
            return
        index: QModelIndex = self.indexAt(event.pos())
        if index.column() < self.title_count:
            return
        if self.check_state is None or index.model() is None:
            return
        if not self.model().itemFromIndex(index).isEnabled():
            return
        self.model().setData(index, self.check_state, Qt.ItemDataRole.CheckStateRole)

    def model(self) -> QStandardItemModel:
        return super().model()
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.is_already_pressed = False
        self.check_state = None
