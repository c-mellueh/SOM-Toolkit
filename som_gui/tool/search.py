from __future__ import annotations
import som_gui
import som_gui.core.tool
from som_gui.module.project.constants import CLASS_REFERENCE, UMLAUT_DICT
from som_gui.module import search
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget
from PySide6.QtCore import Qt
from som_gui import tool

if TYPE_CHECKING:
    from som_gui.module.search.prop import SearchProperties
    from som_gui.module.search.ui import SearchWindow
import SOMcreator
from thefuzz import fuzz


class Search(som_gui.core.tool.Search):
    @classmethod
    def get_column_texts(cls):
        prop = cls.get_search_properties()
        if prop.search_mode == 1:
            return ["Objekt", "Identifier", "Abkürzung"]
        if prop.search_mode == 2:
            return ["PropertySet", "Attribut"]

    @classmethod
    def get_dialog(cls) -> SearchWindow:
        return cls.get_search_properties().search_window

    @classmethod
    def get_search_mode(cls) -> int:
        return cls.get_search_properties().search_mode

    @classmethod
    def search_object(cls):
        prop = cls.get_search_properties()
        prop.search_mode = 1
        prop.search_window = search.ui.SearchWindow()
        prop.search_window.widget.tableWidget.itemDoubleClicked.connect(cls.activate_item)
        cls.fill_dialog()
        prop.search_window.setWindowTitle("Objektsuche")
        if not prop.search_window.exec():
            return None
        return prop.selected_info

    @classmethod
    def search_attribute(cls):
        prop = cls.get_search_properties()
        prop.search_mode = 2
        prop.search_window = search.ui.SearchWindow()
        prop.search_window.widget.tableWidget.itemDoubleClicked.connect(cls.activate_item)
        cls.fill_dialog()
        prop.search_window.setWindowTitle("AttributSuche")
        if not prop.search_window.exec():
            return None
        return prop.selected_info


    @classmethod
    def fill_dialog(cls):
        dialog = cls.get_dialog()
        table = dialog.widget.tableWidget
        header_texts = cls.get_column_texts()
        table.setColumnCount(len(header_texts) + 1)
        table.setHorizontalHeaderLabels(header_texts)
        for item_row in cls.create_table_items():
            row = table.rowCount()
            table.insertRow(row)
            [table.setItem(row, col, item) for col, item in enumerate(item_row)]

    @classmethod
    def create_table_items(cls):
        item_dict = dict()
        project = tool.Project.get()
        if cls.get_search_mode() == 1:
            for obj in project.objects:
                item_dict[obj] = [obj.name, obj.ident_value, obj.abbreviation]
        elif cls.get_search_mode() == 2:
            attributes = filter(lambda item: isinstance(item, SOMcreator.Attribute), project.get_all_hirarchy_items())
            for attribute in attributes:
                val = tuple([attribute.property_set.name, attribute.name])
                item_dict[val] = val

        item_list = list()
        for data, values in item_dict.items():
            items = [QTableWidgetItem(text) for text in values]
            [i.setData(CLASS_REFERENCE, data) for i in items]
            item_list.append(items)
        return item_list

    @classmethod
    def refresh_dialog(cls):
        widget = cls.get_dialog().widget
        threshold = cls.get_search_properties().filter_threshold
        widget.tableWidget.setSortingEnabled(False)
        search_text = widget.lineEdit.text()
        search_text = search_text.translate(UMLAUT_DICT)
        column_count = len(cls.get_column_texts())
        widget.tableWidget.hideColumn(column_count)
        for row in range(widget.tableWidget.rowCount()):
            ration = cls.check_row(widget.tableWidget, search_text, row, column_count)
            if ration > threshold:
                widget.tableWidget.showRow(row)
            else:
                widget.tableWidget.hideRow(row)
        widget.tableWidget.setSortingEnabled(True)
        widget.tableWidget.resizeColumnsToContents()
        widget.tableWidget.sortByColumn(column_count, Qt.SortOrder.DescendingOrder)

    @classmethod
    def check_row(cls, table: QTableWidget, search_text: str, row: int, column_count: int) -> float:
        model = table.model()
        texts = [table.item(row, col).text().lower() for col in range(column_count)]
        ratio = max(fuzz.ratio(search_text, text) for text in texts)
        model.setData(model.index(row, column_count), ratio, Qt.ItemDataRole.DisplayRole)
        return ratio

    @classmethod
    def get_search_properties(cls) -> SearchProperties:
        return som_gui.SearchProperties

    @classmethod
    def activate_item(cls):
        item = cls.get_dialog().widget.tableWidget.selectedItems()[0]
        prop = cls.get_search_properties()
        prop.selected_info = item.data(CLASS_REFERENCE)
        cls.get_dialog().accept()
