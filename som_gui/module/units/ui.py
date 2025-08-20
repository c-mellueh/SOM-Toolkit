from PySide6.QtCore import QRect, QCoreApplication, Qt, QAbstractItemModel, QModelIndex
from PySide6.QtWidgets import QHeaderView, QWidget, QComboBox, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from som_gui.module.units import trigger
from .qt import ui_UnitSettings
from som_gui import tool

CHECK_COLUMN = 2


class UnitSettings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_UnitSettings.Ui_UnitSettings()
        self.ui.setupUi(self)
        trigger.unit_settings_created(self)


# class UnitComboBox(QComboBox):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.tree_view = QTreeView()
#         self.setView(self.tree_view)
#         d = tool.Units.get_units_dict()
#         self.mod =SettingsItemModel(d)
#         self.setModel(self.mod)


class UnitComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree_view = QTreeView()
        self.setView(self.tree_view)
        d = tool.Units.get_units_dict()
        self.mod = ComboboxItemModel(d)
        self.setModel(self.mod)
        self.tree_view.header().setVisible(False)
        self.tree_view.expanded.connect(lambda: setattr(self, "is_locked", True))
        self.tree_view.collapsed.connect(lambda: setattr(self, "is_locked", True))
        self.tree_view.selectionModel().selectionChanged.connect(
            lambda: setattr(self, "is_locked", False)
        )
        self.currentIndexChanged.connect(
            self.index_changed
        )  # Populate the model with hierarchical data
        self.setEditable(False)
        # self.add_items()
        self.is_locked = False
        self.tree_view.setMinimumHeight(40)

    def paintEvent(self, e):
        from . import trigger

        trigger.repaint_unit_combobox(self)
        return super().paintEvent(e)

    def hidePopup(self):
        # Allow the popup to close if the combo box loses focus
        if not self.is_locked:
            super().hidePopup()

    def index_changed(self, _):
        self.is_locked = False
        index = self.tree_view.selectionModel().selectedIndexes()[0]
        item = index.internalPointer()
        if not item:
            return
        if item["type"] == "quantity":
            if item["units"]:
                unit = item["units"][0]
            else:
                self.setCurrentText("")
                return
        else:
            unit = item

        self.setCurrentText(unit["Code"])
        trigger.update_current_unit(self.parent(), unit)


class SettingsItemModel(QAbstractItemModel):
    def __init__(self, data_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from som_gui.resources.data import UNIT_PATH
        import json

        self.data_dict = data_dict
        # self.setHorizontalHeaderLabels(["Unit", "Prefix"])
        # self.setColumnCount(2)

    def headerData(self, section, orientation, /, role=...):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                if section == 0:
                    return QCoreApplication.translate("Units", "Name")
                if section == 1:
                    return QCoreApplication.translate("Units", "Abbrev.")
                if section == 2:
                    return QCoreApplication.translate("Units", "Is Active")
        return None

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.data_dict)
        else:
            data = parent.internalPointer()
            if data["type"] == "quantity":
                return len(parent.internalPointer()["children"]) + len(
                    parent.internalPointer()["units"]
                )
            return 0

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.CheckStateRole):
            return None
        data = index.internalPointer()
        if Qt.ItemDataRole.DisplayRole == role:
            if data["type"] == "quantity":
                if index.column() == 0:
                    return index.internalPointer().get("name", "")
                if index.column() == 1:
                    return None
            else:
                if index.column() == 0:
                    return index.internalPointer().get("name", "")
                if index.column() == 1:
                    return index.internalPointer().get("Code", "")
        else:
            if index.column() != CHECK_COLUMN:
                return None

            if self.hasChildren(index):
                cs = {
                    self.data(ci, role=Qt.ItemDataRole.CheckStateRole)
                    for ci in self.get_children(index)
                }
                if {Qt.CheckState.Checked} == cs:
                    return Qt.CheckState.Checked
                elif {Qt.CheckState.Unchecked} == cs:
                    return Qt.CheckState.Unchecked
                else:
                    return Qt.CheckState.PartiallyChecked
            return tool.Util.bool_to_checkstate(data.get("is_active", True))

    def get_children(self, parent_index: QModelIndex):
        column = parent_index.column()
        return [
            self.index(r, column, parent_index)
            for r in range(self.rowCount(parent_index))
        ]

    def _emit_subtree_flags_changed(self, parent_index: QModelIndex):
        """
        Emittiert dataChanged für alle direkten Kinder-Ranges und läuft rekursiv/iterativ
        durch die gesamte Teilstruktur. Leere Rollenliste ist ok; die View fragt flags() neu ab.
        """
        stack = [parent_index]
        while stack:
            p = stack.pop()
            rows = self.rowCount(p)
            if rows <= 0:
                continue

            cols = self.columnCount(p)
            top_left = self.index(0, 0, p)
            bottom_right = self.index(rows - 1, cols - 1, p)
            # Flags haben sich „logisch“ geändert -> dataChanged ohne spezielle Rollen
            self.dataChanged.emit(top_left, bottom_right, [])

            # Tiefer gehen: Spalte 0 pro Zeile reicht zum Traversieren
            for r in range(rows):
                child_parent = self.index(r, 0, p)
                stack.append(child_parent)

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid():
            return False
        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        data = index.internalPointer()
        data["is_active"] = bool(value)
        if self.hasChildren(index):
            for row in range(self.rowCount(index)):
                child = self.index(row, CHECK_COLUMN, index)
                self.setData(child, value, role)
        self._emit_subtree_flags_changed(index)

        parent = self.parent(index).siblingAtColumn(CHECK_COLUMN)
        while parent.isValid():
            parent = parent
            self.dataChanged.emit(parent, parent, parent.parent())
            parent = self.parent(parent).siblingAtColumn(CHECK_COLUMN)
        return True

    def index(self, row: int, column: int, parent=QModelIndex()):
        # logging.debug(f"request Index {row}:{column} {parent}")
        if not parent.isValid():
            if 0 > row >= len(self.data_dict):
                return QModelIndex()
            element = self.data_dict[row]
            element["type"] = "quantity"
            index = self.createIndex(row, column, element)
            return index
        else:
            parent = parent.siblingAtColumn(0)
            parent_data = parent.internalPointer()
            children = parent_data["children"]
            child_count = len(children)
            units = parent_data["units"]
            unit_count = len(units)
            if 0 <= row < child_count:
                child_data = children[row]
                child_data["parent"] = parent
                child_data["type"] = "quantity"
                index = self.createIndex(row, column, child_data)
                return index
            elif child_count <= row <= child_count + unit_count:
                unit_data = units[row - child_count]
                unit_data["parent"] = parent
                unit_data["type"] = "unit"
                if "checked" not in unit_data:
                    unit_data["checked"] = True
                index = self.createIndex(row, column, unit_data)
                return index
            else:
                return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        data = index.internalPointer()
        if data is None or data.get("parent") is None:
            return QModelIndex()
        return data["parent"]

    def flags(self, index: QModelIndex):
        """
        make Item Checkable if Column > check_column_index
        Disable Item if Parent is not checked or parent is disabled
        """
        flags = super().flags(index)

        column = index.column()
        if column >= self.columnCount():
            return flags

        if (
            index.column() == CHECK_COLUMN
        ):  # and index.internalPointer().get("type") == "unit":
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        else:
            flags &= ~Qt.ItemFlag.ItemIsUserCheckable
        return flags


