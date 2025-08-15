from PySide6.QtCore import QRect, QSize, Qt,QAbstractItemModel,QModelIndex
from PySide6.QtWidgets import QHeaderView, QWidget, QComboBox, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from som_gui.module.units import trigger
from .qt import ui_UnitSettings
from som_gui import tool

class UnitSettings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_UnitSettings.Ui_UnitSettings()
        self.ui.setupUi(self)
        trigger.unit_settings_created(self)


class UnitComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree_view = QTreeView()
        self.setView(self.tree_view)
        self.mod: QStandardItemModel = QStandardItemModel()
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
        self.setEditable(True)
        self.add_items()
        self.is_locked = False
        self.tree_view.setMinimumHeight(self.tree_view.sizeHintForRow(0) * 5)

    def paintEvent(self, e):
        from . import trigger

        trigger.repaint_unit_combobox(self)
        return super().paintEvent(e)

    def add_items(self):
        from ifcopenshell.util import unit as ifc_unit

        self.mod.appendRow(QStandardItem())
        for unit_name in sorted(ifc_unit.unit_names):
            unit = QStandardItem(unit_name.capitalize())
            for prefix in reversed(list(ifc_unit.prefixes.keys())):
                unit.appendRow(QStandardItem(prefix.capitalize()))
            self.mod.appendRow(unit)

    def hidePopup(self):
        # Allow the popup to close if the combo box loses focus
        if not self.is_locked:
            super().hidePopup()

    def index_changed(self, _):
        self.is_locked = False
        index = self.tree_view.selectionModel().selectedIndexes()[0]
        item = self.mod.itemFromIndex(index)
        if not item:
            return
        self.setCurrentText(self.get_full_text(item))

    def get_full_text(self, item):
        text = item.text()
        parent = item.parent()
        if not parent:
            return text

        parent_text = parent.text()
        if not "_" in parent_text or parent_text == "DEGREE_CELSIUS":
            return f"{text}_{parent.text()}"

        [p1, p2] = parent_text.split("_")
        return "_".join((p1, text, p2))

class SettingsItemModel(QAbstractItemModel):
    def __init__(self,data_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from som_gui.resources.data import UNIT_PATH
        import json
        self.data_dict =data_dict
        # self.setHorizontalHeaderLabels(["Unit", "Prefix"])
        # self.setColumnCount(2)

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.data_dict)
        else:
            data = parent.internalPointer()
            if data["type"] == "quantity":
                return len(parent.internalPointer()["children"]+ parent.internalPointer()["units"])
            return 0


    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        

        if role not in (Qt.ItemDataRole.DisplayRole,Qt.ItemDataRole.CheckStateRole):
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
                    return index.internalPointer().get("Name", "")
                if index.column() == 1:
                    return index.internalPointer().get("Code", "")
        else:
            if index.column() != 2:
                return None
            if data["type"] == "quantity":
                return None
            return tool.Util.bool_to_checkstate(data.get("is_checked", True))
        
    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole):
        if not index.isValid():
            return False

        if role != Qt.ItemDataRole.CheckStateRole:
            return False
        data = index.internalPointer()
        data["is_checked"] = bool(value)
        return True
    
    def index(self, row: int, column: int, parent=QModelIndex()):
        # logging.debug(f"request Index {row}:{column} {parent}")
        if not parent.isValid():
            if row >= len(self.data_dict):
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
            elif child_count<=row<= child_count + unit_count:
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
        data =  index.internalPointer()
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

        if index.column() == 2: #and index.internalPointer().get("type") == "unit":
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        else:
            flags &= ~Qt.ItemFlag.ItemIsUserCheckable
        return flags