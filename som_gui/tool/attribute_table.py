from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QPoint, Qt
from PySide6.QtGui import QIcon, QPalette
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.main_window.ui import MainWindow
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.property_set_window.ui import PropertySetWindow
from som_gui.resources.icons import get_link_icon

if TYPE_CHECKING:
    from som_gui.module.attribute_table.prop import AttributeTableProperties
    from som_gui.module.attribute_table import ui

LINKSTATE = Qt.ItemDataRole.UserRole + 2


class AttributeTable(som_gui.core.tool.AttributeTable):

    @classmethod
    def get_properties(cls) -> AttributeTableProperties:
        return som_gui.AttributeTableProperties

    @classmethod
    def edit_selected_attribute_name(cls, table: ui.AttributeTable) -> None:
        """
        create Popup for editing selected attribute Name
        :param table:  Active AttributeTable
        :return:
        """
        attributes = cls.get_selected_attributes(table)
        if len(attributes) != 1:
            return
        attribute = list(attributes)[0]
        window = table.window()
        answer = tool.Popups.request_attribute_name(attribute.name, window)
        if answer:
            attribute.name = answer

    @classmethod
    def delete_selected_attributes(cls, table: ui.AttributeTable, with_child=False):
        """
        delete selected Attributes
        param table: Active AttributeTable
        :param with_child: recursive deletion of child elements
        """
        attributes = cls.get_selected_attributes(table)
        for attribute in attributes:
            attribute.delete(with_child)

    @classmethod
    def remove_parent_of_selected_attribute(cls, table: ui.AttributeTable) -> None:
        """
        remove parent of selected attribute
        :param table:
        :return:
        """
        attributes = cls.get_selected_attributes(table)
        for attribute in attributes:
            if not attribute.parent:
                continue
            if not attribute in attribute.parent.get_children(filter=True):
                attribute.parent = None
                continue
            attribute.parent.remove_child(attribute)

    @classmethod
    def add_parent_of_selected_attribute(cls, table: ui.AttributeTable) -> None:
        """
        find possible parent of selected attribute if parent exists add parent to attribute
        :param table: Active AttributeTable
        :return:
        """
        attributes = cls.get_selected_attributes(table)
        for attribute in attributes:
            parent = cls.get_possible_parent(attribute)
            if not parent:
                continue

            parent.add_child(attribute)

    @classmethod
    def remove_attributes_from_table(
        cls, attributes: set[SOMcreator.SOMProperty], table: QTableWidget
    ):
        """
        Remove set of attributes from table
        :param attributes:
        :param table:
        :return:
        """
        row_indexes = sorted(
            [cls.get_row_index_from_attribute(a, table) for a in attributes]
        )
        for row_index in reversed(row_indexes):
            table.removeRow(row_index)

    @classmethod
    def add_attributes_to_table(
        cls, attributes: set[SOMcreator.SOMProperty], table: QTableWidget
    ) -> None:
        """
        add list of Attributes to Table
        :param attributes: Attributes which will be added to table
        :param table: Table to whom attributes will be added
        :return:
        """
        for attribute in attributes:
            table.setSortingEnabled(False)  # disable sorting else bugs will appear
            items = [
                QTableWidgetItem() for _ in range(cls.get_column_count())
            ]  # create QTableWidgetItem for row
            # add row
            row_index = table.rowCount()
            table.setRowCount(row_index + 1)
            # fill row
            [item.setData(CLASS_REFERENCE, attribute) for item in items]
            [table.setItem(row_index, col, item) for col, item in enumerate(items)]
            [
                item.setFlags(item.flags() | item.flags().ItemIsUserCheckable)
                for item in items
            ]
            cls.update_row(table, row_index)
            table.setSortingEnabled(True)

    @classmethod
    def get_column_count(cls) -> int:
        return len(cls.get_properties().attribute_table_columns)

    @classmethod
    def update_row(cls, table: QTableWidget, index: int):
        """
        update row by getter functions. First column get link icon if attribute has parent
        :param table:
        :param index:
        :return:
        """

        row_items = [table.item(index, col) for col in range(cls.get_column_count())]
        attribute = cls.get_attribute_from_item(row_items[0])
        if attribute is None:
            return

        # update row values
        for item, (_, column_getter) in zip(
            row_items, cls.get_properties().attribute_table_columns
        ):
            value = column_getter(attribute)
            cls.format_row_value(item, value)
        cls.format_row(row_items)

        # Update Link Icon
        attribute_has_parent = bool(attribute.parent is not None)
        if (
            not row_items[0].data(LINKSTATE) == attribute_has_parent
        ):  # only update if data changes else infinite update loop
            row_items[0].setIcon(
                get_link_icon() if attribute_has_parent else QIcon()
            )  # update Icon
            row_items[0].setData(LINKSTATE, attribute_has_parent)

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
        Highlights row if attribute is Ident Attribute
        :param row:
        :return:
        """
        attribute = cls.get_attribute_from_item(row[0])
        palette = QPalette()
        if attribute.property_set is None:
            brush = palette.base()
        elif not attribute.property_set.object:
            brush = palette.base()
        elif attribute.property_set.object.ident_attrib == attribute:
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
        :param get_function: getter function for cell value. SOMcreator.Attribute will be passed as argument
        :return:
        """
        cls.get_properties().attribute_table_columns.append((name, get_function))

    @classmethod
    def get_existing_attributes_in_table(cls, table: QTableWidget):
        attributes = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            attributes.add(cls.get_attribute_from_item(item))
        return attributes

    @classmethod
    def get_property_set_by_table(cls, table: QTableWidget) -> SOMcreator.PropertySet:
        window = table.window()
        if isinstance(window, PropertySetWindow):
            return tool.PropertySetWindow.get_property_set_by_window(window)
        if isinstance(window, MainWindow):
            return tool.PropertySet.get_active_property_set()

    @classmethod
    def get_item_from_pos(cls, table: QTableWidget, pos: QPoint):
        item = table.itemAt(pos)
        return cls.get_attribute_from_item(item)

    @classmethod
    def get_attribute_table_header_names(cls):
        prop = cls.get_properties()
        base_names = [name for (name, getter) in prop.attribute_table_columns]
        translation = [
            QCoreApplication.translate("AttributeTable", name) for name in base_names
        ]
        return translation

    @classmethod
    def get_possible_parent(
        cls, attribute: SOMcreator.SOMProperty
    ) -> None | SOMcreator.SOMProperty:
        if not attribute.property_set:
            return None
        if not attribute.property_set.parent:
            return None
        possible_parents = {
            a.name: a for a in attribute.property_set.parent.get_attributes(filter=True)
        }.get(attribute.name)
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
        cls, table: ui.AttributeTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for renaming an attribute.
        :param table: Active Attribute Table
        :return:
        """
        if len(cls.get_selected_attributes(table)) == 1:
            return table.tr("Rename"), lambda: cls.edit_selected_attribute_name(table)
        else:
            return None

    @classmethod
    def context_menu_builder_delete(
        cls, table: ui.AttributeTable, with_child=False
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for deleting an attribute.
        :param table: Active Attribute Table
        :return:
        """

        # return if no attribute is selected
        if len(cls.get_selected_attributes(table)) == 0:
            return None

        # stop user from deleting identifier attribute
        obj = cls.get_property_set_by_table(table).object
        ident_attrib = None if obj is None else obj.ident_attrib
        if ident_attrib in cls.get_selected_attributes(table):
            return None

        # don't show if any attribute is not a parent if deletion with child is requested
        logging.debug([a.is_parent for a in cls.get_selected_attributes(table)])
        if (
            not all(a.is_parent for a in cls.get_selected_attributes(table))
            and with_child
        ):
            return None

        name = (
            table.tr("Delete (with subattributes)")
            if with_child
            else table.tr("Delete")
        )
        return name, lambda: cls.delete_selected_attributes(
            table, with_child=with_child
        )

    @classmethod
    def context_menu_builder_remove_connection(
        cls, table: ui.AttributeTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for removing a parent connect of an attribute.
        :param table: Active Attribute Table
        :return:
        """

        # return if no attribute is selected
        selected_attributes = cls.get_selected_attributes(table)
        if len(selected_attributes) == 0:
            return None

        # don't show if any attribute is not a child
        if not any(a.is_child for a in selected_attributes):
            return None
        return table.tr(
            "Remove Connection"
        ), lambda: cls.remove_parent_of_selected_attribute(table)

    @classmethod
    def context_menu_builder_add_connection(
        cls, table: ui.AttributeTable
    ) -> tuple[str, Callable] | None:
        """
        Contextmenu function for adding a parent connect of an attribute.
        :param table: Active Attribute Table
        :return:
        """
        # return if no attribute is selected
        if len(cls.get_selected_attributes(table)) == 0:
            return None

        # don't show if no possible parent is found
        possible_parents = [
            (a, cls.get_possible_parent(a)) for a in cls.get_selected_attributes(table)
        ]
        if not any(
            parent is not None for a, parent in possible_parents if a.parent != parent
        ):
            return None

        return table.tr(
            "Connect to Parent"
        ), lambda: cls.add_parent_of_selected_attribute(table)

    @classmethod
    def set_property_set_of_table(
        cls, table: ui.AttributeTable, property_set: SOMcreator.PropertySet
    ) -> None:
        """
        define which property_set is shown in AttributeTable
        :param table: active AttributeTable
        :param property_set: PropertySet which will be linked
        :return:
        """
        table.property_set = property_set

    @classmethod
    def get_property_set_of_table(
        cls, table: ui.AttributeTable
    ) -> SOMcreator.PropertySet | None:
        """
        get property set of table
        :param table: active AttributeTable
        :return:
        """
        return table.property_set

    @classmethod
    def get_row_index_from_attribute(
        cls, attribute: SOMcreator.SOMProperty, table: QTableWidget
    ) -> int:
        """
        :return: Row index
        """
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_attribute_from_item(item) == attribute:
                return row

    @classmethod
    def get_selected_attributes(
        cls, table: ui.AttributeTable
    ) -> set[SOMcreator.SOMProperty]:
        """
        :param table: Active AttributeTable
        :return: selected attributes in AttributeTable
        """
        return {cls.get_attribute_from_item(item) for item in table.selectedItems()}

    @classmethod
    def get_attribute_from_item(
        cls, item: QTableWidgetItem
    ) -> SOMcreator.SOMProperty | None:
        """
        return the Attribute which is linked to a table entry
        :param item:
        :return:
        """
        if item is None:
            return None
        entity = item.data(CLASS_REFERENCE)
        return entity if isinstance(entity, SOMcreator.SOMProperty) else None
