from __future__ import annotations
from som_gui.core import property_set_window as core
from som_gui import tool
from typing import TYPE_CHECKING
from PySide6 import QtGui

if TYPE_CHECKING:
    from .ui import PropertySetWindow


def connect():
    pass


def on_new_project():
    pass


def connect_window(window: PropertySetWindow):
    window.widget.button_add_line.clicked.connect(lambda: core.add_value_button_clicked(window, tool.PropertySet))
    window.widget.button_add.clicked.connect(
        lambda: core.add_attribute_button_clicked(window, tool.PropertySet, tool.Attribute))

    window.widget.table_widget.customContextMenuRequested.connect(
        lambda pos: core.pset_window_context_menu(window, pos, tool.PropertySet, tool.Attribute))
    window.widget.combo_type.currentIndexChanged.connect(lambda: core.value_type_changed(window, tool.PropertySet))
    window.widget.line_edit_seperator.textChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySet, tool.Settings))
    window.widget.check_box_seperator.stateChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySet, tool.Settings))


def repaint_window(widget: PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySet, tool.Attribute)


def close_window(window: PropertySetWindow):
    core.close_pset_window(window, tool.PropertySet)


def key_press_event(event, window: PropertySetWindow):
    sep_bool = tool.Settings.get_seperator_status()
    if not event.matches(QtGui.QKeySequence.StandardKey.Paste) and sep_bool:
        return True
    return core.handle_paste_event(window, tool.PropertySet, tool.Settings)
