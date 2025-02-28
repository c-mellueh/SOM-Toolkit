from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData, Qt

import SOMcreator
from som_gui.core import property_set_window as property_set_window_core
from som_gui.module.attribute_table.constants import MIME_DATA_KEY

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
    from PySide6.QtGui import QDropEvent
    from som_gui.module.attribute_table import ui
    from som_gui.module.property_set_window.ui import PropertySetWindow


def init_context_menu(attribute_table: Type[tool.AttributeTable]):
    """
    Defines all standard context menu actions associated with an attribute table.
    """
    attribute_table.add_context_menu_builder(
        attribute_table.context_menu_builder_rename
    )
    attribute_table.add_context_menu_builder(
        lambda t: attribute_table.context_menu_builder_delete(t, False)
    )
    attribute_table.add_context_menu_builder(
        lambda t: attribute_table.context_menu_builder_delete(t, True)
    )
    attribute_table.add_context_menu_builder(
        attribute_table.context_menu_builder_remove_connection
    )
    attribute_table.add_context_menu_builder(
        attribute_table.context_menu_builder_add_connection
    )


def init_attribute_columns(attribute_table: Type[tool.AttributeTable]):
    """
    Defines all attribute columns associated with an attribute table. This can be expanded by plugins
    :param attribute_table:
    :return:
    """
    logging.info("Add Basic Attribute Columns")
    # write translations so Qtlinguist knows them
    name = QCoreApplication.translate("AttributeTable", "Name")
    datatype = QCoreApplication.translate("AttributeTable", "Datatype")
    valuetype = QCoreApplication.translate("AttributeTable", "Valuetype")
    value = QCoreApplication.translate("AttributeTable", "Value")
    optional = QCoreApplication.translate("AttributeTable", "Optional")
    unit = QCoreApplication.translate("AttributeTable", "Unit")

    attribute_table.add_column_to_table("Name", lambda a: a.name)
    attribute_table.add_column_to_table("Datatype", lambda a: a.data_type)
    attribute_table.add_column_to_table("Valuetype", lambda a: a.value_type)
    attribute_table.add_column_to_table("Unit", lambda a: a.unit)
    attribute_table.add_column_to_table("Value", lambda a: a.value)
    attribute_table.add_column_to_table(
        "Optional", lambda a: a.is_optional(ignore_hirarchy=True)
    )


def retranslate_ui(
    table: ui.AttributeTable,
    attribute_table: Type[tool.AttributeTable],
    main_window: Type[tool.MainWindow],
):
    if table is None:
        table = main_window.get_attribute_table()
    labels = attribute_table.get_attribute_table_header_names()
    table.setHorizontalHeaderLabels(labels)


def toggle_optionality(
    item: QTableWidgetItem, attribute_table: Type[tool.AttributeTable]
):
    """
    change the optionality of an attribute by their QTableWidgetItem
    :param item:
    :param attribute_table:
    :return:
    """
    attribute = attribute_table.get_attribute_from_item(item)
    if not item.column() == 4:
        return
    cs = True if item.checkState() == Qt.CheckState.Checked else False
    attribute.set_optional(cs)


def create_mime_data(
    items: list[QTableWidgetItem],
    mime_data: QMimeData,
    attribute_table: Type[tool.AttributeTable],
) -> QMimeData:
    """
    create MimeData used for Dropping Attributes into different Tables
    """
    objects = {attribute_table.get_attribute_from_item(item) for item in items}
    mime_data.setProperty(MIME_DATA_KEY, objects)
    return mime_data


