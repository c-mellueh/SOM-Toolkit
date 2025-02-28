from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

import som_gui
import som_gui.core.tool
from som_gui import __version__ as version
from som_gui import tool
from som_gui.module import search
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.module.search.prop import SearchProperties
    from som_gui.module.search.ui import SearchDialog
import SOMcreator
from thefuzz import fuzz


class Search(som_gui.core.tool.Search):
    @classmethod
    def get_properties(cls) -> SearchProperties:
        return som_gui.SearchProperties

    @classmethod
    def _search(
        cls, search_mode: int, search_items: list, data_getters: list[Callable]
    ):
        """
        Create Search Window
        :param search_mode:
        :param search_items: entities which will be searchable
        :param data_getters: getter functions for row values
        :return:
        """
        prop = cls.get_properties()
        search_dialog = search.ui.SearchDialog()
        prop.search_dialogues.add(search_dialog)
        search_dialog.search_mode = search_mode
        cls.fill_table(search_dialog, search_items, data_getters)
        cls.retranslate_title(search_dialog, prop.search_mode)
        if not search_dialog.exec_():
            prop.search_dialogues.remove(search_dialog)
            return None
        prop.search_dialogues.remove(search_dialog)
        return search_dialog.return_value

    @classmethod
    def search_object(
        cls, searchable_objects: list[SOMcreator.SOMClass]
    ) -> SOMcreator.SOMClass | None:
        """
        Opens SearchWindow which searches for an object
        :param searchable_objects: Objects which will be visible in Search Table
        :return:

        """
        # Create Getter Methods for Columns
        getter_methods = [
            lambda o: getattr(o, "name"),
            lambda o: getattr(o, "ident_value"),
            lambda o: getattr(o, "abbreviation"),
        ]
        return cls._search(1, searchable_objects, getter_methods)

    @classmethod
    def search_attribute(
        cls, searchable_attributes: list[SOMcreator.SOMProperty]
    ) -> SOMcreator.SOMProperty | None:
        """
        Opens SearchWindow which searches for an Attribute
        :param searchable_attributes: Attributes which will be visible in Search Table

        :return:
        """
        getter_methods = [
            lambda a: getattr(a, "property_set").name,
            lambda a: getattr(a, "name"),
        ]
        return cls._search(2, searchable_attributes, getter_methods)

    @classmethod
    def get_column_texts(cls, search_mode: int) -> list[str]:
        """
        Get text of Columns for different search_modes
        :return:
        """
        if search_mode == 1:
            return [
                QCoreApplication.translate("Search", "Object"),
                QCoreApplication.translate("Search", "Identifier"),
                QCoreApplication.translate("Search", "Abbreviation"),
            ]
        if search_mode == 2:
            return [
                QCoreApplication.translate("Search", "PropertySet"),
                QCoreApplication.translate("Search", "Attribute"),
            ]

    @classmethod
    def retranslate_title(cls, dialog: SearchDialog, search_mode: int):
        """
        retranslates title based on search mode and language
        :param dialog:
        :param search_mode:
        :return:
        """
        title = ""
        if search_mode == 1:
            title = QCoreApplication.translate("Search", "Search Object")
        elif search_mode == 2:
            title = QCoreApplication.translate("Search", "Search Attribute")

        dialog.setWindowTitle(tool.Util.get_window_title(f"{title} v{version}"))

    @classmethod
    def fill_table(
        cls, dialog: SearchDialog, search_items: list, data_getters: list[Callable]
    ):
        """
        fills table based on search mode with entities
        :return:
        """
        table = dialog.ui.tableWidget
        # Fill Horizontal Header
        header_texts = cls.get_column_texts(cls.get_search_mode(dialog))
        table.setColumnCount(len(header_texts) + 1)
        table.setHorizontalHeaderLabels(header_texts)
        # Insert TableWidgetItems
        for item_row in cls.create_table_items(dialog, search_items, data_getters):
            row = table.rowCount()
            table.insertRow(row)
            [table.setItem(row, col, item) for col, item in enumerate(item_row)]

    @classmethod
    def create_table_items(
        cls, dialog: SearchDialog, search_items: list, getter_methods: list[Callable]
    ):
        """
        Create TableWidgetItems
        :param dialog:
        :return:
        """
        item_list = list()
        for entity in search_items:  # Iterate over Objects or Attributes
            row_data = [
                m(entity) for m in getter_methods
            ]  # use getter Methods for Row Values
            items = [QTableWidgetItem(text) for text in row_data]
            [cls.set_info_of_item(i, entity) for i in items]
            item_list.append(items)
        return item_list

    @classmethod
    def get_row_matchscore(
        cls, table: QTableWidget, search_text: str, row: int, column_count: int
    ) -> float:
        """
        get match-score of Row
        :param table:
        :param search_text:
        :param row:
        :param column_count:
        :return:
        """
        model = table.model()
        texts = [table.item(row, col).text().lower() for col in range(column_count)]
        ratio = max(fuzz.ratio(search_text.lower(), text) for text in texts)
        model.setData(
            model.index(row, column_count), ratio, Qt.ItemDataRole.DisplayRole
        )  # Used for Sorting
        return ratio

    @classmethod
    def get_selected_item(cls, dialog: SearchDialog) -> QTableWidgetItem:
        return dialog.ui.tableWidget.selectedItems()[0]

    @classmethod
    def get_info_from_item(
        cls, item: QTableWidgetItem
    ) -> SOMcreator.SOMClass | SOMcreator.SOMProperty:
        return item.data(CLASS_REFERENCE)

    @classmethod
    def set_info_of_item(
        cls, item: QTableWidgetItem, info: SOMcreator.SOMClass | SOMcreator.SOMProperty
    ):
        item.setData(CLASS_REFERENCE, info)

    @classmethod
    def get_search_mode(cls, dialog: SearchDialog) -> int:
        """
        :param dialog:
        :return: 1 = Object 2= Attribute
        """
        return dialog.search_mode

    @classmethod
    def get_threshold(cls) -> int:
        """
        Integer threshold ot which match-score elements in table should be shown
        :return:
        """
        return cls.get_properties().filter_threshold

    @classmethod
    def get_table(cls, dialog: SearchDialog):
        """
        Getter of Search Table
        :param dialog: Search Window
        :return: Search Table
        """
        return dialog.ui.tableWidget

    @classmethod
    def get_search_text(cls, dialog: SearchDialog):
        """
        Getter of Search Text
        :param dialog: Search Window
        :return: Search Text
        """
        return dialog.ui.lineEdit.text()

    @classmethod
    def get_dialogues(cls) -> set[SearchDialog]:
        """
        return list of active dialogues (len(set) should be 1)
        :return:
        """
        return cls.get_properties().search_dialogues
