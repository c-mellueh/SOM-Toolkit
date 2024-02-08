from PySide6.QtWidgets import QTableWidget, QWidget, QDialog, QStyledItemDelegate, QLineEdit
from PySide6.QtCore import Signal, QModelIndex
from som_gui.module import predefined_property_sets
from .window import Ui_Dialog
from som_gui.icons import get_icon


class PsetTableWidget(QTableWidget):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.customContextMenuRequested.connect(predefined_property_sets.trigger.context_menu_requested)
        self.setItemDelegate(LineEditDelegate(self))

    def paintEvent(self, event):
        super().paintEvent(event)
        predefined_property_sets.trigger.repaint_window()


class PredefinedPropertySetWindow(QDialog):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self):
        super().__init__()
        self.widget = Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Vordefinierte PropertySets")
        self.widget.list_view_pset.setItemDelegate(LineEditDelegate(self))

    def paintEvent(self, event):
        super().paintEvent(event)
        predefined_property_sets.trigger.repaint_window()

    def accept(self):
        predefined_property_sets.trigger.accept()


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
        editor: QLineEdit = super().createEditor(parent, option, index)
        editor.textChanged.connect(lambda text: predefined_property_sets.trigger.edit_name(text, index))
        return editor

    def destroyEditor(self, editor, index):
        self.edit_stopped.emit(index)
        return super().destroyEditor(editor, index)
