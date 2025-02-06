from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.core import connection as core
from som_gui import tool
if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.connection import ui as ui_connection
    from som_gui.plugins.aggregation_window.module.node import ui as ui_node

def connect():
    pass


def on_new_project():
    pass


def paint_connection(connection:ui_connection.Connection):
    core.paint_connection(connection, aw_tool.Connection,aw_tool.View)

def retranslate_ui():
    pass
