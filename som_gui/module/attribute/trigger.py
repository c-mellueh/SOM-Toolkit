from som_gui.core import attribute as core
from som_gui import tool
import som_gui
from PySide6.QtWidgets import QTableWidget


def connect():
    core.add_basic_attribute_columns(tool.Attribute)


def on_new_project():
    core.setup_table_header(som_gui.MainUi.ui.table_attribute, tool.Attribute)


def table_paint_event(table: QTableWidget):
    core.refresh_attribute_table(table, tool.Attribute)
