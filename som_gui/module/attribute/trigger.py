from __future__ import annotations
from som_gui.core import attribute as core
from som_gui import tool
import som_gui
from PySide6.QtWidgets import QTableWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.property_set.ui import PropertySetWindow

def connect():
    core.add_basic_attribute_columns(tool.Attribute)


def on_new_project():
    core.setup_table_header(som_gui.MainUi.ui.table_attribute, tool.Attribute)


def table_paint_event(table: QTableWidget):
    core.refresh_attribute_table(table, tool.Attribute)


def connect_attribute_table(table: QTableWidget):
    table.itemClicked.connect(lambda item: core.attribute_clicked(item, tool.Attribute, tool.PropertySet))
