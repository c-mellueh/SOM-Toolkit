from __future__ import annotations
from SOMcreator.constants.value_constants import RANGE
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import Attribute, PropertySet
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


def add_basic_attribute_columns(attribute_tool: Type[Attribute]):
    attribute_tool.add_column_to_table("Name", attribute_tool.get_attribute_name)
    attribute_tool.add_column_to_table("Datentyp", attribute_tool.get_attribute_data_type)
    attribute_tool.add_column_to_table("Werttyp", attribute_tool.get_attribute_value_type)
    attribute_tool.add_column_to_table("Werte", attribute_tool.get_attribute_values)
    attribute_tool.add_column_to_table("Optional", attribute_tool.is_attribute_optional)


def setup_table_header(table: QTableWidget, attribute_tool: Type[Attribute]):
    header_texts = attribute_tool.get_attribute_table_header_names()
    table.setColumnCount(len(header_texts))
    table.setHorizontalHeaderLabels(header_texts)


def refresh_attribute_table(table: QTableWidget, attribute_tool: Type[Attribute]):
    existing_attributes = attribute_tool.get_existing_attributes_in_table(table)
    property_set = attribute_tool.get_property_set_by_table(table)
    if property_set is None:
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)
        return
    delete_attributes = existing_attributes.difference(set(property_set.attributes))
    new_attributes = set(property_set.attributes).difference(existing_attributes)
    attribute_tool.remove_attributes_from_table(delete_attributes, table)
    attribute_tool.add_attributes_to_table(sorted(new_attributes), table)
    for row in range(table.rowCount()):
        attribute_tool.update_row(table, row)
    table.resizeColumnsToContents()


def attribute_clicked(item: QTableWidgetItem, attribute_tool: Type[Attribute], property_set_tool: Type[PropertySet]):
    attribute = attribute_tool.get_attribute_from_item(item)
    data_type = attribute_tool.get_attribute_data_type(attribute)
    value_type = attribute_tool.get_attribute_value_type(attribute)
    values = attribute_tool.get_attribute_values(attribute)
    description = attribute_tool.get_attribute_description(attribute)
    window = item.tableWidget().window()

    property_set_tool.pw_set_data_type(data_type, window)
    property_set_tool.pw_set_value_type(value_type, window)
    property_set_tool.pw_set_description(description, window)
    property_set_tool.pw_toggle_comboboxes(attribute, window)

    property_set_tool.pw_clear_values(window)
    property_set_tool.pw_set_values(values, window)
    if not values:
        if value_type == RANGE:
            property_set_tool.pw_add_value_line(2, window)
        else:
            property_set_tool.pw_add_value_line(1, window)
