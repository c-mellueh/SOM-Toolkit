from __future__ import annotations
import logging

from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTableView
import SOMcreator
from som_gui import tool


class PropertyView(QTableView):
    update_requested = Signal()
    mouse_moved = Signal(QMouseEvent, QObject)
    mouse_released = Signal(QMouseEvent, QObject)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

    def enterEvent(self, event):
        self.update_requested.emit()
        return super().enterEvent(event)

    def update_view(self):
        model = self.model()
        if model is None:
            return
        model.dataChanged.emit(
            model.createIndex(0, 0),
            model.createIndex(model.rowCount(), model.columnCount()),
        )

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        self.mouse_moved.emit(event, self)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.mouse_released.emit(event, self)


class PropertyModel(QAbstractTableModel):
    updated_required = Signal()
    resize_required = Signal()

    def __init__(self, *args, **kwargs):
        self.fixed_column_count = 2
        self.som_class: SOMcreator.SOMClass = None
        self.columns: list[tuple[SOMcreator.UseCase, SOMcreator.Phase]] = list()
        self.column_count = len(self.columns) + self.fixed_column_count
        self.old_column_count = self.column_count
        self.old_row_count = 1
        self.properties: list[SOMcreator.SOMProperty] = list()
        super().__init__(*args, **kwargs)

    def update_data(self):
        columns = list()
        if not self.som_class:
            self.columns = list()
        else:
            project = self.som_class.project
            for use_case in project.get_usecases():
                for phase in project.get_phases():
                    if project.get_filter_state(phase, use_case):
                        columns.append((use_case, phase))

        self.columns = columns
        self.column_count = len(self.columns) + self.fixed_column_count
        self.properties = (
            list(self.som_class.get_properties(filter=False))
            if self.som_class
            else list()
        )

    def flags(self, index):
        flags = super().flags(index)
        if index.column() < self.fixed_column_count:
            return flags
        property = self.get_property_from_index(index)
        flags |= Qt.ItemFlag.ItemIsUserCheckable
        som_class = property.property_set.som_class
        usecase, phase = self.columns[index.column() - self.fixed_column_count]
        while som_class is not None:
            if not som_class.get_filter_state(phase, usecase):
                flags &= ~Qt.ItemFlag.ItemIsEnabled
                return flags
            som_class = som_class.parent
        return flags

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def rowCount(self, parent=QModelIndex()):
        return len(self.properties)

    def get_property_from_index(self, index: QModelIndex) -> SOMcreator.SOMProperty:
        return self.properties[index.row()]

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        def get_checkstate(column: int, som_property: SOMcreator.SOMProperty):
            if column < self.fixed_column_count:
                return None
            usecase, phase = self.columns[column - self.fixed_column_count]
            return tool.Util.bool_to_checkstate(
                som_property.get_filter_state(phase, usecase)
            )

        def get_text(column: int, som_property: SOMcreator.SOMProperty):
            if column == 0:
                property_set = som_property.property_set
                return None if property_set is None else property_set.name
            elif column == 1:
                return som_property.name
            else:
                return None

        if not index.isValid():
            return None

        som_property: SOMcreator.SOMProperty = self.properties[index.row()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            result = get_text(index.column(), som_property)
            return result
        elif role == Qt.ItemDataRole.CheckStateRole:
            return get_checkstate(index.column(), som_property)
        return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid():
            return False
        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        if index.column() < self.fixed_column_count:
            return False
        som_property = self.get_property_from_index(index)
        usecase, phase = self.columns[index.column() - self.fixed_column_count]
        som_property.set_filter_state(phase, usecase, bool(value))
        return True
