from __future__ import annotations
from som_gui.core import attribute_table as core
from som_gui import tool
import som_gui
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import AttributeTable


def connect():
    core.add_basic_attribute_columns(tool.Attribute, tool.AttributeTable)
    tool.MainWindow.get_attribute_table().itemDoubleClicked.connect(
        lambda item: core.attribute_double_clicked(item, tool.Attribute, tool.AttributeTable, tool.PropertySet,
                                                   tool.PropertySetWindow))


def connect_table(table: AttributeTable):
    table.customContextMenuRequested.connect(
        lambda pos: core.context_menu(table, pos, tool.PropertySet, tool.AttributeTable))
    table.itemClicked.connect(lambda item: core.item_changed(item, tool.AttributeTable))

def drop_event(event, table):
    core.drop_event(event, table, tool.PropertySetWindow, tool.Attribute)


def create_mime_data(items: list[QTableWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.AttributeTable)


def on_new_project():
    core.setup_table_header(tool.MainWindow, tool.AttributeTable)


def table_paint_event(table: QTableWidget):
    core.paint_attribute_table(table, tool.AttributeTable)
