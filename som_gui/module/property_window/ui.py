from __future__ import annotations

from PySide6.QtCore import (
    QAbstractTableModel,
    QSortFilterProxyModel,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtWidgets import QWidget, QWidget, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPalette, QIcon

from som_gui.resources.icons import get_icon, get_link_icon
import SOMcreator
from . import trigger
from som_gui import tool


class PropertyWindow(QWidget):
    closed = Signal()
    def __init__(self, som_property: SOMcreator.SOMProperty, *args, **kwargs):
        from .qt.ui_Window import Ui_PropertyWindow

        super().__init__(*args, **kwargs)
        self.setWindowIcon(get_icon())
        self.ui = Ui_PropertyWindow()
        self.ui.setupUi(self)
        self.som_property = som_property
        self.initial_fill = True
        trigger.window_created(self)

    def enterEvent(self, event):
        trigger.update_window(self)
        return super().enterEvent(event)

    def closeEvent(self, event):
        self.closed.emit()
        return super().closeEvent(event)


class ValueView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.som_property: SOMcreator.SOMProperty = None

    def model(self) -> SortModel:
        return super().model()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            trigger.paste_clipboard(self)
        else:
            return super().keyPressEvent(event)

class ValueModel(QAbstractTableModel):

    def __init__(self, som_property: SOMcreator.SOMProperty, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.som_property: SOMcreator.SOMProperty = som_property
        self.column_count = 1
        self.row_count = len(self.som_property.all_values)
        self.ignored_values = set()
        self.inherited_values = set()
        self._values = list()
        self.link_item = get_link_icon()
        self.update_values()
        self.dataChanged.connect(lambda x, y, z: self.update_values())

    def update_values(self):
        self._values = list(self.som_property.all_values)
        self.row_count = len(self.values)
        self.ignored_values = {
            v for v in self.values if self.som_property.is_value_ignored(v)
        }
        self.is_identifier = self.som_property.is_identifier()
        self.inherited_values = {
            v for v in self.values if self.som_property.is_value_inherited(v)
        }

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    @property
    def values(self) -> list:
        return self._values

    def is_value_ignored(self, v):
        return v in self.ignored_values

    def data(self, index: QModelIndex, role):
        row = index.row()
        value = self.values[row]
        palette = QPalette()

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return str(value)

        if role == Qt.ItemDataRole.ForegroundRole:
            if self.is_value_ignored(value):
                return tool.Util.get_greyed_out_brush()
            else:
                return tool.Util.get_standard_text_brush()

        if role == Qt.ItemDataRole.DecorationRole:
            if self.is_value_inherited(value):
                return self.link_item
            else:
                return QIcon()

        if role == Qt.ItemDataRole.BackgroundRole:
            return palette.mid() if self.is_identifier else palette.base()
        return None

    def get_own_value_index(self, row: int):
        all_values = self.som_property.all_values
        inherit_row_count = len([v for v in all_values if self.is_value_inherited(v)])
        if 0 <= row < inherit_row_count:
            return None
        return row - inherit_row_count

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if role != Qt.ItemDataRole.EditRole:
            return False

        old_value_row = self.get_own_value_index(index.row())
        self.som_property._own_values[old_value_row] = value
        self.dataChanged.emit(index, index, [role])
        return True

    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        value = self.values[index.row()]

        if self.is_value_inherited(value):
            flags &= ~Qt.ItemFlag.ItemIsEditable
        else:
            flags |= Qt.ItemFlag.ItemIsEditable

        flags |= Qt.ItemFlag.ItemIsSelectable
        return flags

    def insertRow(self, row, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.som_property.add_value("")
        self.update_values()
        self.endInsertRows()

    def removeRow(self, row, parent=QModelIndex()):
        own_value_row = self.get_own_value_index(row)
        if own_value_row is None:
            return
        self.beginRemoveRows(parent, row, row)
        self.som_property._own_values.pop(own_value_row)
        self.update_values()
        self.endRemoveRows()

    def append_row(self):
        self.insertRow(self.rowCount())

    def is_value_inherited(self, value):
        return value in self.inherited_values


class SortModel(QSortFilterProxyModel):
    def __init__(self, som_property: SOMcreator.SOMProperty, *args, **kwargs):
        self.som_property = som_property
        super().__init__(*args, **kwargs)

    def sourceModel(self) -> ValueModel:
        return super().sourceModel()
