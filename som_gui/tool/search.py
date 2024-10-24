from __future__ import annotations
import som_gui
import som_gui.core.tool
from som_gui.module.project.constants import CLASS_REFERENCE, UMLAUT_DICT
from som_gui.module import search
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget
from PySide6.QtCore import Qt, QCoreApplication
from som_gui import tool
from som_gui import __version__ as version

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
            return [QCoreApplication.translate("Search", "Object"),
                    QCoreApplication.translate("Search", "Identifier"),
                    QCoreApplication.translate("Search", "Abbreviation"),
                    ]
        if prop.search_mode == 2:
            return [QCoreApplication.translate("Search", "PropertySet"),
                    QCoreApplication.translate("Search", "Attribute"), ]

    @classmethod
    def get_dialog(cls) -> SearchWindow:
        return cls.get_search_properties().search_window

    @classmethod
    def get_search_mode(cls) -> int:
        return cls.get_search_properties().search_mode

    @classmethod
    def retranslate_title(cls, widget: SearchWindow, search_mode: int):
        title = ""
        if search_mode == 1:
            title = QCoreApplication.translate('Search', 'Search Object')
        elif search_mode == 2:
            title = QCoreApplication.translate('Search', 'Search Attribute')

        widget.setWindowTitle(tool.Util.get_window_title(f"{title} v{version}"))

    @classmethod
    def search_object(cls) -> SOMcreator.Object | None:
        prop = cls.get_search_properties()
        prop.search_mode = 1
        prop.search_window = search.ui.SearchWindow()
        prop.search_window.ui.tableWidget.itemDoubleClicked.connect(cls.activate_item)
        cls.fill_dialog()
        cls.retranslate_title(prop.search_window, prop.search_mode)
        if not prop.search_window.exec():
            return None
        return prop.selected_info

    @classmethod
    def search_attribute(cls):
        prop = cls.get_search_properties()
        prop.search_mode = 2
        prop.search_window = search.ui.SearchWindow()
        prop.search_window.ui.tableWidget.itemDoubleClicked.connect(cls.activate_item)
        cls.fill_dialog()
        cls.retranslate_title(prop.search_window, prop.search_mode)

        if not prop.search_window.exec():
            return None
        return prop.selected_info

    @classmethod
    def fill_dialog(cls):
        dialog = cls.get_dialog()
        table = dialog.ui.tableWidget
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
        project: SOMcreator.Project = tool.Project.get()
        if cls.get_search_mode() == 1:
            for obj in project.get_objects(filter=True):
                item_dict[obj] = [obj.name, obj.ident_value, obj.abbreviation]
        elif cls.get_search_mode() == 2:
            attributes = filter(lambda item: isinstance(item, SOMcreator.Attribute),
                                project.get_hirarchy_items(filter=False))
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
    def refresh_dialog(cls, widget: SearchWindow, threshold):
        widget_ui = widget.ui
        widget_ui.tableWidget.setSortingEnabled(False)
        search_text = widget_ui.lineEdit.text()
        search_text = search_text.translate(UMLAUT_DICT)
        column_count = len(cls.get_column_texts())
        widget_ui.tableWidget.hideColumn(column_count)
        for row in range(widget_ui.tableWidget.rowCount()):
            ration = cls.check_row(widget_ui.tableWidget, search_text, row, column_count)
            if ration > threshold:
                widget_ui.tableWidget.showRow(row)
            else:
                widget_ui.tableWidget.hideRow(row)
        widget_ui.tableWidget.setSortingEnabled(True)
        widget_ui.tableWidget.resizeColumnsToContents()
        widget_ui.tableWidget.sortByColumn(column_count, Qt.SortOrder.DescendingOrder)

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
        item = cls.get_dialog().ui.tableWidget.selectedItems()[0]
        prop = cls.get_search_properties()
        prop.selected_info = item.data(CLASS_REFERENCE)
        cls.get_dialog().accept()
