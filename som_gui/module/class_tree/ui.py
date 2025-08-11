from __future__ import annotations

from PySide6.QtWidgets import QTreeView, QTreeWidget, QWidget

from som_gui.module import class_tree
from som_gui.resources.icons import get_icon
import logging
from typing import TYPE_CHECKING
from PySide6.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    Signal,
    QObject,
)
from PySide6.QtGui import QMouseEvent, QDropEvent
import SOMcreator
from som_gui import tool
from PySide6.QtCore import QSortFilterProxyModel
from . import trigger


class ClassView(QTreeView):
    update_requested = Signal()
    mouse_moved = Signal(QMouseEvent, QObject)
    mouse_released = Signal(QMouseEvent, QObject)
    selected_class_changed = Signal(SOMcreator.SOMClass)
    class_double_clicked = Signal(SOMcreator.SOMClass)
    item_dropped = Signal(QDropEvent)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        trigger.connect_new_class_tree(self)

    def enterEvent(self, event):
        # self.update_requested.emit()
        return super().enterEvent(event)

    # for Typehints
    def model(self) -> ClassModel:
        model = super().model()
        if not isinstance(model, ClassModel):
            return model.sourceModel()
        return model

    def sort_model(self) -> QSortFilterProxyModel:
        model = super().model()
        if isinstance(model, ClassModel):
            return None
        return model

    def update_view(self):
        model = self.model()
        if model is None:
            return
        model.update_root_classes()
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

    def dragMoveEvent(self, event):
        return super().dragMoveEvent(event)

    def dropEvent(self, event):
        self.item_dropped.emit(event)


