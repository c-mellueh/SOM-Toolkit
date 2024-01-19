from __future__ import annotations

import logging
import uuid
from typing import Type, TYPE_CHECKING

import SOMcreator

import som_gui.module.objects

if TYPE_CHECKING:
    from som_gui.tool import Objects, Project
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint


def create_object_info_widget(mode: int, object_tool: Type[Objects]):
    dialog = object_tool.oi_create_widget()
    widget = dialog.widget
    widget.button_add_ifc.pressed.connect(lambda: object_info_add_ifc(object_tool))
    widget.combo_box_pset.currentIndexChanged.connect(lambda: object_info_pset_changed(object_tool))
    object_tool.oi_fill_properties(mode=mode)
    object_tool.oi_update_dialog()
    if dialog.exec():
        object_info_accept(object_tool)


def object_info_accept(object_tool: Type[Objects]):
    data_dict = object_tool.oi_get_values()
    focus_object = object_tool.oi_get_focus_object()
    mode = object_tool.oi_get_mode()
    result = 666
    if mode == 1:
        result = object_tool.change_object_info(focus_object, data_dict)
    if mode == 2:
        result, focus_object = object_tool.copy_object(focus_object, data_dict)
    if object_tool.handle_attribute_issue(result):
        object_tool.fill_object_entry(focus_object)


def object_info_refresh(object_tool: Type[Objects]):
    data_dict = object_tool.oi_get_values()
    object_tool.oi_set_values(data_dict)
    ident_value = data_dict["ident_value"]
    abbreviation = data_dict["abbreviation"]
    group = data_dict["is_group"]

    ident_filter = object_tool.get_active_object().ident_value if object_tool.oi_get_mode() == 1 else None
    abbrev_filter = object_tool.get_active_object().abbreviation if object_tool.oi_get_mode() == 1 else None
    if not object_tool.identifier_is_allowed(ident_value, ident_filter):
        object_tool.oi_set_ident_value_color("red")
    else:
        object_tool.oi_set_ident_value_color("black")

    if not object_tool.abbreviation_is_allowed(abbreviation, abbrev_filter):
        object_tool.oi_set_abbrev_value_color("red")
    else:
        object_tool.oi_set_abbrev_value_color("black")
    object_tool.oi_change_visibility_identifiers(group)


def object_info_pset_changed(object_tool: Type[Objects]):
    object_tool.oi_update_attribute_combobox()


def object_info_add_ifc(object_tool: Type[Objects]):
    object_tool.add_ifc_mapping("")


def load_context_menus(object_tool: Type[Objects]):
    object_tool.clear_context_menu_list()
    object_tool.add_context_menu_entry("Kopieren", lambda: create_object_info_widget(2, object_tool), True, False)
    object_tool.add_context_menu_entry("Löschen", object_tool.delete_selection, True, True)
    object_tool.add_context_menu_entry("Ausklappen", object_tool.expand_selection, True, True)
    object_tool.add_context_menu_entry("Einklappen", object_tool.collapse_selection, True, True)
    object_tool.add_context_menu_entry("Gruppieren", lambda: create_group(object_tool), True, True)
    object_tool.add_context_menu_entry("Info", lambda: create_object_info_widget(1, object_tool), True, False)


def create_group(object_tool: Type[Objects]):
    d = {
        "name":         "NeueGruppe",
        "is_group":     True,
        "ifc_mappings": ["IfcGroup"]
    }
    result, obj = object_tool.create_object(d)
    if result == som_gui.module.objects.OK:
        selected_objects = set(object_tool.get_selected_objects())
        object_tool.group_objects(obj, selected_objects)


def create_context_menu(pos: QPoint, object_tool: Type[Objects]):
    menu = object_tool.create_context_menu()
    menu_pos = object_tool.get_object_tree().viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_object_tree(object_tool: Type[Objects], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    load_objects(object_tool, project_tool)


def load_objects(object_tool: Type[Objects], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter=True)
    object_tree: QTreeWidget = object_tool.get_object_tree()
    object_tool.fill_object_tree(set(root_objects), object_tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, object_tool: Type[Objects]):
    object_tool.update_check_state(item)
    pass


def item_selection_changed(object_tool: Type[Objects]):
    selected_items = object_tool.get_selected_items()
    if len(selected_items) == 1:
        obj = object_tool.get_object_from_item(selected_items[0])
        object_tool.set_active_object(obj)


def item_dropped_on(pos: QPoint, object_tool: Type[Objects]):
    selected_items = object_tool.get_selected_items()
    dropped_on_item = object_tool.get_item_from_pos(pos)
    if dropped_on_item is None:
        return
    dropped_on_object = object_tool.get_object_from_item(dropped_on_item)
    if not object_tool.drop_indication_pos_is_on_item():
        dropped_on_object = dropped_on_object.parent
    dropped_objects = [object_tool.get_object_from_item(item) for item in selected_items]
    for obj in dropped_objects:
        if dropped_on_object is None:
            obj.remove_parent()
        else:
            obj.parent = dropped_on_object
