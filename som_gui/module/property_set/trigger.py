from __future__ import annotations
import som_gui
from som_gui.core import property_set as core
from som_gui import tool


def connect():
    table = som_gui.MainUi.ui.table_pset
    table.itemSelectionChanged.connect(lambda: core.pset_selection_changed(tool.PropertySet, tool.Attribute))
    table.itemDoubleClicked.connect(lambda: core.table_double_clicked(tool.PropertySet, tool.Attribute))
    table.edit_started.connect(lambda: core.pset_table_edit_started(tool.PropertySet))
    table.edit_stopped.connect(lambda: core.pset_table_edit_stopped(tool.PropertySet))
    tool.MainWindow.get_ui().button_Pset_add.clicked.connect(
        lambda: core.add_property_set_button_pressed(tool.Object, tool.MainWindow, tool.PropertySet, tool.Popups))
    tool.MainWindow.add_action("Vordefinierte Psets/Anzeigen",
                               lambda: core.create_predefined_pset_window(tool.Attribute, tool.PropertySet,
                                                                          tool.Object))


def on_new_project():
    pass


def repaint_event():
    core.repaint_pset_table(tool.PropertySet, tool.Object)


def pset_table_context_menu_requested(pos):
    core.pset_table_context_menu(pos, tool.PropertySet)
