from __future__ import annotations

from typing import TYPE_CHECKING

from som_gui import tool
from som_gui.core import predefined_property_set as core
from som_gui.core import property_set as property_set_core

if TYPE_CHECKING:
    from .ui import PredefinedPropertySetWindow


def connect():
    core.create_main_menu_actions(tool.PredefinedPropertySet, tool.MainWindow)
    core.add_compare_widget(
        tool.PredefinedPropertySetCompare, tool.PropertyCompare, tool.CompareWindow
    )


def open_window():
    core.open_window(tool.PredefinedPropertySet, tool.Util)


def connect_dialog(dialog: PredefinedPropertySetWindow):
    dialog.ui.list_view_pset.itemSelectionChanged.connect(
        lambda: core.pset_selection_changed(tool.PredefinedPropertySet)
    )

    dialog.ui.table_widgets_classes.itemDoubleClicked.connect(
        lambda: core.class_double_clicked(
            tool.PredefinedPropertySet, tool.PropertySet, tool.ClassTree,tool.MainWindow
        )
    )

    dialog.ui.list_view_pset.customContextMenuRequested.connect(
        lambda pos: core.pset_context_menu(
            pos, tool.PredefinedPropertySet, tool.PropertySet
        )
    )

    dialog.ui.list_view_pset.itemChanged.connect(
        lambda item: core.pset_data_changed(item, tool.PropertySet)
    )

    dialog.ui.list_view_pset.itemDoubleClicked.connect(
        lambda item: core.pset_double_clicked(
            item, tool.PropertySet, tool.PropertySetWindow, tool.PropertyTable
        )
    )

    dialog.ui.table_widgets_classes.customContextMenuRequested.connect(
        lambda pos: core.class_context_menu(
            pos, tool.PredefinedPropertySet, tool.PropertySet
        )
    )

    dialog.edit_started.connect(
        lambda: core.name_edit_started(tool.PredefinedPropertySet)
    )

    dialog.edit_stopped.connect(
        lambda: core.name_edit_stopped(tool.PredefinedPropertySet)
    )


def edit_name(text, index):
    property_set_core.rename_pset_by_editor(text, index, tool.PropertySet)


def on_new_project():
    pass


def repaint_window():
    core.repaint_window(tool.PredefinedPropertySet)


def accept():
    core.close_window(tool.PredefinedPropertySet)


def retranslate_ui():
    core.retranslate_ui(tool.PredefinedPropertySet, tool.Util)
