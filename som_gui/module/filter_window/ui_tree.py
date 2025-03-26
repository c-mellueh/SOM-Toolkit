from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTreeView

import SOMcreator
from som_gui import tool
from . import trigger

if TYPE_CHECKING:
    from .ui_header import CustomHeaderView


class FilterTreeView(QTreeView):
    def __init__(self, parent, mode):
        super().__init__(parent)
        self.mode = mode

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        trigger.tree_mouse_move_event(self.indexAt(event.pos()))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        trigger.tree_mouse_release_event(self.indexAt(event.pos()))

    def header(self) -> CustomHeaderView:
        return super().header()


class ClassTreeView(FilterTreeView):
    def __init__(self, mode, parent=None):
        super().__init__(parent, mode)

    def enterEvent(self, event):
        trigger.update_class_tree()
        super().enterEvent(event)

    def model(self) -> ClassModel:
        return super().model()


class PsetTreeView(FilterTreeView):
    def __init__(self, mode, parent=None):
        super().__init__(parent, mode)

    def enterEvent(self, event):
        trigger.update_pset_tree()
        super().enterEvent(event)

    def model(self) -> PsetModel:
        return super().model()


class TreeModel(QAbstractItemModel):
    def __init__(self, project: SOMcreator.SOMProject, first_column_functions):
        """
        :param: check_column_index = Index of the first column which will contain checkData
        """
        super().__init__()
        self.project = project
        self.update_allowed_combinations()
        self.check_column_index = len(first_column_functions)
        self.column_count = 0
        self.update_data()
        self.first_column_functions = first_column_functions

    def update_data(self):
        self.allowed_combinations = self.allowed_combinations
        self.column_count = self.check_column_index + len(self.allowed_combinations)

        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
        )

    def flags(self, index: QModelIndex, parent_index: QModelIndex):
        """
        make Item Checkable if Column > check_column_index
        Disable Item if Parent is not checked or parent is disabled
        """
        flags = super().flags(index)
        if index.column() >= self.check_column_index:
            flags |= Qt.ItemFlag.ItemIsUserCheckable

        if not parent_index.isValid():
            return flags
        if index.column() < self.check_column_index:
            return flags
        is_parent_enabled = Qt.ItemFlag.ItemIsEnabled in parent_index.flags()
        cs = parent_index.data(Qt.ItemDataRole.CheckStateRole)
        is_parent_checked = tool.Util.checkstate_to_bool(cs)
        if not (is_parent_enabled and is_parent_checked):
            flags &= ~Qt.ItemFlag.ItemIsEnabled
        return flags

    def update_allowed_combinations(self):
        self.allowed_combinations = list()
        for use_case in self.project.get_usecases():
            for phase in self.project.get_phases():
                if self.project.get_filter_state(phase, use_case):
                    self.allowed_combinations.append((use_case, phase))

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    # Returns the data to be displayed for each cell
    def data(
        self,
        index,
        role=Qt.ItemDataRole.DisplayRole,
    ):
        if not index.isValid():
            return None
        node: SOMcreator.SOMClass = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            for col, getter_function in enumerate(self.first_column_functions):
                if index.column() == col:
                    return getter_function(node)

        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() >= self.check_column_index:
                pos = index.column() - self.check_column_index
                if pos >= len(self.allowed_combinations):
                    return None
                usecase, phase = self.allowed_combinations[pos]
                return tool.Util.bool_to_checkstate(
                    node.get_filter_state(phase, usecase)
                )
        return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid() or role != Qt.ItemDataRole.CheckStateRole:
            return False
        node: (
            SOMcreator.SOMClass | SOMcreator.SOMProperty | SOMcreator.SOMPropertySet
        ) = index.internalPointer()
        logical_position = index.column() - self.check_column_index
        if logical_position >= len(self.allowed_combinations):
            return False
        usecase, phase = self.allowed_combinations[logical_position]
        logging.debug(f"Set {node} {phase.name}:{usecase.name} to {bool(value)}")
        node.set_filter_state(phase, usecase, bool(value))
        trigger.update_class_tree()
        trigger.update_pset_tree()
        return True


