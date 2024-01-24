from PySide6.QtWidgets import QTableWidget, QWidget, QLineEdit, QDialog, QStyledItemDelegate
from PySide6.QtCore import Qt, Signal, QModelIndex
from PySide6 import QtGui
from som_gui.module import property_set
from .window import Ui_layout_main
from .ui_predefined_pset import Ui_Dialog
from som_gui.icons import get_icon


class PsetTableWidget(QTableWidget):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.customContextMenuRequested.connect(property_set.trigger.pset_table_context_menu_requested)
        self.setItemDelegate(LineEditDelegate(self))

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_event()


class PropertySetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_layout_main()
        self.widget.setupUi(self)
        self.widget.verticalLayout_2.setSpacing(2)
        self.widget.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.widget.verticalLayout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWindowIcon(get_icon())

    def closeEvent(self, event):
        super().closeEvent(event)
        property_set.trigger.close_pset_window(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        property_set.trigger.repaint_pset_window(self)


class LineInput(QLineEdit):
    def __init__(self) -> None:
        super(LineInput, self).__init__()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if property_set.trigger.key_press_event(event, self.window()):
            super().keyPressEvent(event)


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
        property_set.trigger.repaint_predefined_pset_window()

    def accept(self):
        property_set.trigger.predefined_pset_window_accept()


class LineEditDelegate(QStyledItemDelegate):
    """A delegate that allows the user to change integer values from the model
       using a spin box widget. """
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_stopped.connect(parent.edit_stopped)
        self.edit_started.connect(parent.edit_started)

    def createEditor(self, parent, option, index):
        self.edit_started.emit(index)
        editor: QLineEdit = super().createEditor(parent, option, index)
        editor.textChanged.connect(lambda text: property_set.trigger.pset_name_changed(text, index))
        return editor

    def destroyEditor(self, editor, index):
        self.edit_stopped.emit(index)
        return super().destroyEditor(editor, index)
