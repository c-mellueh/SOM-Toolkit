from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import filter_window as core
from typing import TYPE_CHECKING


def connect():
    tool.MainWindow.add_action("Filter",
                               lambda: core.open(tool.FilterWindow))


def pt_horizontal_context_requested():
    # was uc_context_menu_requested
    pass


def pt_vertical_context_requested():
    # was pp_context_menu_requested
    pass


def pt_item_clicked():
    # was itemChanged
    pass
def on_new_project():
    pass


def pt_update():
    core.update_project_table(tool.FilterWindow)