class ClassModel(QAbstractItemModel):
    reset_required = Signal(str)

    def __init__(self, *args, **kwargs):
        self.root_classes = (
            list(self.project.get_root_classes()) if self.project else list()
        )
        # We use this function because project.get_root_classes() takes too long to call every time
        # (name getter, value_getter, value_setter,role)
        self.columns: list[tuple[callable, callable, callable, Qt.ItemDataRole]] = (
            list()
        )

        self.class_index_dict: dict[SOMcreator.SOMClass, QModelIndex] = dict()
        self.old_column_count = len(self.columns)
        self.row_count_dict: dict[QModelIndex, int] = {
            QModelIndex(): len(self.root_classes)
        }
        super().__init__(*args, **kwargs)
        self.reset_required.connect(self.reset)

    @property
    def project(self):
        return tool.Project.get()

    def reset(self, source: str):
        logging.info(f"{source} -> Reset Class Model {self}")
        self.beginResetModel()
        self.root_classes = list(self.project.get_root_classes())
        self.class_index_dict = dict()
        self.row_count_dict = {QModelIndex(): len(self.root_classes)}
        self.old_column_count = len(self.columns)
        self.endResetModel()

    def update_root_classes(self):
        if not self.project:
            return
        old_root_classes = set(self.root_classes)
        new_root_classes = set(list(self.project.get_root_classes(filter=False)))
        for som_class in old_root_classes.difference(new_root_classes):
            self.root_classes.remove(som_class)
        for som_class in new_root_classes.difference(old_root_classes):
            self.root_classes.append(som_class)

    def headerData(self, section, orientation, /, role=...):
        if (
            role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole)
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.columns[section][0]()
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        """
        make Item Checkable if Column > check_column_index
        Disable Item if Parent is not checked or parent is disabled
        """
        flags = super().flags(index)
        flags |= Qt.ItemFlag.ItemIsDragEnabled
        flags |= Qt.ItemFlag.ItemIsDropEnabled

        column = index.column()
        if column >= len(self.columns):
            return flags

        role = self.columns[column][3]
        if role == Qt.ItemDataRole.CheckStateRole:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        else:
            flags &= ~Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def columnCount(self, parent=QModelIndex()):
        column_count = len(self.columns)
        if column_count != self.old_column_count:
            self.reset_required.emit("columnCount")
            self.old_column_count = column_count
        return len(self.columns)

    def get_row_count(self, parent=QModelIndex()):
        if not parent.isValid():
            result = len(list(self.root_classes))
        else:
            som_class: SOMcreator.SOMClass = parent.internalPointer()
            result = len(list(som_class.get_children(filter=True)))
        return result

    def rowCount(self, parent=QModelIndex()):
        if parent not in self.row_count_dict:
            self.row_count_dict[parent] = self.get_row_count(parent)
        return self.row_count_dict[parent]

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid():
            return None

        som_class: SOMcreator.SOMClass = index.internalPointer()
        column = index.column()
        if role != self.columns[column][3]:
            return
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            result = self.get_text(column, som_class)
            return result

        elif role == Qt.ItemDataRole.CheckStateRole:
            return self.get_checkstate(column, som_class)
        return None

    def get_checkstate(self, column: int, som_class: SOMcreator.SOMClass):
        getter_func = self.columns[column][1]
        return tool.Util.bool_to_checkstate(getter_func(som_class))

    def get_text(self, column: int, som_class: SOMcreator.SOMClass):
        getter_func = self.columns[column][1]
        return getter_func(som_class)

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid():
            return False
        column = index.column()
        if role != self.columns[column][3]:
            return False

        setter_func = self.columns[column][2]
        som_class: SOMcreator.SOMClass = index.internalPointer()
        if role == Qt.ItemDataRole.CheckStateRole:
            setter_func(som_class, bool(value))
        else:
            setter_func(som_class, value)
        return True

    def index(self, row: int, column: int, parent=QModelIndex()):
        # logging.debug(f"request Index {row}:{column} {parent}")
        if not parent.isValid():
            if row >= len(list(self.root_classes)):
                if not self.root_classes:
                    return QModelIndex()
                logging.debug("Index Exmits resize Required")
                self.reset_required.emit("index")
                return QModelIndex()
            som_class = self.root_classes[row]
            index = self.createIndex(row, column, som_class)
            return index
        else:
            parent = parent.siblingAtColumn(0)
            som_class: SOMcreator.SOMClass = parent.internalPointer()
            children = list(som_class.get_children(filter=False))
            if 0 <= row < len(children):
                child_class = children[row]
                index = self.createIndex(row, column, child_class)
                return index
            else:
                return QModelIndex()
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
        return parent_index.siblingAtColumn(0)

    def supportedDragActions(self):
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction

    def supportedDropActions(self):
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction

    def removeRow(self, row, /, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        if parent in self.row_count_dict:
            self.row_count_dict[parent] -= 1
        if not parent.isValid():
            self.root_classes.pop(row)
        self.endRemoveRows()

    def insertRow(self, row, parent=QModelIndex()):
        parent = parent.siblingAtColumn(0)
        if not parent in self.row_count_dict:
            self.row_count_dict[parent] = 0
        self.beginInsertRows(parent, row, row)
        self.row_count_dict[parent] += 1
        logging.debug(f"Insert Row {parent} {row}")
        self.endInsertRows()
        return True

    def removeColumn(self, column: int, parent=QModelIndex()):
        self.beginRemoveColumns(parent, column, column)
        self.columns.pop(column)
        self.old_column_count -= 1
        self.endRemoveColumns()

    def insertColumn(
        self,
        column_index: int,
        parent=QModelIndex(),
        column_functions: tuple[callable, callable, callable, callable] = tuple(),
    ):
        self.beginInsertColumns(parent, column_index, column_index)
        self.old_column_count += 1
        self.columns.insert(column_index, column_functions)
        self.endInsertColumns()

    def moveColumn(
        self, sourceParent, sourceColumn, destinationParent, destinationChild
    ):
        self.beginMoveColumns(
            sourceParent,
            sourceColumn,
            sourceColumn,
            destinationParent,
            destinationChild,
        )
        column_funcs = self.columns.pop(sourceColumn)
        self.columns.insert(destinationChild, column_funcs)
        self.endMoveColumns()

    def moveRow(
        self,
        sourceParent: QModelIndex,
        sourceRow: int,
        destinationParent: QModelIndex,
        destinationChild: int,
    ):
        if sourceParent.siblingAtColumn(0) == destinationParent.siblingAtColumn(0):
            return
        self.beginMoveRows(
            sourceParent, sourceRow, sourceRow, destinationParent, destinationChild
        )
        start_index = self.index(sourceRow, 0, sourceParent)
        som_class: SOMcreator.SOMClass = start_index.internalPointer()
        if not destinationParent.isValid():
            som_class.remove_parent()
            self.root_classes.append(som_class)
        else:
            new_parent: SOMcreator.SOMClass = destinationParent.internalPointer()
            new_parent.add_child(som_class)
        if sourceParent in self.row_count_dict:
            self.row_count_dict[sourceParent] -= 1
        if not sourceParent.isValid():
            self.root_classes.pop(sourceRow)
        if destinationParent in self.row_count_dict:
            self.row_count_dict[destinationParent] += 1
        self.endMoveRows()

    def mimeData(self, indexes):
        return trigger.create_mime_data(indexes, super().mimeData(indexes))
