from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtWidgets import QDialog, QWidget

from som_gui.module import predefined_property_set
from som_gui.module.property_set.ui import LineEditDelegate
from som_gui.resources.icons import get_icon
from .qt import ui_CompareWidget, ui_Widget


class PredefinedPropertySetWindow(QDialog):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self):
        super().__init__()
        self.ui = ui_Widget.Ui_PredefinedPset()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())
        self.ui.list_view_pset.setItemDelegate(LineEditDelegate(self))

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
        self.ui = ui_CompareWidget.Ui_PredefinedPset()
        self.ui.setupUi(self)
        self.ui.tree_widget_propertysets.setColumnCount(2)
        self.ui.table_widget_values.setColumnCount(2)
        self.ui.table_infos.setColumnCount(3)
        self.ui.table_infos.setVerticalHeaderLabels(["Name", "XXX", "XXX"])
