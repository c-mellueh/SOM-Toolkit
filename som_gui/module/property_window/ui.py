from PySide6.QtCore import (
    QAbstractTableModel,
    QSortFilterProxyModel,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtWidgets import QWidget, QWidget, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem,QPalette,QIcon

from som_gui.resources.icons import get_icon,get_link_icon
import SOMcreator
from . import trigger
from som_gui import tool

class PropertyWindow(QWidget):
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


class ValueView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.som_property: SOMcreator.SOMProperty = None


class ValueModel(QAbstractTableModel):
    values_changed = Signal()

    def __init__(self, som_property: SOMcreator.SOMProperty, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.som_property: SOMcreator.SOMProperty = som_property
        self.column_count = 1

    def rowCount(self, parent=QModelIndex()):
        return len(self.som_property.all_values)

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    @property
    def values(self) -> list:
        return self.som_property.all_values


    def data(self, index: QModelIndex, role):
        som_property = self.som_property
        row = index.row()
        value = self.values[row]
        palette = QPalette()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return str(value)
        if role == Qt.ItemDataRole.ForegroundRole:
            if self.som_property.is_value_ignored(value):
             
                return tool.Util.get_greyed_out_brush()
            else:
                return tool.Util.get_standard_text_brush()
        if role == Qt.ItemDataRole.DecorationRole:

            if value in som_property._allowed_values:
                return QIcon()
            else:
                return get_link_icon()
        
        if role == Qt.ItemDataRole.BackgroundRole:

            return palette.mid() if som_property.is_identifier() else palette.base()
        return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        row = index.row()
        if role == Qt.ItemDataRole.EditRole:
            self.som_property.all_values[row] = value
            self.dataChanged.emit(index, index, [role])
            self.values_changed.emit()
            return True
        return False

    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        value = self.values[index.row()]

        if self.som_property.is_value_ignored(value):
            flags &= ~Qt.ItemFlag.ItemIsEditable
        else:
            flags |= Qt.ItemFlag.ItemIsEditable

        flags |=Qt.ItemFlag.ItemIsSelectable
        return flags

    def insertRow(self, row, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.som_property._allowed_values.append("")
        self.endInsertRows()

    def append_row(self):
        self.insertRow(self.rowCount())


class SortModel(QSortFilterProxyModel):
    def __init__(self, som_property: SOMcreator.SOMProperty, *args, **kwargs):
        self.som_property = som_property
        super().__init__(*args, **kwargs)
