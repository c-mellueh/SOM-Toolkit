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
from PySide6.QtGui import QMouseEvent, QColor, QPainter, QPalette, QBrush
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


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        from .qt import ui_Settings

        self.ui = ui_Settings.Ui_FilterWindow()
        self.ui.setupUi(self)
        trigger.settings_widget_created(self)


class FilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .qt import ui_Widget

        self.ui = ui_Widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())


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


class FilterTreeView(QTreeView):
    def __init__(self, parent, frozen_col_count):
        super().__init__(parent)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        trigger.tree_mouse_move_event(self.indexAt(event.pos()))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        trigger.tree_mouse_release_event(index)


class ClassTreeView(FilterTreeView):
    def __init__(self, parent=None):
        super().__init__(parent, 2)

    def enterEvent(self, event):
        super().enterEvent(event)
        trigger.update_class_tree()

    def model(self) -> ClassModel:
        return super().model()

    def header(self) -> CustomHeaderView:
        return super().header()


class PsetTreeView(FilterTreeView):
    def __init__(self, parent=None):
        super().__init__(parent, 1)

    def enterEvent(self, event):
        super().enterEvent(event)
        trigger.update_pset_tree()

    def model(self) -> PsetModel:
        return super().model()


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
        trigger.change_filter_state(usecase, phase,bool(value))
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


class TreeModel(QAbstractItemModel):
    def __init__(
        self,
        project: SOMcreator.SOMProject,
        check_column_index: int,
        column_titles: list[str],
    ):
        super().__init__()
        self.project = project
        self.allowed_combinations = self.get_allowed_combinations()
        self.check_column_index = (
            check_column_index  # index of first column with checkdata
        )
        self.column_titles = column_titles

    def update(self):
        self.allowed_combinations = self.get_allowed_combinations()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
        )

    def flags(self, index, parent_index):
        flags = super().flags(index)
        if index.column() < self.check_column_index:
            return flags
        if index.column() >= self.check_column_index:
            flags = flags | Qt.ItemFlag.ItemIsUserCheckable
        if not parent_index.isValid():
            return flags
        is_parent_enabled = Qt.ItemFlag.ItemIsEnabled in parent_index.flags()
        is_parent_checked = tool.Util.checkstate_to_bool(
            parent_index.data(Qt.ItemDataRole.CheckStateRole)
        )
        if not (is_parent_enabled and is_parent_checked):
            flags = flags & ~Qt.ItemFlag.ItemIsEnabled
        return flags

    def column_index_from_ucph(self,usecase:SOMcreator.UseCase,phase:SOMcreator.Phase):
        return self.allowed_combinations.index((usecase,phase))


    def get_allowed_combinations(self):
        allowed_combinations = list()
        for use_case in self.project.get_usecases():
            for phase in self.project.get_phases():
                if self.project.get_filter_state(phase, use_case):
                    allowed_combinations.append((use_case, phase))
        return allowed_combinations

    def columnCount(self, parent=QModelIndex()):
        return self.check_column_index + len(self.allowed_combinations)

    # Returns the data to be displayed for each cell
    def data(
        self,
        index,
        role=Qt.ItemDataRole.DisplayRole,
        getter_functions: list[Callable] = None,
    ):
        if getter_functions is None:
            return None
        if not index.isValid():
            return None
        node: SOMcreator.SOMClass = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            for col, getter_function in enumerate(getter_functions):
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
        node: SOMcreator.SOMClass = index.internalPointer()
        if index.column() - self.check_column_index >= len(self.allowed_combinations):
            return False

        usecase, phase = self.get_allowed_combinations()[
            index.column() - self.check_column_index
        ]
        logging.debug(f"Set {node} {phase.name}:{usecase.name} to {bool(value)}")
        node.set_filter_state(phase, usecase, bool(value))
        trigger.update_class_tree()
        trigger.update_pset_tree()
        return True


class ClassModel(TreeModel):
    def __init__(self, project: SOMcreator.SOMProject):
        super().__init__(project, 2, ["h0", "h1"])
        self.root_classes = list(self.project.get_root_classes(filter=False))

    def retranslate_ui(self):
        h0 = QCoreApplication.translate("FilterWindow", "Class")
        h1 = QCoreApplication.translate("FilterWindow", "Identifier")
        self.column_titles = [h0, h1]

    def flags(self, index: QModelIndex):
        parent_index = self.parent(index)
        parent_index = parent_index.sibling(parent_index.row(), index.column())
        return super().flags(index, parent_index)

    def update(self):
        """
        updates root_classes so that you dont need to call get_root_classes on every instance between paint events
        """
        logging.debug("Update")
        self.root_classes = list(self.project.get_root_classes(filter=False))
        super().update()

    def get_root(self):
        return self.root_classes

    # Returns the number of children (rows) under the given index
    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.get_root())  # Top-level items
        node: SOMcreator.SOMClass = parent.internalPointer()
        count = len(
            list(node.get_children(filter=False))
        )  # Use get_children() to access children
        return count

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

    # Returns the data to be displayed for each cell
    def data(self, index, role=Qt.DisplayRole):
        getter_funcs = [
            lambda o: getattr(o, "name"),
            lambda o: getattr(o, "ident_value"),
        ]
        return super().data(index, role, getter_funcs)


class PsetModel(TreeModel):
    def __init__(self, project: SOMcreator.SOMProject):
        super().__init__(project, 1, ["h1"])
        self.active_class = tool.FilterWindow.get_active_class()

    def retranslate_ui(self):
        h0 = QCoreApplication.translate("FilterWindow", "PropertySet/Property")
        self.column_titles = [h0]

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

    def update(self):
        logging.debug("Update")
        self.active_class = tool.FilterWindow.get_active_class()
        super().update()

    def get_property_sets(self) -> list[SOMcreator.SOMPropertySet]:
        if tool.FilterWindow.get_active_class() is None:
            return []
        return list(
            tool.FilterWindow.get_active_class().get_property_sets(filter=False)
        )

    # Returns the number of children (rows) under the given index
    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.get_property_sets())  # Top-level items
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
            item: SOMcreator.SOMPropertySet = self.get_property_sets()[row]
            item.index = self.createIndex(row, column, item)
            return item.index

        node: SOMcreator.SOMPropertySet = parent.internalPointer()
        children = list(
            node.get_properties(filter=False)
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
        node: SOMcreator.SOMPropertySet | SOMcreator.SOMProperty = (
            index.internalPointer()
        )
        if node is None or isinstance(node, SOMcreator.SOMPropertySet):
            return QModelIndex()
        parent_index: QModelIndex = node.property_set.index
        return parent_index.sibling(parent_index.row(), 0)

    # Returns the data to be displayed for each cell
    def data(self, index, role=Qt.DisplayRole):
        getter_funcs = [lambda o: getattr(o, "name")]
        return super().data(index, role, getter_funcs)



    