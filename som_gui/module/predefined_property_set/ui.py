from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Signal, QModelIndex
from som_gui.module import predefined_property_set
from som_gui.icons import get_icon
from som_gui.module.property_set.ui import LineEditDelegate
from som_gui import tool
from .qt import compare_widget, widget


class PredefinedPropertySetWindow(QDialog):
    edit_started = Signal(QModelIndex)
    edit_stopped = Signal(QModelIndex)

    def __init__(self):
        super().__init__()
        self.widget = widget.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(f"Vordefinierte PropertySets | {tool.Util.get_status_text()}")
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
        self.widget = compare_widget.Ui_Form()
        self.widget.setupUi(self)
        self.widget.tree_widget_propertysets.setColumnCount(2)
        self.widget.table_widget_values.setColumnCount(2)
        self.widget.table_infos.setColumnCount(3)
        self.widget.table_infos.setVerticalHeaderLabels(["Name", "XXX", "XXX"])
