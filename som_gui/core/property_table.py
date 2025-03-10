from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData, Qt

import SOMcreator
from som_gui.core import property_set_window as property_set_window_core
from som_gui.module.property_table.constants import MIME_DATA_KEY

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
) -> QMimeData:
    """
    create MimeData used for Dropping Properties into different Tables
    """
    objects = {property_table.get_property_from_item(item) for item in items}
    mime_data.setProperty(MIME_DATA_KEY, objects)
    return mime_data


def drop_event(
    event: QDropEvent,
    target_table: ui.PropertyTable,
    property_table: Type[tool.PropertyTable],
    property_tool: Type[tool.Property],
):
    """
    handling of dropping of property row from a property set window to another property set window
    :param target_table: table on which the property is dropped on
    :return:
    """

    # Check if move is inside the same window
    source_table: ui.PropertyTable = event.source()  # type: ignore
    if source_table == target_table:
        event.accept()
        return

    proposed_action = event.proposedAction()
    target_property_set = property_table.get_property_set_by_table(target_table)
    existing_properties = {
        a.name: a for a in target_property_set.get_properties(filter=False)
    }
    dropped_properties: set[SOMcreator.SOMProperty] = event.mimeData().property(
        MIME_DATA_KEY
    )  # get set of dropped Properties

    if proposed_action == Qt.DropAction.CopyAction:
        for som_property in dropped_properties:
            # check if Property with same name exists already
            existing_property = existing_properties.get(som_property.name)
            if existing_property:
                # overwrite date
                data = property_tool.get_property_data(som_property)
                property_tool.set_data_by_dict(existing_property, data)
            else:
                # copy property to property_set
                som_property = copy.copy(som_property)
                som_property.remove_parent()
                target_property_set.add_property(som_property)

    elif proposed_action == Qt.DropAction.MoveAction:
        for som_property in dropped_properties:
            # check if Property with same name exists already
            existing_property = existing_properties.get(som_property.name)
            if existing_property:
                # replace Property
                target_property_set.remove_property(existing_property)
            target_property_set.add_property(som_property)
            som_property.remove_parent()  # remove ParentProperty
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
    window = property_set_window_core.open_pset_window(
        active_property_set, property_set_window, property_table
    )
    property_set_window_core.activate_property(
        active_property, window, property_set_window
    )


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
