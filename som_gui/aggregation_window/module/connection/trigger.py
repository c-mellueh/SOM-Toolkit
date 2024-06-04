from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget
from som_gui.aggregation_window.core import connection as core
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool
from PySide6.QtGui import QPainter

if TYPE_CHECKING:
    from . import ui


def connect():
    pass


def on_new_project():
    pass


def paint_connection(connection):
    core.paint_connection(connection, aw_tool.Connection)
