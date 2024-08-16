from PySide6.QtWidgets import QTableWidget, QWidget, QDialog, QStyledItemDelegate, QLineEdit
from PySide6.QtCore import Signal, QModelIndex
from som_gui.module import predefined_property_set
from .window import Ui_Dialog
from som_gui.icons import get_icon
from som_gui.module.property_set.ui import LineEditDelegate
from .compare_widget import Ui_Form

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
        predefined_property_set.trigger.repaint_window()

    def accept(self):
        predefined_property_set.trigger.accept()

    def text_changed(self, text, index):
        predefined_property_set.trigger.edit_name(text, index)


class CompareWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = Ui_Form()
        self.widget.setupUi(self)
