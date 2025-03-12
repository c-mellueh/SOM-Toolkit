from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from som_gui import tool
from som_gui.core import property_table as core

if TYPE_CHECKING:
    from .ui import PropertyTable


def connect():
    core.init_property_columns(tool.PropertyTable)
    tool.MainWindow.get_property_table().itemDoubleClicked.connect(
        lambda item: core.activate_item(
            item, tool.PropertyTable, tool.PropertySet, tool.PropertySetWindow
        )
    )
    core.init_context_menu(tool.PropertyTable)


def retranslate_ui(table=None):
    core.retranslate_ui(table, tool.PropertyTable, tool.MainWindow)


def connect_table(table: PropertyTable):
    table.customContextMenuRequested.connect(
        lambda pos: core.create_context_menu(table, pos, tool.PropertyTable, tool.Util)
    )
    table.itemClicked.connect(
        lambda item: core.toggle_optionality(item, tool.PropertyTable)
    )


def drop_event(event, table):
    core.drop_event(event, table, tool.PropertyTable, tool.Property,tool.PropertySet)


def create_mime_data(items: list[QTableWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.PropertyTable,tool.Property)


def on_new_project():
    return


def table_paint_event(table: PropertyTable):
    core.update_table(table, tool.PropertyTable)
    core.retranslate_ui(table, tool.PropertyTable, tool.MainWindow)