def drop_event(
    event: QDropEvent,
    target_table: ui.AttributeTable,
    attribute_table: Type[tool.AttributeTable],
    attribute_tool: Type[tool.Attribute],
):
    """
    handling of dropping of attribute row from a property set window to another property set window
    :param target_table: table on which the attribute is dropped on
    :return:
    """

    # Check if move is inside the same window
    source_table: ui.AttributeTable = event.source()
    if source_table == target_table:
        event.accept()
        return

    proposed_action = event.proposedAction()
    target_property_set = attribute_table.get_property_set_by_table(target_table)
    existing_attributes = {
        a.name: a for a in target_property_set.get_attributes(filter=False)
    }
    dropped_attributes: set[SOMcreator.SOMProperty] = event.mimeData().property(
        MIME_DATA_KEY
    )  # get set of dropped Attributes

    if proposed_action == Qt.DropAction.CopyAction:
        for attribute in dropped_attributes:
            # check if Attribute with same name exists already
            existing_attribute = existing_attributes.get(attribute.name)
            if existing_attribute:
                # overwrite date
                data = attribute_tool.get_attribute_data(attribute)
                attribute_tool.set_attribute_data_by_dict(existing_attribute, data)
            else:
                # copy attribute to property_set
                attribute = copy.copy(attribute)
                attribute.remove_parent()
                target_property_set.add_property(attribute)

    elif proposed_action == Qt.DropAction.MoveAction:
        for attribute in dropped_attributes:
            # check if Attribute with same name exists already
            existing_attribute = existing_attributes.get(attribute.name)
            if existing_attribute:
                # replace Attribute
                target_property_set.remove_attribute(existing_attribute)
            target_property_set.add_property(attribute)
            attribute.remove_parent()  # remove ParentAttribute
    target_table.repaint()
    event.accept()


def create_context_menu(
    table: ui.AttributeTable,
    pos,
    attribute_table: Type[tool.AttributeTable],
    util: Type[tool.Util],
):
    """
    Create Context Menu based on context menu builders
    """

    # see tool.AttributeTable.add_context_menu_builder

    menu_list = list()

    # Create list of context menu entries
    for context_menu_builder in attribute_table.get_context_menu_builders():
        result = context_menu_builder(table)
        if result is not None:
            menu_list.append(result)

    menu = util.create_context_menu(menu_list)
    # Run Context Menu
    menu.exec(table.viewport().mapToGlobal(pos))


def activate_item(
    item: QTableWidgetItem,
    attribute_table: Type[tool.AttributeTable],
    property_set: Type[tool.PropertySet],
    property_set_window: Type[tool.PropertySetWindow],
):
    """
    Activate Attribute based on QTableWidgetItem
    :return:
    """
    active_attribute = attribute_table.get_attribute_from_item(item)
    active_property_set = property_set.get_active_property_set()
    # create Window or activate it
    window = property_set_window_core.open_pset_window(
        active_property_set, property_set_window, attribute_table
    )
    property_set_window_core.activate_attribute(
        active_attribute, window, property_set_window
    )


def update_attribute_table(
    table: QTableWidget, attribute_table: Type[tool.AttributeTable]
):
    logging.debug(f"Repaint Attribute Table")

    existing_attributes = attribute_table.get_existing_attributes_in_table(table)
    property_set = attribute_table.get_property_set_by_table(table)
    if property_set is None:
        # clear Table
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)
        return

    if attribute_table.get_column_count() > table.columnCount():
        for _ in range(attribute_table.get_column_count() - table.columnCount()):
            table.insertColumn(table.columnCount())
    if attribute_table.get_column_count() < table.columnCount():
        for _ in range(table.columnCount() - attribute_table.get_column_count()):
            table.removeColumn(table.columnCount())

    # get Attributes which should be deleted and added
    delete_attributes = existing_attributes.difference(
        set(property_set.get_attributes(filter=True))
    )
    new_attributes = set(property_set.get_attributes(filter=True)).difference(
        existing_attributes
    )
    attribute_table.remove_attributes_from_table(delete_attributes, table)
    attribute_table.add_attributes_to_table(new_attributes, table)

    # update rows
    for row in range(table.rowCount()):
        attribute_table.update_row(table, row)
