from __future__ import annotations

from PySide6.QtWidgets import QTreeView, QTreeWidget, QWidget

from som_gui.module import class_tree
from som_gui.resources.icons import get_icon
import logging
from typing import TYPE_CHECKING
from PySide6.QtCore import (
    QAbstractItemModel,
    QSortFilterProxyModel,
    QModelIndex,
    Qt,
    Signal,
    QObject
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTreeView
import SOMcreator
from som_gui import tool

class ClassTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        class_tree.trigger.repaint_event(self)

    def dropEvent(self, event):
        class_tree.trigger.drop_event(event,self)
        super().dropEvent(event)

    def mimeData(self, items):
        mime_data = super().mimeData(items)
        return class_tree.trigger.create_mime_data(list(items), mime_data)

class ClassView(QTreeView):
    update_requested = Signal()
    mouse_moved = Signal(QMouseEvent,QObject)
    mouse_released = Signal(QMouseEvent,QObject)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTreeView.SelectionMode.SingleSelection)

    def enterEvent(self, event):
        self.update_requested.emit()
        return super().enterEvent(event)

    # for Typehints
    def model(self) -> ClassModel:
        return super().model()

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
        self.mouse_moved.emit(event,self)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.mouse_released.emit(event,self)

class ClassModel(QAbstractItemModel):
    updated_required = Signal()
    resize_required = Signal(QModelIndex)

    def __init__(self, project: SOMcreator.SOMProject, *args, **kwargs):
        self.project = project
        self.root_classes = list()
        #(name getter, value_getter, value_setter)
        self.columns: list[tuple[callable,callable,callable]] = list()
        self.column_count = len(self.columns)

        self.class_index_dict: dict[SOMcreator.SOMClass, QModelIndex] = dict()
        self.old_column_count = self.column_count
        self.row_count_dict: dict[QModelIndex, int] = dict()
        super().__init__(*args, **kwargs)
        self.update_data()

    def update_data(self):
        columns = list()
        for use_case in self.project.get_usecases():
            for phase in self.project.get_phases():
                if self.project.get_filter_state(phase, use_case):
                    columns.append((use_case, phase))
        self.columns = columns
        self.column_count = len(self.columns) + self.fixed_column_count
        self.root_classes = list(self.project.get_root_classes(filter=False))


    def headerData(self, section, orientation, /, role = ...):
        if role in (Qt.ItemDataRole.DisplayRole,Qt.ItemDataRole.EditRole) and orientation == Qt.Orientation.Horizontal:
            return self.columns[section][0]()
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        """
        make Item Checkable if Column > check_column_index
        Disable Item if Parent is not checked or parent is disabled
        """
        flags = super().flags(index)
        parent_index = self.parent(index).siblingAtColumn(index.column())
        if index.column() >= self.fixed_column_count:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        if not parent_index.isValid():
            return flags
        is_parent_enabled = Qt.ItemFlag.ItemIsEnabled in parent_index.flags()
        parent_cs = parent_index.data(Qt.ItemDataRole.CheckStateRole)
        is_parent_checked = tool.Util.checkstate_to_bool(parent_cs)
        if not (is_parent_enabled and is_parent_checked):
            flags &= ~Qt.ItemFlag.ItemIsEnabled
        return flags

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def get_row_count(self, parent=QModelIndex()):
        if not parent.isValid():
            result = len(self.root_classes)
        else:
            som_class: SOMcreator.SOMClass = parent.internalPointer()
            result = len(som_class._children)
        return result

    def rowCount(self, parent=QModelIndex()):
        result = self.get_row_count(parent)
        old_result = self.row_count_dict.get(parent)
        if old_result != result and old_result is not None:
            logging.debug(f"RowCount emits Resize Required")
            self.resize_required.emit(parent)
        if old_result is None:
            self.row_count_dict[parent] = result
        return result

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid():
            return None

        som_class: SOMcreator.SOMClass = index.internalPointer()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            result = self.get_text(index.column(), som_class)
            return result
        elif role == Qt.ItemDataRole.CheckStateRole:
            return self.get_checkstate(index.column(), som_class)
        return None

    def get_checkstate(self, column: int, som_class: SOMcreator.SOMClass):
        if column < self.fixed_column_count:
            return None
        if column - self.fixed_column_count >= len(self.columns):
            return None
        usecase, phase = self.columns[column - self.fixed_column_count]
        return tool.Util.bool_to_checkstate(som_class.get_filter_state(phase, usecase))

    def get_text(self, column: int, som_class: SOMcreator.SOMClass):
        if column == 0:
            return som_class.name
        elif column == 1:
            return som_class.ident_value if not som_class.is_concept else ""
        else:
            return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid():
            return False
        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        if index.column() < self.fixed_column_count:
            return False
        som_class: SOMcreator.SOMClass = index.internalPointer()
        usecase, phase = self.columns[index.column() - self.fixed_column_count]
        som_class.set_filter_state(phase, usecase, bool(value))
        return True

    def index(self, row: int, column: int, parent: QModelIndex):
        if not parent.isValid():
            if row >= len(self.root_classes):
                logging.debug("Index Exmits resize Required")
                self.resize_required.emit(parent)
                return QModelIndex()
            som_class = self.root_classes[row]
            index = self.createIndex(row, column, som_class)
            logging.debug(f"Index: {row}:{column} -> BASE -> {som_class.name}")
            return index
        else:
            parent = parent.siblingAtColumn(0)
            som_class: SOMcreator.SOMClass = parent.internalPointer()
            logging.debug(f"Index: {row}:{column} -> {som_class.name}")

            children = list(som_class.get_children(filter=False))
            if 0 <= row < len(children):
                child_class = children[row]
                index = self.createIndex(row, column, child_class)
                return index
            else:
                logging.debug("Index Exmits resize Required")
                self.resize_required.emit(parent)

        return QModelIndex()

    def createIndex(self, row, column, pointer=None):
        index = super().createIndex(row, column, pointer)
        if pointer is not None:
            self.class_index_dict[pointer] = index
        return index

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        som_class: SOMcreator.SOMClass = index.internalPointer()
        if som_class is None or not som_class.is_child:
            return QModelIndex()
        parent_class = som_class.parent
        parent_index = self.class_index_dict.get(parent_class)
        if parent_index is None or not parent_index.isValid():
            return QModelIndex()
        if parent_index.column() > self.fixed_column_count:
            return parent_index.siblingAtColumn(0)
        return parent_index



class ClassFilterModel(QSortFilterProxyModel):
    def __init__(self, fixed_column_count: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixed_column_count = fixed_column_count

    def filterAcceptsColumn(self, source_column, source_parent):
        res = source_column < self.fixed_column_count
        return res
