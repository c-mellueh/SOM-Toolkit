from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING


from PySide6.QtCore import (
    QAbstractItemModel,
    QAbstractTableModel,
    QCoreApplication,
    QSortFilterProxyModel,
    QModelIndex,
    Qt,
    Signal,
    QSize,
    QRect,
    QPoint,
)
    
from PySide6.QtGui import QMouseEvent, QColor, QPainter, QPalette, QBrush,QPaintEvent
from PySide6.QtWidgets import (
    QTableView,
    QTreeView,
    QWidget,
    QHeaderView,
    QStyleOptionHeader,
    QStyle,
)
import SOMcreator
import som_gui
from som_gui import tool
from . import trigger

if TYPE_CHECKING:
    from .ui_header import CustomHeaderView



class ProjectView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.model().update()

    def model(self) -> ProjectModel:
        return super().model()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        trigger.tree_mouse_move_event(self.indexAt(event.pos()))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        trigger.tree_mouse_release_event(index)

class ProjectModel(QAbstractTableModel):
    data_changed_externally = Signal()

    def __init__(self, project: SOMcreator.SOMProject):
        super().__init__()
        self.project = project
        self.check_column_index = 0
        self.last_col_count = self.columnCount()
        self.last_row_count = self.rowCount()

    def update(self):
        logging.debug(
            f"Update FilterView rowCount: {self.rowCount()} columnCount: {self.columnCount()}"
        )
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
        )

        if (
            self.last_col_count != self.columnCount()
            or self.last_row_count != self.rowCount()
        ):
            self.data_changed_externally.emit()

        self.last_col_count = self.columnCount()
        self.last_row_count = self.rowCount()

    def flags(self, index):
        flags = super().flags(index)
        return flags | Qt.ItemFlag.ItemIsUserCheckable

    def rowCount(self, parent=None):
        return len(self.project.get_phases())

    def columnCount(self, parent=None):
        return len(self.project.get_usecases())

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.CheckStateRole:
            state = self.project.get_filter_matrix()[index.row()][index.column()]
            return tool.Util.bool_to_checkstate(state)
        return None

    def setData(self, index: QModelIndex, value, role=...):
        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        phase = self.project.get_phase_by_index(index.row())
        usecase = self.project.get_usecase_by_index(index.column())
        self.project.set_filter_state(phase,usecase,bool(value))
        trigger.update_class_tree()
        trigger.update_pset_tree()
        return True

    def headerData(self, section, orientation, role=...):
        if role not in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return
        if orientation == Qt.Orientation.Horizontal:
            if section > len(self.project.get_usecases()) - 1:
                return None
            return self.project.get_usecases()[section].name
        else:
            if section > len(self.project.get_phases()) - 1:
                return None
            return self.project.get_phases()[section].name

    def insertRows(self, row, count, parent=None):
        logging.debug("Insert Rows")
        text = QCoreApplication.translate("FilterWindow", "New Phase")
        new_name = tool.Util.get_new_name(
            text, [ph.name for ph in self.project.get_phases()]
        )
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        phase = SOMcreator.Phase(new_name, new_name, new_name)
        self.project.add_phase(phase)
        self.endInsertRows()

