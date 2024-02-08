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
    from PySide6.QtWidgets import QTableWidget





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


def open_pset_window(property_set: SOMcreator.PropertySet, property_set_window: Type[tool.PropertySetWindow]):
    existing_window = property_set_window.get_window_by_property_set(property_set)
    if existing_window is not None:
        property_set_window.bring_window_to_front(existing_window)
        return existing_window

    window = property_set_window.create_window(property_set)
    property_set_window.fill_window_ui(window)
    property_set_window.connect_window_triggers(window)

    table = property_set_window.get_table(window)
    # paint_attribute_table(table, property_set_window) TODO: Muss imported werden
    table.resizeColumnsToContents()
    return window


def close_pset_window(window: PropertySetWindow, property_set_tool: Type[tool.PropertySetWindow]):
    property_set_tool.close_property_set_window(window)


def handle_paste_event(window: PropertySetWindow, property_set_window: Type[tool.PropertySetWindow]) -> bool:
    text_list = property_set_window.get_paste_text_list()
    if len(text_list) < 2:
        return True

    existing_input_lines = property_set_window.get_input_value_lines(window)
    lines_to_create = max(len(text_list) - len(existing_input_lines), -1)
    column_count = property_set_window.get_required_column_count(window)

    for i in range(lines_to_create + 1):
        property_set_window.add_value_line(column_count, window)

    for text, lines in zip(text_list, property_set_window.get_input_value_lines(window)):
        lines[0].setText(text.strip())
    return False
