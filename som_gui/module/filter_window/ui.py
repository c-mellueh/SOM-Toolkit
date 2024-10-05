from __future__ import annotations
import logging
from random import triangular
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QAbstractItemModel
from PySide6.QtWidgets import QTableWidget, QDialog, QTreeView, QWidget, QTableView
from ifcopenshell.express.rules.IFC4X1 import project

import SOMcreator
from som_gui.icons import get_icon
import som_gui.module.project_filter as project_filter
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from som_gui import tool
import som_gui
from . import trigger
from ...core.object import ident_attribute_changed


class FilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .qt import widget
        self.ui = widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())
        self.setWindowTitle(f"Projekt Filter {tool.Util.get_status_text()}")


class ProjectView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        action = QAction(f"Add Column", self)
        self.addAction(action)
        action.triggered.connect(self.add_column)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def add_column(self):
        self.model().add_usecase()

    def model(self) -> ProjectModel:
        return super().model()


class ObjectTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #
    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     object_filter.trigger.refresh_object_tree()
    #
    # def mousePressEvent(self, event: QMouseEvent):
    #     index = self.indexAt(event.pos())
    #     if core.tree_mouse_press_event(index, tool.ObjectFilter):
    #         super().mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     super().mouseMoveEvent(event)
    #     core.tree_mouse_move_event(self.indexAt(event.pos()), tool.ObjectFilter)
    #
    # def mouseReleaseEvent(self, event):
    #     super().mouseReleaseEvent(event)
    #     index = self.indexAt(event.pos())
    #     core.tree_mouse_release_event(index, tool.ObjectFilter)
    def enterEvent(self, event):
        super().enterEvent(event)
        trigger.update_object_tree()

    def model(self) -> ObjectModel:
        return super().model()


class PsetTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProjectModel(QAbstractTableModel):
    def __init__(self, project: SOMcreator.Project):
        super().__init__()
        self.project = project

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
        trigger.update_object_tree()
        return True

    def headerData(self, section, orientation, role=...):
        if role not in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return
        if orientation == Qt.Orientation.Horizontal:
            return self.project.get_usecases()[section].name
        else:
            return self.project.get_phases()[section].name

    def insertRows(self, row, count, parent=None):
        new_name = tool.Util.get_new_name("Neue Phase", [uc.name for uc in self.project.get_usecases()])
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        phase = SOMcreator.Phase(new_name, new_name, new_name)
        self.project.add_project_phase(phase)
        self.endInsertRows()


class ObjectModel(QAbstractItemModel):
    def __init__(self, project: SOMcreator.Project):
        self.project = project
        self.root_objects = list(self.project.get_root_objects(filter=False))
        super().__init__()
        self.allowed_combinations = self.get_allowed_combinations()

    def flags(self, index: QModelIndex):
        flags = super().flags(index)

        if index.column() < 2:
            return flags
        if index.column() >= 2:
            flags = flags | Qt.ItemFlag.ItemIsUserCheckable
        obj: SOMcreator.Object = index.internalPointer()
        parent_index = self.parent(index)
        if obj is None:
            return flags
        if not obj.parent:
            return flags

        if not parent_index.isValid():
            return flags
        is_parent_enabled = Qt.ItemFlag.ItemIsEnabled in parent_index.flags()
        is_parent_checked = tool.Util.checkstate_to_bool(parent_index.data(Qt.ItemDataRole.CheckStateRole))
        if not (is_parent_enabled and is_parent_checked):
            flags = flags & ~ Qt.ItemFlag.ItemIsEnabled
        return flags

    def get_allowed_combinations(self):
        allowed_combinations = list()
        for phase in self.project.get_phases():
            for usecase in self.project.get_usecases():
                if self.project.get_filter_state(phase, usecase):
                    allowed_combinations.append((phase, usecase))
        return allowed_combinations

    def update(self):
        logging.debug("Update")
        self.allowed_combinations = self.get_allowed_combinations()
        self.root_objects = list(self.project.get_root_objects(filter=False))
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(), self.columnCount()))

    def get_root(self):
        return self.root_objects

    # Returns the number of children (rows) under the given index
    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.get_root())  # Top-level items
        node: SOMcreator.Object = parent.internalPointer()
        count = len(list(node.get_children(filter=False)))  # Use get_children() to access children
        return count

    # Returns the number of columns for the children of the given parent
    def columnCount(self, parent=QModelIndex()):
        return 2 + len(self.allowed_combinations)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                if section == 0:
                    return "Objekt"
                elif section == 1:
                    return "Identifier"
                else:
                    if section - 2 >= len(self.allowed_combinations):
                        return None
                    phase, usecase = self.allowed_combinations[section - 2]
                    return f"{phase.name}-{usecase.name}"

    # Creates an index for a given row and column
    def index(self, row, column, parent=QModelIndex()):

        if not parent.isValid():
            if row >= len(self.get_root()):
                self.beginRemoveRows(QModelIndex(), row, row)
                self.endRemoveRows()
                return QModelIndex()
            item = self.get_root()[row]
            item.index = self.createIndex(row, column, item)
            return item.index

        node: SOMcreator.Object = parent.internalPointer()
        children = list(node.get_children(filter=False))  # Use get_children() to access children

        if row >= 0 and row < len(children):
            child = children[row]
            child.index = self.createIndex(row, column, child)
            return child.index
        return QModelIndex()

    # Returns the parent index of the given index
    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        node: SOMcreator.Object = index.internalPointer()
        if node is None:
            return QModelIndex()
        if not node.parent:
            return QModelIndex()
        parent_index: QModelIndex = node.parent.index
        return parent_index.sibling(parent_index.row(), index.column())

    # Returns the data to be displayed for each cell
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        node: SOMcreator.Object = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return node.name
            elif index.column() == 1:
                return node.ident_value

        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() > 1:
                pos = index.column() - 2
                if pos >= len(self.allowed_combinations):
                    return None
                phase, usecase = self.allowed_combinations[pos]
                return tool.Util.bool_to_checkstate(node.get_filter_state(phase, usecase))

        return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid() or role != Qt.ItemDataRole.CheckStateRole:
            return False
        node: SOMcreator.Object = index.internalPointer()
        if index.column() - 2 >= len(self.allowed_combinations):
            return False

        phase, usecase = self.get_allowed_combinations()[index.column() - 2]
        node.set_filter_state(phase, usecase, bool(value))
        trigger.update_object_tree()
        return True