class ClassModel(TreeModel):
    def __init__(self, project: SOMcreator.SOMProject):
        getter_funcs = [
            lambda o: getattr(o, "name"),
            lambda o: getattr(o, "ident_value"),
        ]
        super().__init__(project, getter_funcs)
        self.root_classes = list(self.project.get_root_classes(filter=False))

    def flags(self, index: QModelIndex):
        parent_index = self.parent(index)
        parent_sibling = parent_index.sibling(parent_index.row(), index.column())
        return super().flags(index, parent_sibling)

    def update_data(self):
        """
        updates root_classes so that you dont need to call get_root_classes on every instance between paint events
        """
        self.root_classes = list(self.project.get_root_classes(filter=False))
        super().update_data()

    # Returns the number of children (rows) under the given index
    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.root_classes)  # Top-level items
        node: SOMcreator.SOMClass = parent.internalPointer()
        count = len(
            list(node.get_children(filter=False))
        )  # Use get_children() to access children
        return count

    # Creates an index for a given row and column
    def index(self, row: int, column: int, parent=QModelIndex()):

        if not parent.isValid():
            if row >= len(self.root_classes):
                self.beginRemoveRows(QModelIndex(), row, row)
                self.endRemoveRows()
                return QModelIndex()
            item = self.root_classes[row]
            item.index = self.createIndex(row, column, item)
            return item.index

        node: SOMcreator.SOMClass = parent.internalPointer()
        children = list(
            node.get_children(filter=False)
        )  # Use get_children() to access children

        if 0 <= row < len(children):
            child = children[row]
            child.index = self.createIndex(row, column, child)
            return child.index
        return QModelIndex()

    # Returns the parent index of the given index
    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        node: SOMcreator.SOMClass = index.internalPointer()
        if node is None or not node.parent:
            return QModelIndex()
        parent_index: QModelIndex = node.parent.index
        return parent_index.sibling(parent_index.row(), 0)


class PsetModel(TreeModel):
    def __init__(self, project: SOMcreator.SOMProject):
        self.active_class: SOMcreator.SOMClass = None
        self.property_sets: list[SOMcreator.SOMPropertySet] = list()
        getter_funcs = [lambda p: getattr(p, "name")]
        super().__init__(project, getter_funcs)

    def flags(self, index: QModelIndex):
        node: SOMcreator.SOMPropertySet | SOMcreator.SOMProperty = (
            index.internalPointer()
        )
        if isinstance(node, SOMcreator.SOMPropertySet):
            parent_index = node.som_class.index
            parent_index = parent_index.sibling(parent_index.row(), index.column() + 1)
        else:
            parent_index = self.parent(index)
            parent_index = parent_index.sibling(parent_index.row(), index.column())
        return super().flags(index, parent_index)

    def update_data(self):
        self.property_sets = (
            list(self.active_class.get_property_sets(filter=False))
            if self.active_class
            else []
        )
        super().update_data()

    # Returns the number of children (rows) under the given index
    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.property_sets)  # Top-level items
        node: SOMcreator.SOMPropertySet = parent.internalPointer()
        if isinstance(node, SOMcreator.SOMProperty):
            return 0
        count = len(
            list(node.get_properties(filter=False))
        )  # Use get_children() to access children
        return count

    # Creates an index for a given row and column
    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            if row >= self.rowCount():
                self.beginRemoveRows(QModelIndex(), row, row)
                self.endRemoveRows()
                return QModelIndex()
            item: SOMcreator.SOMPropertySet = self.property_sets[row]
            item.index = self.createIndex(row, column, item)
            return item.index

        node: SOMcreator.SOMPropertySet = parent.internalPointer()
        children = list(node.get_properties(filter=False))
        if 0 <= row < len(children):
            child = children[row]
            child.index = self.createIndex(row, column, child)
            return child.index
        return QModelIndex()

    # Returns the parent index of the given index
    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        node: SOMcreator.SOMPropertySet | SOMcreator.SOMProperty = (
            index.internalPointer()
        )
        if node is None or isinstance(node, SOMcreator.SOMPropertySet):
            return QModelIndex()
        parent_index: QModelIndex = node.property_set.index
        return parent_index.sibling(parent_index.row(), 0)
