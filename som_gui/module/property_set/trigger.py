from __future__ import annotations

from typing import TYPE_CHECKING

from som_gui import tool
from som_gui.core import property_set as core

if TYPE_CHECKING:
    from .ui import PsetTableWidget


def connect():
    table: PsetTableWidget = tool.MainWindow.get_property_set_table_widget()
    table.itemSelectionChanged.connect(
        lambda: core.pset_selection_changed(
            tool.PropertySet, tool.PropertyTable, tool.MainWindow
        )
    )
    table.edit_started.connect(lambda: core.pset_table_edit_started(tool.PropertySet))
    table.edit_stopped.connect(lambda: core.pset_table_edit_stopped(tool.PropertySet))
    tool.MainWindow.get_ui().button_Pset_add.clicked.connect(
        lambda: core.add_property_set_button_pressed(
            tool.MainWindow,
            tool.PropertySet,
            tool.Popups,
            tool.PredefinedPropertySet,
            tool.Util
        )
    )
    table.itemClicked.connect(lambda item: core.pset_clicked(item, tool.PropertySet))


def edit_name(text, index):
    core.rename_pset_by_editor(text, index, tool.PropertySet)


def on_new_project():
    pass


def repaint_event():
    core.repaint_pset_table(tool.PropertySet, tool.MainWindow)


def pset_table_context_menu_requested(pos):
    core.pset_table_context_menu(pos, tool.PropertySet,tool.Class)


def retranslate_ui():
    pass
