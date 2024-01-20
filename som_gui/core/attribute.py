from __future__ import annotations
from PySide6.QtWidgets import QTableWidget

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import Attribute


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
