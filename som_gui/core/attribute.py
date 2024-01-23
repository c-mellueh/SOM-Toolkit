from __future__ import annotations

import logging

import SOMcreator
from SOMcreator.constants.value_constants import RANGE
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import Attribute, PropertySet
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


def add_basic_attribute_columns(attribute_tool: Type[Attribute]):
    logging.info("Add Basic Attribute Columns")
    attribute_tool.add_column_to_table("Name", attribute_tool.get_attribute_name)
    attribute_tool.add_column_to_table("Datentyp", attribute_tool.get_attribute_data_type)
    attribute_tool.add_column_to_table("Werttyp", attribute_tool.get_attribute_value_type)
    attribute_tool.add_column_to_table("Werte", attribute_tool.get_attribute_values)
    attribute_tool.add_column_to_table("Optional", attribute_tool.is_attribute_optional)


def add_basic_attribute_data(attribute_tool: Type[Attribute]):
    attribute_tool.add_attribute_data_value("name", attribute_tool.get_attribute_name,
                                            attribute_tool.set_attribute_name)
    attribute_tool.add_attribute_data_value("data_type", attribute_tool.get_attribute_data_type,
                                            attribute_tool.set_attribute_data_type)
    attribute_tool.add_attribute_data_value("value_type", attribute_tool.get_attribute_value_type,
                                            attribute_tool.set_attribute_value_type)
    attribute_tool.add_attribute_data_value("values", attribute_tool.get_attribute_values,
                                            attribute_tool.set_attribute_values)
    attribute_tool.add_attribute_data_value("description", attribute_tool.get_attribute_description,
                                            attribute_tool.set_attribute_description)
    attribute_tool.add_attribute_data_value("optional", attribute_tool.is_attribute_optional,
                                            attribute_tool.set_attribute_optional)


def setup_table_header(table: QTableWidget, attribute_tool: Type[Attribute]):
    logging.info(f"Setup Attribute Table Headers")
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


def attribute_clicked(item: QTableWidgetItem, attribute_tool: Type[Attribute], property_set_tool: Type[PropertySet]):
    attribute = attribute_tool.get_attribute_from_item(item)
    window = item.tableWidget().window()
    activate_attribute(attribute, window, attribute_tool, property_set_tool)


def activate_attribute(attribute: SOMcreator.Attribute, window, attribute_tool: Type[Attribute],
                       property_set_tool: Type[PropertySet]):
    name = attribute_tool.get_attribute_name(attribute)
    data_type = attribute_tool.get_attribute_data_type(attribute)
    value_type = attribute_tool.get_attribute_value_type(attribute)
    values = attribute_tool.get_attribute_values(attribute)
    description = attribute_tool.get_attribute_description(attribute)

    property_set_tool.pw_set_attribute_name(name, window)
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


def attribute_double_clicked(item: QTableWidgetItem, attribute_tool: Type[Attribute],
                             property_set_tool: Type[PropertySet]):
    attriute = attribute_tool.get_attribute_from_item(item)
    window = property_set_tool.open_pset_window(property_set_tool.get_active_property_set())
    activate_attribute(attriute, window, attribute_tool, property_set_tool)
