def add_property_set_button_pressed(object_tool: Type[Object], main_window_tool: Type[MainWindow],
                                    property_set_tool: Type[PropertySet], popup_tool: Type[Popups]):
    obj = object_tool.get_active_object()
    pset_name = main_window_tool.get_pset_name()
    if property_set_tool.check_if_pset_allready_exists(pset_name, obj):
        popup_tool.create_warning_popup(f"PropertySet '{pset_name}' existiert bereits")
        return

    predefined_pset_dict = {p.name: p for p in property_set_tool.get_predefined_psets()}
    connect_predefined_pset = False
    if pset_name in predefined_pset_dict:
        connect_predefined_pset = popup_tool.request_property_set_merge(pset_name, 1)
        if connect_predefined_pset is None:
            return

    parent_property_sets = property_set_tool.get_inheritable_property_sets(obj)
    parent_pset_dict = {p.name: p for p in parent_property_sets}
    connect_parent_pset = False
    if pset_name in parent_pset_dict and not connect_predefined_pset:
        connect_parent_pset = popup_tool.request_property_set_merge(pset_name, 2)
        if connect_parent_pset is None:
            return

    if connect_predefined_pset:
        parent = predefined_pset_dict.get(pset_name)
    elif connect_parent_pset:
        parent = parent_pset_dict.get(pset_name)
    else:
        parent = None
    property_set_tool.create_property_set(pset_name, obj, parent)
    repaint_pset_table(property_set_tool, object_tool)


def create_predefined_pset_window(attribute_tool: Type[Attribute], property_set_tool: Type[PropertySet],
                                  object_tool: Type[Object]):
    if not property_set_tool.get_predefined_pset_window():
        dialog = property_set_tool.create_predefined_pset_window()
        dialog.widget.list_view_pset.itemSelectionChanged.connect(lambda: predef_selection_changed(property_set_tool))
        dialog.widget.list_view_existance.itemDoubleClicked.connect(
            lambda: predef_object_double_clicked(property_set_tool, object_tool))
        dialog.widget.list_view_pset.customContextMenuRequested.connect(
            lambda pos: predefined_pset_window_context_menu(pos, property_set_tool))
        dialog.widget.list_view_pset.itemChanged.connect(
            lambda item: predefined_pset_item_changed(item, property_set_tool))
        dialog.widget.list_view_pset.itemDoubleClicked.connect(
            lambda item: pset_item_double_clicked(item, property_set_tool, attribute_tool))
    property_set_tool.get_predefined_pset_window().show()


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


def open_pset_window(property_set: SOMcreator.PropertySet, property_set_tool: Type[PropertySet],
                     attribute_tool: Type[Attribute]):
    window = property_set_tool.open_pset_window(property_set)
    table = attribute_tool.get_table(window)
    attribute_core.refresh_attribute_table(table, attribute_tool)
    table.resizeColumnsToContents()
    return window


def predef_object_double_clicked(property_set_tool: Type[PropertySet], object_tool: Type[Object]):
    item = property_set_tool.get_predefined_pset_inheritance_list().selectedItems()[0]
    property_set = property_set_tool.get_property_set_from_item(item)
    property_set_tool.close_predefined_pset_window()

    obj = property_set.object
    obj_item = object_tool.get_item_from_object(obj)
    object_tool.select_object(obj)
    object_tool.expand_to_item(obj_item)
    property_set_tool.select_property_set(property_set)


