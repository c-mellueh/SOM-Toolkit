from __future__ import annotations

import copy

import SOMcreator

from som_gui.core import property_set_window as property_set_window_core
import logging
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import QMimeData, Qt

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
    from PySide6.QtGui import QDropEvent
    from som_gui.module.attribute_table import ui


def item_changed(item: QTableWidgetItem, attribute_table: Type[tool.AttributeTable]):
    attribute = attribute_table.get_attribute_from_item(item)
    if not item.column() == 4:
        return
    cs = True if item.checkState() == Qt.CheckState.Checked else False
    attribute.optional = cs


def drop_event(event: QDropEvent, table: ui.AttributeTable, property_set_window: Type[tool.PropertySetWindow],
               attribute_tool: Type[tool.Attribute]):
    attributes: set[SOMcreator.Attribute] = event.mimeData().property("Objects")
    window = table.window()
    source_window = event.source().window()
    if source_window == window:
        event.accept()
        return

    proposed_action = event.proposedAction()
    property_set = property_set_window.get_property_set_by_window(window)

    existing_attributes = {a.name: a for a in property_set.get_all_attributes()}

    if proposed_action == Qt.DropAction.CopyAction:
        for attribute in attributes:
            existing_attribute = existing_attributes.get(attribute.name)
            if existing_attribute:
                data = attribute_tool.get_attribute_data(attribute)
                attribute_tool.set_attribute_data(existing_attribute, data)
            else:
                attribute = copy.copy(attribute)
                attribute.remove_parent()
                property_set.add_attribute(attribute)

    elif proposed_action == Qt.DropAction.MoveAction:
        for attribute in attributes:
            existing_attribute = existing_attributes.get(attribute.name)
            if existing_attribute:
                property_set.remove_attribute(existing_attribute)
            property_set.add_attribute(attribute)
            attribute.remove_parent()
    event.accept()


def create_mime_data(items: list[QTableWidgetItem], mime_data: QMimeData, attribute_table: Type[tool.AttributeTable]):
    objects = {attribute_table.get_attribute_from_item(item) for item in items}
    mime_data.setProperty("Objects", objects)
    return mime_data


def context_menu(table: ui.AttributeTable, pos, property_set: Type[tool.PropertySet],
                 attribute_table: Type[tool.AttributeTable]):
    active_attribute = attribute_table.get_item_from_pos(table, pos)
    attribute_table.set_active_table(table)
    attribute_table.set_active_attribute(active_attribute)
    if active_attribute is None:
        return

    actions = [["Umbenennen", attribute_table.edit_attribute_name],
               ["Löschen", lambda: attribute_table.delete_selected_attribute(False)], ]

    if active_attribute.property_set.object:
        if active_attribute.property_set.object.ident_attrib == active_attribute:
            actions = [["Umbenennen", attribute_table.edit_attribute_name], ]

    if active_attribute.is_child:
        actions.append(["Verknüpfung Lösen", attribute_table.remove_parent_of_selected_attribute])
    else:
        possible_parent = attribute_table.get_possible_parent(active_attribute)
        if possible_parent:
            actions.append(["Verknüpfung Hinzufügen", attribute_table.add_parent_of_selected_attribute])

    if active_attribute.is_parent:
        actions.append(["Löschen (mit Verknüpfung)", lambda: attribute_table.delete_selected_attribute(True)])


    property_set.create_context_menu(table.viewport().mapToGlobal(pos), actions)


def add_basic_attribute_columns(attribute: Type[tool.Attribute], attribute_table: Type[tool.AttributeTable]):
    logging.info("Add Basic Attribute Columns")
    attribute_table.add_column_to_table("Name", attribute.get_attribute_name)
    attribute_table.add_column_to_table("Datentyp", attribute.get_attribute_data_type)
    attribute_table.add_column_to_table("Werttyp", attribute.get_attribute_value_type)
    attribute_table.add_column_to_table("Werte", attribute.get_attribute_values)
    attribute_table.add_column_to_table("Optional", attribute.is_attribute_optional)


def attribute_double_clicked(item: QTableWidgetItem, attribute: Type[tool.Attribute],
                             attribute_table: Type[tool.AttributeTable],
                             property_set: Type[tool.PropertySet], property_set_window: Type[tool.PropertySetWindow]):
    active_attribute = attribute_table.get_attribute_from_item(item)
    active_property_set = property_set.get_active_property_set()
    window = property_set_window_core.open_pset_window(active_property_set, property_set_window, attribute_table)
    property_set_window_core.activate_attribute(active_attribute, window, attribute, property_set_window)


def paint_attribute_table(table: QTableWidget, attribute_table: Type[tool.AttributeTable]):
    logging.debug(f"Repaint Attribute Table")

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


def setup_table_header(main_window: Type[tool.MainWindow], attribute_table: Type[tool.AttributeTable]):
    table = main_window.get_attribute_table()
    logging.info(f"Setup Attribute Table Headers")
    header_texts = attribute_table.get_attribute_table_header_names()
    table.setColumnCount(len(header_texts))
    table.setHorizontalHeaderLabels(header_texts)
