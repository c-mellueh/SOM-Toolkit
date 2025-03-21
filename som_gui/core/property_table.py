from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData, Qt, QByteArray
from PySide6.QtWidgets import QApplication
import SOMcreator
import pickle

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
    from PySide6.QtGui import QDropEvent
    from som_gui.module.property_table import ui
    from som_gui.module.property_set_window.ui import PropertySetWindow


def init_context_menu(property_table: Type[tool.PropertyTable]):
    """
    Defines all standard context menu actions associated with an property table.
    """
    property_table.add_context_menu_builder(property_table.context_menu_builder_rename)
    property_table.add_context_menu_builder(
        lambda t: property_table.context_menu_builder_delete(t, False)
    )
    property_table.add_context_menu_builder(
        lambda t: property_table.context_menu_builder_delete(t, True)
    )
    property_table.add_context_menu_builder(
        property_table.context_menu_builder_remove_connection
    )
    property_table.add_context_menu_builder(
        property_table.context_menu_builder_add_connection
    )


def init_property_columns(property_table: Type[tool.PropertyTable]):
    """
    Defines all property columns associated with an property table. This can be expanded by plugins
    :param property_table:
    :return:
    """
    logging.info("Add Basic Property Columns")
    # write translations so Qtlinguist knows them
    name = QCoreApplication.translate("PropertyTable", "Name")
    datatype = QCoreApplication.translate("PropertyTable", "Datatype")
    valuetype = QCoreApplication.translate("PropertyTable", "Valuetype")
    value = QCoreApplication.translate("PropertyTable", "Value")
    optional = QCoreApplication.translate("PropertyTable", "Optional")
    unit = QCoreApplication.translate("PropertyTable", "Unit")

    property_table.add_column_to_table("Name", lambda a: a.name)
    property_table.add_column_to_table("Datatype", lambda a: a.data_type)
    property_table.add_column_to_table("Valuetype", lambda a: a.value_type)
    property_table.add_column_to_table("Unit", lambda a: a.unit)
    property_table.add_column_to_table("Value", lambda a: a.allowed_values)
    property_table.add_column_to_table(
        "Optional", lambda a: a.is_optional(ignore_hirarchy=True)
    )


def retranslate_ui(
    table: ui.PropertyTable,
    property_table: Type[tool.PropertyTable],
    main_window: Type[tool.MainWindow],
):
    if table is None:
        table = main_window.get_property_table()
    labels = property_table.get_header_labels()
    table.setHorizontalHeaderLabels(labels)


def toggle_optionality(
    item: QTableWidgetItem, property_table: Type[tool.PropertyTable]
):
    """
    change the optionality of an property by their QTableWidgetItem
    :param item:
    :param property_table:
    :return:
    """
    som_property = property_table.get_property_from_item(item)
    if not som_property:
        return
    if not item.column() == 4:
        return
    cs = True if item.checkState() == Qt.CheckState.Checked else False
    som_property.set_optional(cs)


def create_mime_data(
    items: list[QTableWidgetItem],
    mime_data: QMimeData,
    property_table: Type[tool.PropertyTable],
    property_tool: Type[tool.Property],
) -> QMimeData:
    """
    create MimeData used for Dropping Properties into different Tables
    """
    properties = {property_table.get_property_from_item(item) for item in items}
    if not properties:
        return mime_data
    property_dicts = [property_tool.get_property_data(p) for p in properties]
    property_table.write_property_dicts_to_mime_data(property_dicts, mime_data)
    return mime_data


def drop_event(
    event: QDropEvent,
    target_table: ui.PropertyTable,
    property_table: Type[tool.PropertyTable],
    property_tool: Type[tool.Property],
    property_set: Type[tool.PropertySet],
):
    """
    handling of dropping of property row from a property set window to another property set window
    :param target_table: table on which the property is dropped on
    :return:
    """

    # Check if move is allowed
    if not property_table.is_drop_allowed(event, target_table):
        return

    source_property_set = property_table.get_property_set_by_table(event.source())
    target_property_set = property_table.get_property_set_by_table(target_table)
    property_dicts = property_table.get_property_dict_from_mime_data(event.mimeData())

    for property_dict in property_dicts:
        # check if Property with same name exists already
        property_name = property_dict.get("name")
        existing_property = property_set.get_property_by_name(
            target_property_set, property_name
        )
        if existing_property:
            # overwrite data
            property_tool.set_data_by_dict(existing_property, property_dict)
        else:
            # copy property to property_set
            new_property = property_tool.create_by_dict(property_dict)
            target_property_set.add_property(new_property)
        if event.proposedAction() == Qt.DropAction.MoveAction:
            property_set.remove_property_by_name(source_property_set, property_name)
    target_table.repaint()
    event.accept()


def create_context_menu(
    table: ui.PropertyTable,
    pos,
    property_table: Type[tool.PropertyTable],
    util: Type[tool.Util],
):
    """
    Create Context Menu based on context menu builders
    """

    # see tool.PropertyTable.add_context_menu_builder

    menu_list = list()

    # Create list of context menu entries
    for context_menu_builder in property_table.get_context_menu_builders():
        result = context_menu_builder(table)
        if result is not None:
            menu_list.append(result)

    menu = util.create_context_menu(menu_list)
    # Run Context Menu
    menu.exec(table.viewport().mapToGlobal(pos))


def activate_item(
    item: QTableWidgetItem,
    property_table: Type[tool.PropertyTable],
    property_set: Type[tool.PropertySet],
    property_set_window: Type[tool.PropertySetWindow],
):
    """
    Activate Property based on QTableWidgetItem
    :return:
    """
    active_property = property_table.get_property_from_item(item)
    if not active_property:
        return
    active_property_set = property_set.get_active_property_set()
    # create Window or activate it
    property_set_window.trigger_window_open(active_property_set)
    window = property_set_window.get_window_by_property_set(active_property_set)
    property_set_window.trigger_property_activation(active_property, window)


def update_table(table: QTableWidget, property_table: Type[tool.PropertyTable]):
    logging.debug(f"Repaint Property Table")

    existing_properties = property_table.get_existing_properties(table)
    property_set = property_table.get_property_set_by_table(table)
    if property_set is None:
        # clear Table
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)
        return

    if property_table.get_column_count() > table.columnCount():
        for _ in range(property_table.get_column_count() - table.columnCount()):
            table.insertColumn(table.columnCount())
    if property_table.get_column_count() < table.columnCount():
        for _ in range(table.columnCount() - property_table.get_column_count()):
            table.removeColumn(table.columnCount())

    # get Properties which should be deleted and added
    delete_properties = existing_properties.difference(
        set(property_set.get_properties(filter=True))
    )
    new_properties = set(property_set.get_properties(filter=True)).difference(
        existing_properties
    )
    property_table.remove_properties_from_table(delete_properties, table)
    property_table.add_properties_to_table(new_properties, table)

    # update rows
    for row in range(table.rowCount()):
        property_table.update_row(table, row)