def predef_selection_changed(property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_selected_predef_property_set()
    property_set_tool.set_predef_property_set(property_set)
    repaint_predefined_pset_inheritance_list(property_set_tool)


def predefined_pset_item_changed(item, property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_property_set_from_item(item)
    property_set.name = item.text()


def predefined_pset_window_context_menu(pos, property_set_tool: Type[PropertySet]):
    functions = [
        ["Löschen", property_set_tool.delete_predefined_pset],
        ["Umbenennen", property_set_tool.rename_predefined_pset],
        ["Hinzufügen", property_set_tool.add_predefined_pset],
    ]
    list_widget = property_set_tool.get_predefine_pset_list_widget()
    property_set_tool.create_context_menu(list_widget.mapToGlobal(pos), functions)


def pset_item_double_clicked(item, property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_property_set_from_item(item)
    open_pset_window(property_set, property_set_tool, attribute_tool)


def pset_selection_changed(property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_selecte_property_set_from_table()
    property_set_tool.set_active_property_set(property_set)
    attribute_core.refresh_attribute_table(som_gui.MainUi.ui.table_attribute, attribute_tool)


def pset_table_context_menu(pos, property_set_tool: Type[PropertySet]):
    table = property_set_tool.get_table()
    pset = property_set_tool.get_pset_from_item(table.itemAt(pos))
    if pset.is_child:

        actions = [["Löschen", property_set_tool.delete_table_pset], ]
    else:

        actions = [["Umbenennen", property_set_tool.rename_table_pset],
                   ["Löschen", property_set_tool.delete_table_pset], ]

    property_set_tool.create_context_menu(table.mapToGlobal(pos), actions)


def pset_table_edit_started(property_set: Type[PropertySet]):
    pset = property_set.get_selecte_property_set_from_table()
    table = property_set.get_table()
    for row in range(table.rowCount()):
        if property_set.get_property_set_from_row(row, table) == pset:
            property_set.set_pset_name_by_row(pset, row, table)

    props = property_set.get_pset_properties()
    props.is_renaming_property_set = True


def pset_table_edit_stopped(property_set_tool: Type[PropertySet]):
    props = property_set_tool.get_pset_properties()
    props.is_renaming_property_set = False


def rename_pset_by_editor(new_name: str, index: QModelIndex, property_set_tool: Type[PropertySet]):
    pset = property_set_tool.get_pset_from_index(index)
    pset.name = new_name


def repaint_predefined_pset_inheritance_list(property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_active_predefined_pset()
    list_widget = property_set_tool.get_predefined_pset_inheritance_list()

    if property_set is None:
        list_widget.clear()
        return
    predefined_property_sets = set(property_set.children)
    existing_property_sets = property_set_tool.get_existing_psets_in_list(list_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)
    property_set_tool.remove_property_sets_from_list(delete_property_sets, list_widget)
    property_set_tool.add_property_sets_to_inheritance_list(sorted(add_property_sets, key=lambda p: p.name),
                                                            list_widget)
    property_set_tool.update_predefined_pset_inheritance_list()


def repaint_predefined_pset_list(property_set_tool: Type[PropertySet]):
    if property_set_tool.predefined_pset_list_is_editing():
        return
    property_set_tool.get_predefine_pset_list_widget()
    predefined_property_sets = set(property_set_tool.get_predefined_psets())
    list_widget = property_set_tool.get_predefine_pset_list_widget()
    existing_property_sets = property_set_tool.get_existing_psets_in_list(list_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)
    property_set_tool.remove_property_sets_from_list(delete_property_sets, list_widget)
    property_set_tool.add_property_sets_to_list(sorted(add_property_sets), list_widget)
    property_set_tool.update_predefined_pset_list()


def repaint_predefined_pset_window(property_set_tool: Type[PropertySet]):
    repaint_predefined_pset_list(property_set_tool)
    repaint_predefined_pset_inheritance_list(property_set_tool)
    pass


def repaint_pset_table(property_set_tool: Type[PropertySet], object_tool: Type[Object]):
    if object_tool.get_active_object() is not None:
        property_set_tool.set_enabled(True)
    else:
        property_set_tool.set_enabled(False)

    if property_set_tool.pset_table_is_editing():
        return

    new_property_sets = property_set_tool.get_property_sets()
    table = property_set_tool.get_table()

    existing_property_sets = property_set_tool.get_existing_psets_in_table(table)
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets, table)
    property_set_tool.add_property_sets_to_table(add_property_sets, table)
    property_set_tool.update_property_set_table(table)


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


def table_double_clicked(property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_selecte_property_set_from_table()
    window = property_set_tool.open_pset_window(property_set)
    table = attribute_tool.get_table(window)
    attribute_core.refresh_attribute_table(table, attribute_tool)
    table.resizeColumnsToContents()
    pass


def update_seperator(window: PropertySetWindow, property_set_tool: Type[PropertySet], settings_tool: Type[Settings]):
    text, state = property_set_tool.get_seperator_state(window)
    settings_tool.set_seperator_status(state)
    settings_tool.set_seperator(text)


def value_type_changed(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    value_type = property_set_tool.pw_get_value_type(window)
    if value_type == RANGE:
        property_set_tool.set_value_columns(2, window)
        property_set_tool.restrict_data_type_to_numbers(window)
    else:
        property_set_tool.set_value_columns(1, window)
        property_set_tool.remove_data_type_restriction(window)


from __future__ import annotations
from PySide6 import QtGui
from PySide6.QtCore import QModelIndex
from som_gui.core import attribute as attribute_core
from SOMcreator.constants.value_constants import RANGE

from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool import PropertySet, Object, Attribute, Settings, MainWindow, Popups
    from som_gui.module.property_set.ui import PropertySetWindow

import som_gui
import SOMcreator
