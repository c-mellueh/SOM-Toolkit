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
        self.mod =ComboboxItemModel(d)
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
        #self.add_items()
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
        trigger.update_current_unit(self.parent(),unit)

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
                    return index.internalPointer().get("Code", "")
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
            if 0>row >= len(self.data_dict):
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
    

class ComboboxItemModel(QAbstractItemModel):
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
        return 1

    def data(self, index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        

        if role not in (Qt.ItemDataRole.DisplayRole,Qt.ItemDataRole.CheckStateRole):
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
            if 0>row >= len(self.data_dict)-1:
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