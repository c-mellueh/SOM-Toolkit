from __future__ import annotations
import logging

from PySide6.QtCore import (
    QAbstractTableModel,
    QCoreApplication,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTableView
import SOMcreator
from som_gui import tool

class ProjectView(QTableView):
    update_requested = Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

    def enterEvent(self, event):
        self.update_requested.emit()
        return super().enterEvent(event)

class ProjectModel(QAbstractTableModel):
    data_changed_externally = Signal()
    checkstate_changed = Signal()
    def __init__(self,project:SOMcreator.SOMProject,*args,**kwargs):
        self.project = project
        self.old_column_count = self.columnCount()
        self.old_row_count = self.rowCount()
        super().__init__(*args,**kwargs)

    def update_data(self):
        self.dataChanged.emit(
        self.createIndex(0, 0),
        self.createIndex(self.rowCount(), self.columnCount()),
        )
        if self.was_data_changed_externally():
            self.data_changed_externally.emit()

    def was_data_changed_externally(self):
        changed_externally = False
        if (            self.last_col_count != self.columnCount()
            or self.last_row_count != self.rowCount()
        ):
            changed_externally = True
        self.last_col_count = self.columnCount()
        self.last_row_count = self.rowCount()
        return changed_externally

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
        self.project.set_filter_state(phase, usecase, bool(value))
        self.checkstate_changed.emit()
        return True
        #TODO write connector for update class tree and psettable
    
    def headerData(self, section:int, orientation:Qt.Orientation, role=...):
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