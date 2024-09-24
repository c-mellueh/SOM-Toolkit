from __future__ import annotations
from som_gui.core import property_set_window as core
import som_gui
from som_gui import tool
from typing import TYPE_CHECKING
from PySide6 import QtGui
from .constants import SEPERATOR, SEPERATOR_SECTION, SEPERATOR_STATUS
if TYPE_CHECKING:
    from .ui import PropertySetWindow


def connect():
    pass


def on_new_project():
    pass


def connect_window(window: PropertySetWindow):
    window.widget.button_add_line.clicked.connect(lambda: core.add_value_button_clicked(window, tool.PropertySetWindow))
    window.widget.button_add.clicked.connect(
        lambda: core.add_attribute_button_clicked(window, tool.PropertySet, tool.PropertySetWindow, tool.Attribute))
    window.widget.combo_type.currentIndexChanged.connect(
        lambda: core.value_type_changed(window, tool.PropertySetWindow))
    window.widget.line_edit_seperator.textChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySetWindow, tool.Appdata))
    window.widget.check_box_seperator.stateChanged.connect(
        lambda: core.update_seperator(window, tool.PropertySetWindow, tool.Appdata))

    window.widget.check_box_inherit.stateChanged.connect(
        lambda: core.inherit_checkbox_toggled(window, tool.PropertySetWindow, tool.Attribute))

    table = window.widget.table_widget
    table.itemClicked.connect(
        lambda item: core.attribute_clicked(item, tool.Attribute, tool.AttributeTable, tool.PropertySetWindow))


def repaint_window(widget: PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySetWindow, tool.AttributeTable)


def close_window(window: PropertySetWindow):
    core.close_pset_window(window, tool.PropertySetWindow)


def key_press_event(event, window: PropertySetWindow):
    sep_bool = tool.Appdata.cls.get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)
    if not event.matches(QtGui.QKeySequence.StandardKey.Paste) and sep_bool:
        return True
    return core.handle_paste_event(window, tool.PropertySetWindow)

