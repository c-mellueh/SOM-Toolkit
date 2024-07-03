from PySide6.QtWidgets import QTableWidget, QWidget, QStyledItemDelegate
from PySide6.QtCore import Signal, QModelIndex, Qt
from som_gui.module import property_set


class PsetTableWidget(QTableWidget):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.customContextMenuRequested.connect(property_set.trigger.pset_table_context_menu_requested)
        self.setItemDelegate(LineEditDelegate(self))
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_event()

    def text_changed(self, text, index):
        property_set.trigger.edit_name(text, index)


class LineEditDelegate(QStyledItemDelegate):
    """Stops updating Table Enties"""
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_stopped.connect(parent.edit_stopped)
        self.edit_started.connect(parent.edit_started)

    def createEditor(self, parent, option, index):
        self.edit_started.emit(index)
        editor = super().createEditor(parent, option, index)
        editor.textChanged.connect(lambda text: self.parent().text_changed(text, index))
        return editor

    def destroyEditor(self, editor, index):
        self.edit_stopped.emit(index)
        return super().destroyEditor(editor, index)
