from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QHeaderView, QWidget, QComboBox, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

from .qt import ui_CompareWidget


class AttributeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_CompareWidget.Ui_AttributeCompare()
        self.ui.setupUi(self)
        self.ui.tree_widget_object.setColumnCount(2)
        self.ui.tree_widget_propertysets.setColumnCount(2)
        self.ui.table_widget_values.setColumnCount(2)
        self.ui.table_infos.setColumnCount(3)


class WordWrapHeaderView(QHeaderView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sectionSizeFromContents(self, logicalIndex):
        text = str(
            self.model().headerData(
                logicalIndex, self.orientation(), Qt.ItemDataRole.DisplayRole
            )
        )
        max_width = self.sectionSize(logicalIndex)
        maxheight = 5000
        alignement = self.defaultAlignment()
        metrics = self.fontMetrics()
        rect = metrics.boundingRect(QRect(0, 0, max_width, maxheight), alignement, text)
        text_margin_buffer = QSize(2, 2)
        return rect.size() + text_margin_buffer


class UnitComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree_view = QTreeView()
        self.setView(self.tree_view)
        self.mod = QStandardItemModel()
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
        while parent:
            text = f" {text}_{parent.text()}"
            parent = parent.parent()
        return text
