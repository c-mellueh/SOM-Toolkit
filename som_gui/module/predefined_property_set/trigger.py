from __future__ import annotations

from typing import TYPE_CHECKING

from som_gui import tool
from som_gui.core import predefined_property_set as core
from som_gui.core import property_set as property_set_core
import SOMcreator

if TYPE_CHECKING:
    from .ui import PredefinedPropertySetWindow


def connect():
    core.create_main_menu_actions(tool.PredefinedPropertySet, tool.MainWindow)
    core.add_compare_widget(
        tool.PredefinedPropertySetCompare, tool.PropertyCompare, tool.CompareWindow
    )
    core.connect_signals(tool.PredefinedPropertySet,tool.Property,tool.PropertyTable,tool.PropertyWindow)


def open_window():
    core.open_window(
        tool.PredefinedPropertySet, tool.Util, tool.PropertyTable, tool.PropertyWindow
    )


def set_active_property_set(property_set: SOMcreator.SOMPropertySet):
    core.pset_selection_changed(
        property_set, tool.PredefinedPropertySet, tool.PropertyTable
    )


def activate_linked_property_set(property_set: SOMcreator.SOMPropertySet):
    core.activate_linked_property_set(
        property_set,
        tool.PredefinedPropertySet,
        tool.PropertySet,
        tool.ClassTree,
        tool.MainWindow,
    )


def pset_context_menu_requested(pos):
    core.create_pset_context_menu(pos, tool.PredefinedPropertySet, tool.PropertySet)


def rename_property_set(item):
    core.pset_data_changed(item, tool.PropertySet)


def class_context_menu_requested(pos):
        core.class_context_menu(
            pos, tool.PredefinedPropertySet, tool.PropertySet
        )

def connect_dialog(dialog: PredefinedPropertySetWindow):

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
    core.retranslate_ui(tool.PredefinedPropertySet, tool.Util, tool.PropertyTable)
