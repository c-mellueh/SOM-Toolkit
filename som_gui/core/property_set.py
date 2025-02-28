from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from som_gui.core import attribute_table as attribute_table_core
from som_gui.core import property_set_window as property_set_window_core

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window.ui import PropertySetWindow
    from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QModelIndex, Qt, QCoreApplication


def add_property_set_button_pressed(
    object_tool: Type[tool.Object],
    main_window_tool: Type[tool.MainWindow],
    property_set_tool: Type[tool.PropertySet],
    popup_tool: Type[tool.Popups],
    predefined_psets: Type[tool.PredefinedPropertySet],
):
    obj = object_tool.get_active_object()
    title = QCoreApplication.translate("PropertySet", "Add PropertySet")
    name = QCoreApplication.translate("PropertySet", "PropertySet name?")
    if not name:
        return
    pset_name = popup_tool._request_text_input(title,name,prefill = "",parent = main_window_tool.get())
    if property_set_tool.check_if_pset_allready_exists(pset_name, obj):
        text = QCoreApplication.translate(
            f"PropertySet", "PropertySet '{}' exists allready"
        ).format(pset_name)
        popup_tool.create_warning_popup(text)
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


def pset_selection_changed(
    property_set_tool: Type[tool.PropertySet],
    attribute_table: Type[tool.AttributeTable],
    main_window: Type[tool.MainWindow],
):
    property_set = property_set_tool.get_selecte_property_set_from_table()
        

    property_set_tool.set_active_property_set(property_set)
    attribute_table.set_property_set_of_table(
        main_window.get_attribute_table(), property_set
    )
    attribute_table_core.update_attribute_table(
        main_window.get_attribute_table(), attribute_table
    )
    text = "" if not property_set else property_set.name

    main_window.get_pset_name_label().setText(text)


def pset_table_context_menu(pos, property_set_tool: Type[tool.PropertySet]):

    table = property_set_tool.get_table()
    if not table.itemAt(pos):
        return
    pset = property_set_tool.get_pset_from_item(table.itemAt(pos))
    if pset.is_child:

        actions = [
            [
                QCoreApplication.translate(f"PropertySet", "Delete"),
                property_set_tool.delete_table_pset,
            ],
        ]
    else:

        actions = [
            [
                QCoreApplication.translate(f"PropertySet", "Rename"),
                property_set_tool.rename_table_pset,
            ],
            [
                QCoreApplication.translate(f"PropertySet", "Delete"),
                property_set_tool.delete_table_pset,
            ],
        ]

    property_set_tool.create_context_menu(table.mapToGlobal(pos), actions)


def pset_table_edit_started(property_set: Type[tool.PropertySet]):
    pset = property_set.get_selecte_property_set_from_table()
    table = property_set.get_table()
    for row in range(table.rowCount()):
        if property_set.get_property_set_from_row(row, table) == pset:
            property_set.set_pset_name_by_row(pset, row, table)

    props = property_set.get_properties()
    props.is_renaming_property_set = True


def pset_table_edit_stopped(property_set_tool: Type[tool.PropertySet]):
    props = property_set_tool.get_properties()
    props.is_renaming_property_set = False


def rename_pset_by_editor(
    new_name: str, index: QModelIndex, property_set_tool: Type[tool.PropertySet]
):
    pset = property_set_tool.get_pset_from_index(index)
    pset.name = new_name


def repaint_pset_table(
    property_set_tool: Type[tool.PropertySet], object_tool: Type[tool.Object]
):
    logging.debug(f"Repaint PropertySet Table")

    if object_tool.get_active_object() is None:
        property_set_tool.set_enabled(False)
        return

    property_set_tool.set_enabled(True)
    
    #if pset_table is in rename mode this blocks overwrites
    if property_set_tool.pset_table_is_editing(): 
        return

    new_property_sets = property_set_tool.get_property_sets()
    selected_pset = property_set_tool.get_active_property_set()
    table = property_set_tool.get_table()

    existing_property_sets = property_set_tool.get_existing_psets_in_table(table)
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets, table)
    property_set_tool.add_property_sets_to_table(add_property_sets, table)
    property_set_tool.update_property_set_table(table)

    if not selected_pset:
        return
    pset = {p.name:p for p in new_property_sets}.get(selected_pset.name)
    if pset:
        property_set_tool.select_property_set(pset)
        
def table_double_clicked(
    property_set_tool: Type[tool.PropertySet],
    attribute_table: Type[tool.AttributeTable],
    property_set_window: Type[tool.PropertySetWindow],
):
    property_set = property_set_tool.get_selecte_property_set_from_table()
    property_set_window_core.open_pset_window(
        property_set, property_set_window, attribute_table
    )
