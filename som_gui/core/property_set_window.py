from __future__ import annotations

from typing import TYPE_CHECKING, Type
import logging
import SOMcreator
from SOMcreator.constants.value_constants import RANGE
from som_gui.core import property_table as attribute_table_core
from som_gui.module.property_set_window.constants import (
    SEPERATOR,
    SEPERATOR_SECTION,
    SEPERATOR_STATUS,
)
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window import ui
    from PySide6.QtWidgets import QTableWidgetItem


def retranslate_ui(property_set_window: Type[tool.PropertySetWindow]):
    for (
        window,
        pset,
    ) in property_set_window.get_properties().property_set_windows.items():
        window.ui.retranslateUi(window)
        property_set_window.fill_window_title(window, pset)


def inherit_checkbox_toggled(
    window: ui.PropertySetWindow, property_set_window: Type[tool.PropertySetWindow]
):
    state = property_set_window.get_inherit_checkbox_state(window)
    active_attribute = property_set_window.get_active_attribute(window)
    if active_attribute:
        active_attribute.child_inherits_values = state


def add_attribute_button_clicked(
    window: ui.PropertySetWindow,
    property_set: Type[tool.PropertySet],
    property_set_window: Type[tool.PropertySetWindow],
    attribute: Type[tool.Property],
):
    pset = property_set_window.get_property_set_by_window(window)
    attribute_name = property_set_window.get_attribute_name_input(window)

    old_attribute = property_set.get_attribute_by_name(pset, attribute_name)
    attribute_data = property_set_window.get_attribute_data(window)
    if old_attribute is None:
        new_attribute = attribute.create_attribute_by_dict(attribute_data)
        new_attribute.property_set = pset
    else:
        attribute.set_attribute_data_by_dict(old_attribute, attribute_data)
    property_set_window.clear_values(window)


def add_value_button_clicked(
    window: ui.PropertySetWindow, property_set_tool: Type[tool.PropertySetWindow]
):
    value_type = window.ui.combo_value_type.currentText()
    if value_type == RANGE:
        property_set_tool.add_value_line(2, window)
    else:
        property_set_tool.add_value_line(1, window)
    property_set_tool.update_line_validators(window)


def open_pset_window(
    property_set: SOMcreator.SOMPropertySet,
    property_set_window: Type[tool.PropertySetWindow],
    attribute_table: Type[tool.AttributeTable],
):
    existing_window = property_set_window.get_window_by_property_set(property_set)
    if existing_window is not None:
        property_set_window.bring_window_to_front(existing_window)
        return existing_window

    window = property_set_window.create_window(property_set)
    property_set_window.fill_window_ui(window)
    property_set_window.connect_window_triggers(window)
    property_set_window.fill_window_title(window, property_set)
    table = property_set_window.get_table(window)
    attribute_table.set_property_set_of_table(table, property_set)
    attribute_table_core.update_attribute_table(table, attribute_table)
    table.resizeColumnsToContents()
    property_set_window.update_datatype_completer(window)
    property_set_window.update_valuetype_completer(window)
    property_set_window.update_unit_completer(window)

    window.show()
    return window


def close_pset_window(
    window: ui.PropertySetWindow, property_set_tool: Type[tool.PropertySetWindow]
):
    property_set_tool.close_property_set_window(window)


def handle_paste_event(
    window: ui.PropertySetWindow, property_set_window: Type[tool.PropertySetWindow]
) -> bool:
    text_list = property_set_window.get_paste_text_list()
    if text_list is True:
        return text_list
    if len(text_list) < 2:
        return True

    existing_input_lines = property_set_window.get_input_value_lines(window)
    lines_to_create = max(len(text_list) - len(existing_input_lines), -1)
    column_count = property_set_window.get_required_column_count(window)

    for i in range(lines_to_create + 1):
        property_set_window.add_value_line(column_count, window)

    for text, lines in zip(
        text_list, property_set_window.get_input_value_lines(window)
    ):
        lines[0].setText(text.strip())
    return False


def repaint_pset_window(
    window: ui.PropertySetWindow,
    property_set_window: Type[tool.PropertySetWindow],
    attribute_table: Type[tool.AttributeTable],
):
    table = property_set_window.get_table(window)
    attribute_table_core.update_attribute_table(table, attribute_table)

    property_set_window.update_add_button(window)
    property_set_window.update_line_validators(window)


def value_type_changed(
    window: ui.PropertySetWindow, property_set_window: Type[tool.PropertySetWindow]
):
    value_type = property_set_window.get_value_type(window)
    if value_type == RANGE:
        property_set_window.set_value_columns(2, window)
        property_set_window.restrict_data_type_to_numbers(window)
    else:
        property_set_window.set_value_columns(1, window)
        property_set_window.remove_data_type_restriction(window)


def attribute_clicked(
    item: QTableWidgetItem,
    attribute_table: Type[tool.AttributeTable],
    property_set_window: Type[tool.PropertySetWindow],
):
    active_attribute = attribute_table.get_property_from_item(item)
    window = item.tableWidget().window()
    activate_property(active_attribute, window, property_set_window)


def activate_property(
    active_attribute: SOMcreator.SOMProperty,
    window,
    property_set_window: Type[tool.PropertySetWindow],
):
    property_set_window.set_attribute_name(active_attribute.name, window)
    property_set_window.set_data_type(active_attribute.data_type, window)
    property_set_window.set_value_type(active_attribute.value_type, window)
    property_set_window.set_description(active_attribute.description, window)
    property_set_window.toggle_comboboxes(active_attribute, window)
    property_set_window.set_inherit_checkbox_state(
        active_attribute.child_inherits_values, window
    )
    property_set_window.set_unit(active_attribute.unit, window)

    property_set_window.clear_values(window)
    property_set_window.set_values(active_attribute, window)
    if not active_attribute.allowed_values:
        if active_attribute.value_type == RANGE:
            property_set_window.add_value_line(2, window)
        else:
            property_set_window.add_value_line(1, window)


#### Settings Window


def fill_splitter_settings(
    widget: ui.SplitterSettings,
    property_set_window: Type[tool.PropertySetWindow],
    appdata: Type[tool.Appdata],
):
    property_set_window.set_splitter_settings_widget(widget)
    seperator = appdata.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")
    is_sperator_activated = appdata.get_bool_setting(
        SEPERATOR_SECTION, SEPERATOR_STATUS
    )

    widget.ui.line_edit_seperator.setText(seperator)
    widget.ui.check_box_seperator.setChecked(is_sperator_activated)
    property_set_window.connect_splitter_widget(widget)
    update_splitter_enabled_state(widget, property_set_window)
    pass


def splitter_settings_accepted(
    property_set_window: Type[tool.PropertySetWindow], appdata: Type[tool.Appdata]
):
    widget = property_set_window.get_splitter_settings_widget()
    is_seperator_activated = property_set_window.get_splitter_settings_checkstate(
        widget
    )
    text = property_set_window.get_splitter_settings_text(widget)
    appdata.set_setting(SEPERATOR_SECTION, SEPERATOR, text)
    appdata.set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, is_seperator_activated)


def update_splitter_enabled_state(
    widget: ui.SplitterSettings,
    property_set_window: Type[tool.PropertySetWindow],
):
    is_seperator_activated = property_set_window.get_splitter_settings_checkstate(
        widget
    )
    widget.ui.line_edit_seperator.setEnabled(is_seperator_activated)
