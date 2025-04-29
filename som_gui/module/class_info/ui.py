from PySide6.QtWidgets import (
    QDialog,
    QItemDelegate,
    QComboBox,
    QLineEdit,
    QCompleter,
    QStyledItemDelegate,
)
from PySide6.QtCore import QModelIndex, Qt
from som_gui.module import class_tree
from som_gui.resources.icons import get_icon
from .qt.ui_InfoWidget import Ui_ClassInfo
from . import trigger
from som_gui import tool


class ClassInfoDialog(QDialog):
    def __init__(self):
        super(ClassInfoDialog, self).__init__()
        self.ui = Ui_ClassInfo()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        trigger.class_info_paint_event()
        super().paintEvent(event)


class Delegate(QStyledItemDelegate):
    def __init__(self, versions, *args, **kwargs):
        self.versions = versions
        super().__init__(*args, **kwargs)

    def createEditor(self, parent, option, index: QModelIndex):
        if index.column() == 0:
            classes = set()
            for version in self.versions:
                classes.update(
                    set(tool.IfcSchema.get_all_classes(version, "IfcProduct"))
                )
            widget = QLineEdit(parent)
            widget.setCompleter(QCompleter(sorted(classes)))
        else:
            t = index.siblingAtColumn(0).data(Qt.ItemDataRole.DisplayRole)
            widget = QComboBox(parent)
            types = set()
            for version in self.versions:
                types.update(set(tool.IfcSchema.get_predefined_types(t, version)))
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
