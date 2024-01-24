from __future__ import annotations
import som_gui
from som_gui.core import property_set as core
from som_gui import tool
from typing import TYPE_CHECKING
from PySide6 import QtGui

if TYPE_CHECKING:
    from .ui import PropertySetWindow, PredefinedPropertySetWindow


def connect():
    table = som_gui.MainUi.ui.table_pset
    table.itemSelectionChanged.connect(lambda: core.pset_selection_changed(tool.PropertySet, tool.Attribute))
    table.itemDoubleClicked.connect(lambda: core.table_double_clicked(tool.PropertySet, tool.Attribute))
    tool.MainWindow.get_ui().button_Pset_add.clicked.connect(
        lambda: core.add_property_set_button_pressed(tool.Object, tool.MainWindow, tool.PropertySet, tool.Popups))
    tool.MainWindow.add_action("Vordefinierte Psets/Anzeigen",
                               lambda: core.create_predefined_pset_window(tool.Attribute, tool.PropertySet,
                                                                          tool.Object))

def connect_property_set_window(window: PropertySetWindow):
    window.widget.button_add_line.clicked.connect(lambda: core.add_value_button_clicked(window, tool.PropertySet))
    window.widget.button_add.clicked.connect(
        lambda: core.add_attribute_button_clicked(window, tool.PropertySet, tool.Attribute))

    window.widget.combo_type.currentIndexChanged.connect(lambda: core.value_type_changed(window, tool.PropertySet))
    window.widget.line_edit_seperator.textChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySet, tool.Settings))
    window.widget.check_box_seperator.stateChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySet, tool.Settings))


def repaint_pset_window(widget: PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySet, tool.Attribute)


def predefined_pset_window_accept():
    tool.PropertySet.close_predefined_pset_window()


def repaint_predefined_pset_window():
    core.repaint_predefined_pset_window(tool.PropertySet)

def close_pset_window(window: PropertySetWindow):
    core.close_pset_window(window, tool.PropertySet)


def on_new_project():
    pass


def repaint_event():
    core.refresh_table(tool.PropertySet, tool.Object)


def key_press_event(event, window: PropertySetWindow):
    sep_bool = tool.Settings.get_seperator_status()
    if not event.matches(QtGui.QKeySequence.StandardKey.Paste) and sep_bool:
        return True
    return core.handle_paste_event(window, tool.PropertySet, tool.Settings)
