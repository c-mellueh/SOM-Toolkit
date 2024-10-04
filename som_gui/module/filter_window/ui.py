from random import triangular
from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QTableWidget, QDialog, QTreeView, QWidget, QTableView

import SOMcreator
from som_gui.icons import get_icon
import som_gui.module.project_filter as project_filter
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from som_gui import tool
import som_gui
from . import trigger


class FilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .qt import widget
        self.ui = widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(som_gui.get_icon())
        self.setWindowTitle(f"Projekt Filter {tool.Util.get_status_text()}")


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


class ProjectView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        action = QAction(f"Add Column", self)
        self.addAction(action)
        action.triggered.connect(self.add_column)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def add_column(self):
        self.model().add_usecase()

    def model(self) -> ProjectModel:
        return super().model()


class ProjectTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.pt_update()


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


class PsetTreeView(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
