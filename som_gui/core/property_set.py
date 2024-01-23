from __future__ import annotations
from typing import Type, TYPE_CHECKING

import SOMcreator
from PySide6 import QtGui
import som_gui
from som_gui.core import attribute as attribute_core
from som_gui.core import property_set as property_set_core
from SOMcreator.constants.value_constants import RANGE

if TYPE_CHECKING:
    from som_gui.tool import PropertySet, Object, Attribute, Settings, MainWindow, Popups
    from som_gui.module.property_set.ui import PropertySetWindow


def refresh_table(property_set_tool: Type[PropertySet], object_tool: Type[Object]):
    if object_tool.get_active_object() is not None:
        property_set_tool.set_enabled(True)
    else:
        property_set_tool.set_enabled(False)
    new_property_sets = property_set_tool.get_property_sets()
    table = property_set_tool.get_table()

    existing_property_sets = property_set_tool.get_existing_psets_in_table(table)
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets, table)
    property_set_tool.add_property_sets_to_table(add_property_sets, table)


def pset_selection_changed(property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_selecte_property_set()
    property_set_tool.set_active_property_set(property_set)
    attribute_core.refresh_attribute_table(som_gui.MainUi.ui.table_attribute, attribute_tool)


def table_double_clicked(property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_selecte_property_set()
    window = property_set_tool.open_pset_window(property_set)
    table = attribute_tool.get_table(window)
    attribute_core.refresh_attribute_table(table, attribute_tool)
    table.resizeColumnsToContents()
    pass


def open_pset_window(property_set: SOMcreator.PropertySet, property_set_tool: Type[PropertySet],
                     attribute_tool: Type[Attribute]):
    window = property_set_tool.open_pset_window(property_set)
    table = attribute_tool.get_table(window)
    attribute_core.refresh_attribute_table(table, attribute_tool)
    table.resizeColumnsToContents()
    return window


def repaint_pset_window(window: PropertySetWindow, property_set_tool: Type[PropertySet],
                        attribute_tool: Type[Attribute]):
    pset = property_set_tool.get_property_set_from_window(window)
    attribute_core.refresh_attribute_table(window.widget.table_widget, attribute_tool)
    attribute_name = property_set_tool.pw_get_attribute_name(window)
    if attribute_name in [a.name for a in pset.attributes]:
        property_set_tool.pw_set_add_button_text("Update", window)
    else:
        property_set_tool.pw_set_add_button_text("Hinzufügen", window)
    property_set_tool.update_line_validators(window)
    property_set_tool.pw_set_seperator(window)


def add_value_button_clicked(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    value_type = window.widget.combo_type.currentText()
    if value_type == RANGE:
        property_set_tool.pw_add_value_line(2, window)
    else:
        property_set_tool.pw_add_value_line(1, window)


def add_attribute_button_clicked(window: PropertySetWindow, property_set_tool: Type[PropertySet],
                                 attribute_tool: Type[Attribute]):
    pset = property_set_tool.get_property_set_from_window(window)
    attribute_name = property_set_tool.pw_get_attribute_name(window)
    attribute_dict = {a.name: a for a in pset.attributes}
    attribute = attribute_dict.get(attribute_name)
    attribute_data = property_set_tool.pw_get_attribute_data(window)
    if attribute is None:
        attribute_tool.create_attribute(pset, attribute_data)
    else:
        attribute_tool.set_attribute_data(attribute, attribute_data)


def value_type_changed(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    value_type = property_set_tool.pw_get_value_type(window)
    if value_type == RANGE:
        property_set_tool.set_value_columns(2, window)
        property_set_tool.restrict_data_type_to_numbers(window)
    else:
        property_set_tool.set_value_columns(1, window)
        property_set_tool.remove_data_type_restriction(window)


def close_pset_window(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    property_set_tool.close_property_set_window(window)


def handle_paste_event(window: PropertySetWindow, property_set_tool: Type[PropertySet], settings_tool: Type[Settings]):
    seperator = settings_tool.get_seperator()
    seperator_status = settings_tool.get_seperator_status()
    if not seperator_status:
        return True
    text = QtGui.QGuiApplication.clipboard().text()
    text_list = text.split(seperator)
    if len(text_list) < 2:
        return True

    dif = len(text_list) - len(property_set_tool.get_input_value_lines(window))
    column_count = 2 if property_set_tool.pw_get_value_type(window) == RANGE else 1
    if dif >= 0:
        for i in range(dif + 1):
            property_set_tool.pw_add_value_line(column_count, window)
    for text, lines in zip(text_list, property_set_tool.get_input_value_lines(window)):
        lines[0].setText(text.strip())
    return False


def update_seperator(window: PropertySetWindow, property_set_tool: Type[PropertySet], settings_tool: Type[Settings]):
    text, state = property_set_tool.get_seperator_state(window)
    settings_tool.set_seperator_status(state)
    settings_tool.set_seperator(text)


def add_property_set_button_pressed(object_tool: Type[Object], main_window_tool: Type[MainWindow],
                                    property_set_tool: Type[PropertySet]):
    obj = object_tool.get_active_object()
    pset_name = main_window_tool.get_pset_name()
    property_set_tool.create_property_set(pset_name, obj)
    refresh_table(property_set_tool, object_tool)
