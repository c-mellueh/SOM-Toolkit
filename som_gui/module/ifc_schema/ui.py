from PySide6.QtWidgets import (
    QWidget,
    QStyledItemDelegate,
    QLineEdit,
    QCompleter,
    QComboBox,
)
from PySide6.QtCore import QModelIndex, Qt
from .qt.ui_MappingWidget import Ui_MappingWidget
from . import trigger
import SOMcreator
from som_gui import tool
from SOMcreator.datastructure import ifc_schema

class MappingWidget(QWidget):
    def __init__(self, version, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.ui = Ui_MappingWidget()
        self.ui.setupUi(self)
        trigger.mapping_widget_created(self)

    def paintEvent(self, event):
        tv = self.ui.table_view
        width = tv.columnWidth(0) + tv.columnWidth(1)
        tv.setColumnWidth(0, width / 2 - 3)
        return super().paintEvent(event)


class MappingDelegate(QStyledItemDelegate):
    def __init__(self, version, *args, **kwargs):
        self.version = version
        super().__init__(*args, **kwargs)

    def createEditor(self, parent, option, index: QModelIndex):
        if index.column() == 0:
            classes = ifc_schema.get_all_classes(self.version, "IfcProduct")

            widget = QLineEdit(parent)
            widget.setCompleter(QCompleter(sorted(classes)))
        else:
            t = index.siblingAtColumn(0).data(Qt.ItemDataRole.DisplayRole)
            widget = QComboBox(parent)
            types = ifc_schema.get_predefined_types(t, self.version)
            pdt = [""] + sorted(types)
            widget.addItems(pdt)
            widget.setEditable(True)
            widget.setCompleter(QCompleter(types))
        return widget

    def setEditorData(self, editor, index):
        if index.column() == 0:
            editor.setText(index.data(Qt.EditRole))
        else:
            value = index.data(Qt.EditRole)
            if value:
                i = editor.findText(value)
                if i >= 0:
                    editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index):
        if index.column() == 0:
            value = editor.text()
        else:
            value = editor.currentText()
        model.setData(index, value, Qt.EditRole)
