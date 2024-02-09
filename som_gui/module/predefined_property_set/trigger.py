from __future__ import annotations
from som_gui.core import predefined_property_set as core
from som_gui.core import property_set as property_set_core
from som_gui import tool
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import PredefinedPropertySetWindow


def connect():
    tool.MainWindow.add_action("Vordefinierte Psets/Anzeigen",
                               lambda: core.create_window(tool.PredefinedPropertySet))


def connect_dialog(dialog: PredefinedPropertySetWindow):
    dialog.widget.list_view_pset.itemSelectionChanged.connect(
        lambda: core.predef_selection_changed(tool.PredefinedPropertySet))
    dialog.widget.list_view_existance.itemDoubleClicked.connect(
        lambda: core.predef_object_double_clicked(tool.PredefinedPropertySet, tool.PropertySet, tool.Object))
    dialog.widget.list_view_pset.customContextMenuRequested.connect(
        lambda pos: core.predefined_pset_window_context_menu(pos, tool.PredefinedPropertySet, tool.PropertySet))
    dialog.widget.list_view_pset.itemChanged.connect(
        lambda item: core.predefined_pset_item_changed(item, tool.PropertySet))
    dialog.widget.list_view_pset.itemDoubleClicked.connect(
        lambda item: core.pset_item_double_clicked(item, tool.PropertySet, tool.PropertySetWindow))

    dialog.edit_started.connect(lambda: core.predef_edit_started(tool.PredefinedPropertySet))
    dialog.edit_stopped.connect(lambda: core.predef_edit_stopped(tool.PredefinedPropertySet))


def edit_name(text, index):
    property_set_core.rename_pset_by_editor(text, index, tool.PropertySet)


def on_new_project():
    pass


def repaint_window():
    core.repaint_predefined_pset_window(tool.PredefinedPropertySet)


def accept():
    core.close_predefined_pset_window(tool.PredefinedPropertySet)
