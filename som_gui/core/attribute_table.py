from __future__ import annotations

import logging

import SOMcreator
from SOMcreator.constants.value_constants import RANGE
from typing import TYPE_CHECKING, Type
from som_gui import tool

if TYPE_CHECKING:
    from som_gui.tool import Attribute, PropertySet
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


def context_menu(table, pos, property_set: Type[tool.PropertySet], attribute_table: Type[tool.AttributeTable]):
    active_attribute = attribute_table.get_item_from_pos(table, pos)
    attribute_table.set_active_table(table)
    attribute_table.set_active_attribute(active_attribute)
    if active_attribute.property_set.object.ident_attrib == active_attribute:

        actions = [["Umbenennen", attribute_table.edit_attribute_name], ]
    else:

        actions = [["Umbenennen", attribute_table.edit_attribute_name],
                   ["Löschen", attribute_table.delete_selected_attribute], ]
    property_set.create_context_menu(table.mapToGlobal(pos), actions)


def add_basic_attribute_columns(attribute: Type[tool.Attribute], attribute_table: Type[tool.AttributeTable]):
    logging.info("Add Basic Attribute Columns")
    attribute_table.add_column_to_table("Name", attribute.get_attribute_name)
    attribute_table.add_column_to_table("Datentyp", attribute.get_attribute_data_type)
    attribute_table.add_column_to_table("Werttyp", attribute.get_attribute_value_type)
    attribute_table.add_column_to_table("Werte", attribute.get_attribute_values)
    attribute_table.add_column_to_table("Optional", attribute.is_attribute_optional)


def attribute_clicked(item: QTableWidgetItem, attribute_tool: Type[Attribute], property_set_tool: Type[PropertySet]):
    attribute = attribute_tool.get_attribute_from_item(item)
    attribute_tool.set_active_attribute(attribute)
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


def paint_attribute_table(table: QTableWidget, attribute_table: Type[tool.AttributeTable]):
    existing_attributes = attribute_table.get_existing_attributes_in_table(table)
    property_set = attribute_table.get_property_set_by_table(table)
    if property_set is None:
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)
        return
    delete_attributes = existing_attributes.difference(set(property_set.attributes))
    new_attributes = set(property_set.attributes).difference(existing_attributes)
    attribute_table.remove_attributes_from_table(delete_attributes, table)
    attribute_table.add_attributes_to_table(sorted(new_attributes), table)
    for row in range(table.rowCount()):
        attribute_table.update_row(table, row)
