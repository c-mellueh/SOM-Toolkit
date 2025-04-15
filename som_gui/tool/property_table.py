from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

from PySide6.QtCore import (
    QCoreApplication,
    QPoint,
    Qt,
    QMimeData,
    QByteArray,
    Signal,
    QObject,
)
from PySide6.QtGui import QIcon, QPalette, QDropEvent
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.main_window.ui import MainWindow
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.property_set_window.ui import PropertySetWindow
from som_gui.resources.icons import get_link_icon
from som_gui.module.property_table.constants import MIME_DATA_KEY
from som_gui.module.property_table import trigger
if TYPE_CHECKING:
    from som_gui.module.property_table.prop import PropertyTableProperties
from som_gui.module.property_table import ui

LINKSTATE = Qt.ItemDataRole.UserRole + 2
import pickle


class Signaller(QObject):
    property_info_requested = Signal(SOMcreator.SOMProperty)
    translation_requested = Signal(ui.PropertyTable)

class PropertyTable(som_gui.core.tool.PropertyTable):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> PropertyTableProperties:
        return som_gui.PropertyTableProperties

    @classmethod
    def connect_table(cls, table: ui.PropertyTable):
        print("CONNECT TABLE")
        table.doubleClicked.connect(
            lambda i: cls.signaller.property_info_requested.emit(
                cls.get_property_from_item(i)
            )
        )
        cls.signaller.translation_requested.connect(trigger.retranslate_ui)
    @classmethod
    def edit_selected_property_name(cls, table: ui.PropertyTable) -> None:
        """
        create Popup for editing selected property Name
        :param table:  Active PropertyTable
        :return:
        """
        selected_properties = cls.get_selected_properties(table)
        if len(selected_properties) != 1:
            return
        som_property = list(selected_properties)[0]
        window = table.window()
        answer = tool.Popups.request_property_name(som_property.name, window)
        if answer:
            som_property.name = answer

    @classmethod
    def delete_selected_properties(cls, table: ui.PropertyTable, with_child=False):
        """
        delete selected Properties
        param table: Active PropertyTable
        :param with_child: recursive deletion of child elements
        """
        selected_properties = cls.get_selected_properties(table)
        for som_property in selected_properties:
            som_property.delete(with_child)

    @classmethod
    def remove_parent_of_selected_properties(cls, table: ui.PropertyTable) -> None:
        """
        remove parent of selected property
        :param table:
        :return:
        """
        selected_properties = cls.get_selected_properties(table)
        for som_property in selected_properties:
            if not som_property.parent:
                continue
            if not som_property in som_property.parent.get_children(filter=True):
                som_property.parent = None
                continue
            som_property.parent.remove_child(som_property)

    @classmethod
    def add_parent_of_selected_properties(cls, table: ui.PropertyTable) -> None:
        """
        find possible parent of selected property if parent exists add parent to property
        :param table: Active PropertyTable
        :return:
        """
        selected_properties = cls.get_selected_properties(table)
        for som_property in selected_properties:
            parent = cls.get_possible_parent(som_property)
            if not parent:
                continue

            parent.add_child(som_property)

    @classmethod
    def remove_properties_from_table(
        cls, properties: set[SOMcreator.SOMProperty], table: QTableWidget
    ):
        """
        Remove set of properties from table
        :param properties:
        :param table:
        :return:
        """
        row_indexes = sorted(
            [cls.get_row_index_from_property(a, table) for a in properties]
        )
        for row_index in reversed(row_indexes):
            table.removeRow(row_index)

    @classmethod
    def add_properties_to_table(
        cls, properties: set[SOMcreator.SOMProperty], table: QTableWidget
    ) -> None:
        """
        add list of Properties to Table
        :param properties: Properties which will be added to table
        :param table: Table to whom properties will be added
        :return:
        """
        for som_property in properties:
            table.setSortingEnabled(False)  # disable sorting else bugs will appear
            items = [
                QTableWidgetItem() for _ in range(cls.get_column_count())
            ]  # create QTableWidgetItem for row
            # add row
            row_index = table.rowCount()
            table.setRowCount(row_index + 1)
            # fill row
            [item.setData(CLASS_REFERENCE, som_property) for item in items]
            [table.setItem(row_index, col, item) for col, item in enumerate(items)]
            [
                item.setFlags(item.flags() | item.flags().ItemIsUserCheckable)
                for item in items
            ]
            cls.update_row(table, row_index)
            table.setSortingEnabled(True)

    @classmethod
    def get_column_count(cls) -> int:
        return len(cls.get_properties().property_table_columns)

    @classmethod
    def update_row(cls, table: QTableWidget, index: int):
        """
        update row by getter functions. First column get link icon if property has parent
        :param table:
        :param index:
        :return:
        """

        row_items = [table.item(index, col) for col in range(cls.get_column_count())]
        som_property = cls.get_property_from_item(row_items[0])
        if som_property is None:
            return

        # update row values
        for item, (_, column_getter) in zip(
            row_items, cls.get_properties().property_table_columns
        ):
            value = column_getter(som_property)
            cls.format_row_value(item, value)
        cls.format_row(row_items)

        # Update Link Icon
        if (
            not row_items[0].data(LINKSTATE) == som_property.is_child
        ):  # only update if data changes else infinite update loop
            if som_property.is_child:
                row_items[0].setIcon(get_link_icon())
                parent = som_property.parent.property_set
                class_name = (
                    QCoreApplication.translate(
                        "PropertyTable", "Predefined PropertySet"
                    )
                    if parent.is_predefined
                    else parent.som_class.name
                )
                text = QCoreApplication.translate(
                    "PropertyTable", "Inherits Settings from {}"
                ).format(class_name)
                row_items[0].setToolTip(
                    QCoreApplication.translate("PropertyTable", text)
                )
            else:
                row_items[0].setIcon(QIcon())
                row_items[0].setToolTip("")
            row_items[0].setData(LINKSTATE, som_property.is_child)

    @classmethod
    def format_row_value(
        cls, item: QTableWidgetItem, value: str | set | bool | list | float
    ):
        """
        Formats value to match cell style based on datatype
        :param item:
        :param value:
        :return:
        """
        if isinstance(value, (list, set)):
            item.setText("; ".join([str(v) for v in value]))
            return
        if isinstance(value, bool):
            cs = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            item.setText("")
            item.setCheckState(cs)
            return
        if value is None:
            value = ""
        item.setText(str(value))

    @classmethod
    def format_row(cls, row: list[QTableWidgetItem]) -> None:
        """
        Highlights row if property is Ident Property
        :param row:
        :return:
        """
        som_property = cls.get_property_from_item(row[0])
        palette = QPalette()
        if som_property.property_set is None:
            brush = palette.base()
        elif not som_property.property_set.som_class:
            brush = palette.base()
        elif som_property.property_set.som_class.identifier_property == som_property:
            brush = palette.mid()
        else:
            brush = palette.base()
        for item in row:
            item.setBackground(brush)

    @classmethod
    def add_column_to_table(cls, name: str, get_function: Callable) -> None:
        """
        Define Column which should be shown in Table
        :param name: Name of Column
        :param get_function: getter function for cell value. SOMcreator.SOMProperty will be passed as argument
        :return:
        """
        cls.get_properties().property_table_columns.append((name, get_function))

    @classmethod
    def get_existing_properties(cls, table: QTableWidget):
        properties = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            properties.add(cls.get_property_from_item(item))
        return properties

    @classmethod
    def get_item_from_pos(cls, table: QTableWidget, pos: QPoint):
        item = table.itemAt(pos)
        return cls.get_property_from_item(item)

    @classmethod
    def get_header_labels(cls):
        prop = cls.get_properties()
        base_names = [name for (name, getter) in prop.property_table_columns]
        translation = [
            QCoreApplication.translate("PropertyTable", name) for name in base_names
        ]
        return translation

    @classmethod
    def get_possible_parent(
        cls, som_property: SOMcreator.SOMProperty
    ) -> None | SOMcreator.SOMProperty:
        if not som_property.property_set:
            return None
        if not som_property.property_set.parent:
            return None
        possible_parents = {
            a.name: a
            for a in som_property.property_set.parent.get_properties(filter=True)
        }.get(som_property.name)
        return possible_parents if possible_parents else None

    @classmethod
    def get_context_menu_builders(cls) -> list:
        """
        Functions that are getting called if context menu is requested. Return tuple with name and function or None # Each builder gets passed the current table
        """
        return cls.get_properties().context_menu_builders

    @classmethod
    def add_context_menu_builder(cls, context_menu_builder: Callable):
        """
        :param context_menu_builder: Function which gets called on context menu creation.
        should return tuple[name, function] of context should be shown or None if not shown.
        The function gets passed the current table as a variable
        :return:
        """
        cls.get_properties().context_menu_builders.append(context_menu_builder)

    @classmethod
    def context_menu_builder_rename(
        cls, table: ui.PropertyTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for renaming an property.
        :param table: Active Property Table
        :return:
        """
        if len(cls.get_selected_properties(table)) == 1:
            return QCoreApplication.translate(
                "PropertyTable", "Rename"
            ), lambda: cls.edit_selected_property_name(table)
        else:
            return None

    @classmethod
    def context_menu_builder_delete(
        cls, table: ui.PropertyTable, with_child=False
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for deleting an property.
        :param table: Active Property Table
        :return:
        """

        # return if no property is selected
        if len(cls.get_selected_properties(table)) == 0:
            return None

        # stop user from deleting identifier property
        som_class = cls.get_property_set_by_table(table).som_class
        ident_property = None if som_class is None else som_class.identifier_property
        if ident_property in cls.get_selected_properties(table):
            return None

        # don't show if any property is not a parent if deletion with child is requested
        logging.debug([a.is_parent for a in cls.get_selected_properties(table)])
        if (
            not all(a.is_parent for a in cls.get_selected_properties(table))
            and with_child
        ):
            return None
        text = (
            QCoreApplication.translate("PropertyTable", "Delete (with subproperties)")
            if with_child
            else QCoreApplication.translate("PropertyTable", "Delete")
        )
        return text, lambda: cls.delete_selected_properties(
            table, with_child=with_child
        )

    @classmethod
    def context_menu_builder_remove_connection(
        cls, table: ui.PropertyTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for removing a parent connect of an property.
        :param table: Active Property Table
        :return:
        """

        # return if no property is selected
        selected_properties = cls.get_selected_properties(table)
        if len(selected_properties) == 0:
            return None

        # don't show if any property is not a child
        if not any(a.is_child for a in selected_properties):
            return None
        text = QCoreApplication.translate("PropertyTable", "Remove Connection")
        return text, lambda: cls.remove_parent_of_selected_properties(table)

    @classmethod
    def context_menu_builder_add_connection(
        cls, table: ui.PropertyTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for adding a parent connect of an property.
        :param table: Active Property Table
        :return:
        """
        # return if no property is selected
        if len(cls.get_selected_properties(table)) == 0:
            return None

        # don't show if no possible parent is found
        possible_parents = [
            (a, cls.get_possible_parent(a)) for a in cls.get_selected_properties(table)
        ]
        if not any(
            parent is not None for a, parent in possible_parents if a.parent != parent
        ):
            return None

        return table.tr(
            "Connect to Parent"
        ), lambda: cls.add_parent_of_selected_properties(table)

    @classmethod
    def set_property_set_of_table(
        cls, table: ui.PropertyTable, property_set: SOMcreator.SOMPropertySet
    ) -> None:
        """
        define which property_set is shown in PropertyTable
        :param table: active PropertyTable
        :param property_set: PropertySet which will be linked
        :return:
        """
        table.property_set = property_set

    @classmethod
    def get_property_set_of_table(
        cls, table: ui.PropertyTable
    ) -> SOMcreator.SOMPropertySet | None:
        """
        get property set of table
        :param table: active PropertyTable
        :return:
        """
        return table.property_set

    @classmethod
    def get_property_set_by_table(
        cls, table: QTableWidget
    ) -> SOMcreator.SOMPropertySet | None:
        return table.property_set
    @classmethod
    def get_row_index_from_property(
        cls, som_property: SOMcreator.SOMProperty, table: QTableWidget
    ) -> int:
        """
        :return: Row index
        """
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_property_from_item(item) == som_property:
                return row

    @classmethod
    def get_selected_properties(
        cls, table: ui.PropertyTable
    ) -> set[SOMcreator.SOMProperty]:
        """
        :param table: Active PropertyTable
        :return: selected properties in PropertyTable
        """
        return {cls.get_property_from_item(item) for item in table.selectedItems()}

    @classmethod
    def get_property_from_item(
        cls, item: QTableWidgetItem
    ) -> SOMcreator.SOMProperty | None:
        """
        return the Property which is linked to a table entry
        :param item:
        :return:
        """
        if item is None:
            return None
        entity = item.data(CLASS_REFERENCE)
        return entity if isinstance(entity, SOMcreator.SOMProperty) else None

    @classmethod
    def is_drop_allowed(cls, event: QDropEvent, target_table: QTableWidget):
        if event.proposedAction() not in [
            Qt.DropAction.MoveAction,
            Qt.DropAction.CopyAction,
        ]:
            return False
        source_table: ui.PropertyTable = event.source()  # type: ignore
        if source_table == target_table:
            event.accept()
            return False
        if not isinstance(source_table, ui.PropertyTable | None):
            return False
        return True

    @classmethod
    def write_property_dicts_to_mime_data(
        cls, property_dicts: list[dict], mime_data: QMimeData
    ):
        """
        write properties to MimeData
        :param properties:
        :param mime_data:
        :return:
        """
        serialized = pickle.dumps(property_dicts)
        mime_data.setData(MIME_DATA_KEY, QByteArray(serialized))
        return mime_data

    @classmethod
    def get_property_dict_from_mime_data(
        cls,
        mime_data: QMimeData,
    ) -> list[dict]:
        """
        get PropertyDict from MimeData
        :param mime_data:
        :param property_tool:
        :return:
        """
        pickled_data = mime_data.data(MIME_DATA_KEY)
        if not pickled_data:
            return
        property_dicts = pickle.loads(pickled_data)
        return property_dicts
