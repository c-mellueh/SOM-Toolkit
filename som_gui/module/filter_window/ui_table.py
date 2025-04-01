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
from . import trigger


class ProjectView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.model().update_data()

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

    def update_data(self):
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
        self.project.set_filter_state(phase, usecase, bool(value))
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

class PropertyView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)

    def enterEvent(self, event):
        super().enterEvent(event)
        from .ui import SortFilterModel
        model = self.model()
        if isinstance(model,SortFilterModel):
            model = model.sourceModel()
        model.update_data()

    def model(self) -> PropertyModel:
        return super().model()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        trigger.tree_mouse_move_event(self.indexAt(event.pos()))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        trigger.tree_mouse_release_event(index)


class PropertyModel(QAbstractTableModel):

    def __init__(self,):
        super().__init__()
        self.som_class:SOMcreator.SOMClass = None
        self.row_count = 0
        self.column_count = 2
        self.allowed_combinations = list()
        self.fixed_column_index = 2
        self.properties = list()
    def update_allowed_combinations(self):
        ac = list()
        if self.som_class is None:
            return
        project = self.som_class.project
        for use_case in project.get_usecases():
            for phase in project.get_phases():
                if project.get_filter_state(phase, use_case):
                    ac.append((use_case, phase))
        self.allowed_combinations = ac

    def update_data(self):
        if self.som_class is None:
            return
        self.update_allowed_combinations()
        self.row_count = len(self.som_class.get_properties(filter = False))
        self.column_count = len(self.allowed_combinations)
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
        )

    def set_class(self,som_class:SOMcreator.SOMClass):
        self.som_class = som_class
        self.properties = list(som_class.get_properties(filter = False))
        self.update_data()

    def flags(self, index:QModelIndex):
        flags = super().flags(index)
        if index.column() <self.fixed_column_index:
            return flags
        return flags | Qt.ItemFlag.ItemIsUserCheckable

    def rowCount(self, parent=None):
        return self.row_count

    def columnCount(self, parent=None):
        return self.column_count

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if self.som_class is None:
            return None
        som_property = self.properties[index.row()]
        if index.column() == 0:
            if role == Qt.ItemDataRole.DisplayRole:
                return som_property.property_set.name
        elif index.column() == 1:
            if role == Qt.ItemDataRole.DisplayRole:
                return som_property.name
        else:
            usecase,phase = self.allowed_combinations[index.column()]
            if role == Qt.ItemDataRole.CheckStateRole:
                state = som_property.get_filter_state(phase,usecase)
                return tool.Util.bool_to_checkstate(state)
        return None

    def setData(self, index: QModelIndex, value, role=...):
        if self.som_class is None:
            return False
        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        usecase,phase = self.allowed_combinations[index.column()]
        som_property = self.properties[index.row()]
        som_property.set_filter_state(phase, usecase, bool(value))
        return True
