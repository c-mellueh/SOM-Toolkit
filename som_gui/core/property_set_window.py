from __future__ import annotations
from typing import Type, TYPE_CHECKING

import SOMcreator
from PySide6 import QtGui
from PySide6.QtCore import QModelIndex
import som_gui
from som_gui.core import attribute as attribute_core
from SOMcreator.constants.value_constants import RANGE

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set.ui import PropertySetWindow


def context_menu(window, pos, property_set: Type[tool.PropertySet], property_set_window: Type[tool.PropertySetWindow]):
    table = property_set_window.get_table(window)
    active_attribute = property_set_window.get_item_from_pos(table, pos)
    property_set_window.set_active_attribute(active_attribute)
    property_set_window.set_active_window(window)
    if active_attribute.property_set.object.ident_attrib == active_attribute:

        actions = [["Umbenennen", property_set_window.edit_attribute_name], ]
    else:

        actions = [["Umbenennen", property_set_window.edit_attribute_name],
                   ["Löschen", property_set_window.delete], ]
    property_set.create_context_menu(table.mapToGlobal(pos), actions)


def add_attribute_button_clicked(window: PropertySetWindow, property_set: Type[tool.PropertySet],
                                 property_set_window: Type[tool.PropertySetWindow],
                                 attribute: Type[tool.Attribute]):
    pset = property_set_window.get_property_set_from_window(window)
    attribute_name = property_set_window.get_attribute_name(window)

    old_attribute = property_set.get_attribute_by_name(pset, attribute_name)
    attribute_data = property_set_window.get_attribute_data(window)
    if old_attribute is None:
        attribute.create_attribute(pset, attribute_data)
    else:
        attribute.set_attribute_data(old_attribute, attribute_data)


def add_value_button_clicked(window: PropertySetWindow, property_set_tool: Type[tool.PropertySetWindow]):
    value_type = window.widget.combo_type.currentText()
    if value_type == RANGE:
        property_set_tool.add_value_line(2, window)
    else:
        property_set_tool.add_value_line(1, window)


def close_pset_window(window: PropertySetWindow, property_set_tool: Type[tool.PropertySetWindow]):
    property_set_tool.close_property_set_window(window)
