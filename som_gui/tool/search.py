from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import QCoreApplication, Qt, QObject, Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

import som_gui
import som_gui.core.tool
from som_gui import __version__ as version
from som_gui import tool
from som_gui.module import search
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.search import trigger, constants

if TYPE_CHECKING:
    from som_gui.module.search.prop import SearchProperties
from som_gui.module.search.ui import SearchDialog
import SOMcreator
from thefuzz import fuzz


class Signaller(QObject):
    update_requested = Signal(SearchDialog)
    strict_state_changed = Signal(bool)


class Search(som_gui.core.tool.Search):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> SearchProperties:
        return som_gui.SearchProperties

    @classmethod
    def connect_signals(cls):
        cls.signaller.update_requested.connect(trigger.refresh_window)
        cls.signaller.strict_state_changed.connect(trigger.set_strict_state)

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
        cls.retranslate_title(search_dialog, search_mode)
        search_dialog.ui.lineEdit.textChanged.connect(
            lambda: cls.signaller.update_requested.emit(search_dialog)
        )
        check_box = search_dialog.ui.checkBox_strict
        check_state = tool.Appdata.get_bool_setting(
            constants.SEARCH_SECTION, constants.STRICT_SETTING, False
        )
        if check_state:
            check_box.setChecked(check_state)

        check_box.checkStateChanged.connect(
            lambda: cls.signaller.update_requested.emit(search_dialog)
        )
        check_box.checkStateChanged.connect(
            lambda: cls.signaller.strict_state_changed.emit(check_box.isChecked())
        )

        if not search_dialog.exec_():
            prop.search_dialogues.remove(search_dialog)
            return None
        prop.search_dialogues.remove(search_dialog)
        return search_dialog.return_value

    @classmethod
    def search_class(
        cls, searchable_classes: list[SOMcreator.SOMClass]
    ) -> SOMcreator.SOMClass | None:
        """
        Opens SearchWindow which searches for a class
        :param searchable_classes: Classes which will be visible in Search Table
        :return:

        """
        # Create Getter Methods for Columns
        getter_methods = [
            lambda o: getattr(o, "name"),
            lambda o: getattr(o, "ident_value"),
            lambda o: getattr(o, "abbreviation"),  # TODO: Add plugin function
        ]
        return cls._search(1, searchable_classes, getter_methods)

    @classmethod
    def search_property(
        cls, searchable_properties: list[SOMcreator.SOMProperty]
    ) -> SOMcreator.SOMProperty | None:
        """
        Opens SearchWindow which searches for a Property
        :param searchable_properties: Properties which will be visible in Search Table

        :return:
        """
        getter_methods = [
            lambda a: getattr(a, "property_set").name,
            lambda a: getattr(a, "name"),
        ]
        return cls._search(2, searchable_properties, getter_methods)

    @classmethod
    def get_column_texts(cls, search_mode: int) -> list[str]:
        """
        Get text of Columns for different search_modes
        :return:
        """
        if search_mode == 1:
            return [
                QCoreApplication.translate("Search", "Class"),
                QCoreApplication.translate("Search", "Identifier"),
                QCoreApplication.translate("Search", "Abbreviation"),
            ]
        if search_mode == 2:
            return [
                QCoreApplication.translate("Search", "PropertySet"),
                QCoreApplication.translate("Search", "Property"),
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
            title = QCoreApplication.translate("Search", "Search Class")
        elif search_mode == 2:
            title = QCoreApplication.translate("Search", "Search Property")

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
        for entity in search_items:  # Iterate over Classes or Properties
            row_data = [
                m(entity) for m in getter_methods
            ]  # use getter Methods for Row Values
            items = [QTableWidgetItem(text) for text in row_data]
            [cls.set_info_of_item(i, entity) for i in items]
            item_list.append(items)
        return item_list

    @classmethod
    def get_row_matchscore(
        cls, dialog: SearchDialog, search_text: str, row: int, column_count: int
    ) -> float:
        """
        get match-score of Row
        :param table:
        :param search_text:
        :param row:
        :param column_count:
        :return:
        """
        table = cls.get_table(dialog)
        model = table.model()
        texts = [table.item(row, col).text().lower() for col in range(column_count)]
        search_text = search_text.lower()

        def calc_ratio(t, index):
            if search_text == t:
                return 1000
            if cls.is_in_strict_model(dialog):
                return fuzz.ratio(search_text, t) * 1.0 - 0.1 * index
            else:
                return fuzz.partial_ratio(search_text, t) * 1.0 - 0.1 * index

        ratio = max(calc_ratio(text, index) for index, text in enumerate(texts))

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
        :return: 1 = Class 2= Property
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

    @classmethod
    def is_in_strict_model(cls, dialog: SearchDialog):
        return dialog.ui.checkBox_strict.isChecked()
