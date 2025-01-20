from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from som_gui import tool
from som_gui.core import attribute_table as core

if TYPE_CHECKING:
    from .ui import AttributeTable


def connect():
    core.init_attribute_columns(tool.AttributeTable)
    tool.MainWindow.get_attribute_table().itemDoubleClicked.connect(
        lambda item: core.activate_item(item, tool.AttributeTable, tool.PropertySet,
                                        tool.PropertySetWindow))
    core.init_context_menu(tool.AttributeTable)


def retranslate_ui():
    pass


def connect_table(table: AttributeTable):
    table.customContextMenuRequested.connect(
        lambda pos: core.create_context_menu(table, pos, tool.AttributeTable, tool.Util))
    table.itemClicked.connect(lambda item: core.toggle_optionality(item, tool.AttributeTable))


def drop_event(event, table):
    core.drop_event(event, table, tool.AttributeTable, tool.Attribute)


def create_mime_data(items: list[QTableWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.AttributeTable)


def on_new_project():
    core.setup_table_header(tool.MainWindow, tool.AttributeTable)


def table_paint_event(table: QTableWidget):
    core.update_attribute_table(table, tool.AttributeTable)
