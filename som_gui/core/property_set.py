from __future__ import annotations

import som_gui
from som_gui.core import property_set_window as property_set_window_core
from som_gui.core import attribute_table as attribute_table_core
from typing import Type, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window.ui import PropertySetWindow
    from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QModelIndex, Qt


def add_property_set_button_pressed(object_tool: Type[tool.Object], main_window_tool: Type[tool.MainWindow],
                                    property_set_tool: Type[tool.PropertySet], popup_tool: Type[tool.Popups],
                                    predefined_psets: Type[tool.PredefinedPropertySet]):
    obj = object_tool.get_active_object()
    pset_name = main_window_tool.get_pset_name()
    if property_set_tool.check_if_pset_allready_exists(pset_name, obj):
        popup_tool.create_warning_popup(f"PropertySet '{pset_name}' existiert bereits")
        return

    predefined_pset_dict = {p.name: p for p in predefined_psets.get_property_sets()}
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


def pset_clicked(item: QTableWidgetItem, property_set: Type[tool.PropertySet]):
    pset = property_set.get_pset_from_item(item)
    if not item.column() == 2:
        return
    cs = True if item.checkState() == Qt.CheckState.Checked else False
    pset.set_optional(cs)


def pset_selection_changed(property_set_tool: Type[tool.PropertySet], attribute_table: Type[tool.AttributeTable],
                           main_window: Type[tool.MainWindow]):
    property_set = property_set_tool.get_selecte_property_set_from_table()
    property_set_tool.set_active_property_set(property_set)
    attribute_table_core.paint_attribute_table(main_window.get_attribute_table(), attribute_table)


def pset_table_context_menu(pos, property_set_tool: Type[tool.PropertySet]):
    table = property_set_tool.get_table()
    pset = property_set_tool.get_pset_from_item(table.itemAt(pos))
    if pset.is_child:

        actions = [["Löschen", property_set_tool.delete_table_pset], ]
    else:

        actions = [["Umbenennen", property_set_tool.rename_table_pset],
                   ["Löschen", property_set_tool.delete_table_pset], ]

    property_set_tool.create_context_menu(table.mapToGlobal(pos), actions)


def pset_table_edit_started(property_set: Type[tool.PropertySet]):
    pset = property_set.get_selecte_property_set_from_table()
    table = property_set.get_table()
    for row in range(table.rowCount()):
        if property_set.get_property_set_from_row(row, table) == pset:
            property_set.set_pset_name_by_row(pset, row, table)

    props = property_set.get_pset_properties()
    props.is_renaming_property_set = True


def pset_table_edit_stopped(property_set_tool: Type[tool.PropertySet]):
    props = property_set_tool.get_pset_properties()
    props.is_renaming_property_set = False


def rename_pset_by_editor(new_name: str, index: QModelIndex, property_set_tool: Type[tool.PropertySet]):
    pset = property_set_tool.get_pset_from_index(index)
    pset.name = new_name


def repaint_pset_table(property_set_tool: Type[tool.PropertySet], object_tool: Type[tool.Object]):
    logging.debug(f"Repaint PropertySet Table")

    if object_tool.get_active_object() is not None:
        property_set_tool.set_enabled(True)
    else:
        property_set_tool.set_enabled(False)
        return

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


def table_double_clicked(property_set_tool: Type[tool.PropertySet], attribute_table: Type[tool.AttributeTable],
                         property_set_window: Type[tool.PropertySetWindow]):
    property_set = property_set_tool.get_selecte_property_set_from_table()
    property_set_window_core.open_pset_window(property_set, property_set_window, attribute_table)
