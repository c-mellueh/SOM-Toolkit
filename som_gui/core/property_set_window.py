from __future__ import annotations
from typing import Type, TYPE_CHECKING

import SOMcreator
from som_gui.core import attribute_table as attribute_table_core
from SOMcreator.constants.value_constants import RANGE

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window.ui import PropertySetWindow
    from PySide6.QtWidgets import QTableWidgetItem


def add_attribute_button_clicked(window: PropertySetWindow, property_set: Type[tool.PropertySet],
                                 property_set_window: Type[tool.PropertySetWindow],
                                 attribute: Type[tool.Attribute]):
    pset = property_set_window.get_property_set_by_window(window)
    attribute_name = property_set_window.get_attribute_name_input(window)

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
    property_set_tool.update_line_validators(window)

def open_pset_window(property_set: SOMcreator.PropertySet, property_set_window: Type[tool.PropertySetWindow]):
    existing_window = property_set_window.get_window_by_property_set(property_set)
    if existing_window is not None:
        property_set_window.bring_window_to_front(existing_window)
        return existing_window

    window = property_set_window.create_window(property_set)
    property_set_window.fill_window_ui(window)
    property_set_window.connect_window_triggers(window)
    property_set_window.fill_window_title(window, property_set)
    table = property_set_window.get_table(window)
    # paint_attribute_table(table, property_set_window) TODO: Muss imported werden
    table.resizeColumnsToContents()
    window.show()
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


def repaint_pset_window(window: PropertySetWindow, property_set_window: Type[tool.PropertySetWindow],
                        attribute_table: Type[tool.AttributeTable]):
    table = property_set_window.get_table(window)
    attribute_table_core.paint_attribute_table(table, attribute_table)

    property_set_window.update_add_button(window)
    property_set_window.update_line_validators(window)
    property_set_window.set_seperator(window)


def value_type_changed(window: PropertySetWindow, property_set_window: Type[tool.PropertySetWindow]):
    value_type = property_set_window.get_value_type(window)
    if value_type == RANGE:
        property_set_window.set_value_columns(2, window)
        property_set_window.restrict_data_type_to_numbers(window)
    else:
        property_set_window.set_value_columns(1, window)
        property_set_window.remove_data_type_restriction(window)


def update_seperator(window: PropertySetWindow, property_set_window: Type[tool.PropertySetWindow],
                     settings: Type[tool.Settings]):
    text, state = property_set_window.get_seperator_state(window)
    settings.set_seperator_status(state)
    settings.set_seperator(text)


def attribute_clicked(item: QTableWidgetItem, attribute: Type[tool.Attribute],
                      attribute_table: Type[tool.AttributeTable], property_set_window: Type[tool.PropertySetWindow]):
    active_attribute = attribute_table.get_attribute_from_item(item)
    attribute_table.set_active_attribute(active_attribute)
    window = item.tableWidget().window()
    activate_attribute(active_attribute, window, attribute, property_set_window)


def activate_attribute(active_attribute: SOMcreator.Attribute, window, attribute: Type[tool.Attribute],
                       property_set_window: Type[tool.PropertySetWindow]):
    name = attribute.get_attribute_name(active_attribute)
    data_type = attribute.get_attribute_data_type(active_attribute)
    value_type = attribute.get_attribute_value_type(active_attribute)
    values = attribute.get_attribute_values(active_attribute)
    description = attribute.get_attribute_description(active_attribute)

    property_set_window.set_attribute_name(name, window)
    property_set_window.set_data_type(data_type, window)
    property_set_window.set_value_type(value_type, window)
    property_set_window.set_description(description, window)
    property_set_window.toggle_comboboxes(active_attribute, window)

    property_set_window.clear_values(window)
    property_set_window.set_values(values, window)
    if not values:
        if value_type == RANGE:
            property_set_window.add_value_line(2, window)
        else:
            property_set_window.add_value_line(1, window)