def _calculate_row_count(quant):
    quant_count = len([q for q in quant["children"] if _calculate_row_count(q) > 0])
    unit_count = len([u for u in quant["units"] if u.get("is_active")])
    return quant_count + unit_count


class ComboboxItemModel(QAbstractItemModel):
    def __init__(self, data_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from som_gui.resources.data import UNIT_PATH
        import json

        self.data_dict = data_dict
        # self.setHorizontalHeaderLabels(["Unit", "Prefix"])
        # self.setColumnCount(2)

    def rowCount(self, parent=QModelIndex()):

        if not parent.isValid():
            return len([q for q in self.data_dict if _calculate_row_count(q) > 0])
        else:
            data = parent.internalPointer()
            if data["type"] == "quantity":
                return _calculate_row_count(data)
            return 0

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.CheckStateRole):
            return None
        data = index.internalPointer()
        if Qt.ItemDataRole.DisplayRole != role:
            return None
        if data["type"] == "quantity":
            if index.column() == 0:
                return index.internalPointer().get("name", "")
        else:
            if index.column() == 0:
                return index.internalPointer().get("Code", "")
        return None

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        return False

    def index(self, row: int, column: int, parent=QModelIndex()):
        # logging.debug(f"request Index {row}:{column} {parent}")
        if not parent.isValid():
            first_layer_elements = [
                q for q in self.data_dict if _calculate_row_count(q) > 0
            ]
            if 0 > row >= len(first_layer_elements):
                return QModelIndex()
            element = first_layer_elements[row]
            element["type"] = "quantity"
            index = self.createIndex(row, column, element)
            return index
        else:
            parent = parent.siblingAtColumn(0)
            parent_data = parent.internalPointer()
            children = [
                c for c in parent_data["children"] if _calculate_row_count(c) > 0
            ]
            child_count = len(children)
            units = [u for u in parent_data["units"] if u.get("is_active")]
            unit_count = len(units)
            if 0 <= row < child_count:
                child_data = children[row]
                child_data["parent"] = parent
                child_data["type"] = "quantity"
                index = self.createIndex(row, column, child_data)
                return index
            elif child_count <= row <= child_count + unit_count:
                unit_data = units[row - child_count]
                unit_data["parent"] = parent
                unit_data["type"] = "unit"
                if "checked" not in unit_data:
                    unit_data["checked"] = True
                index = self.createIndex(row, column, unit_data)
                return index
            else:
                return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        data = index.internalPointer()
        if data is None or data.get("parent") is None:
            return QModelIndex()
        return data["parent"]
