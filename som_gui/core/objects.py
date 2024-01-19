from __future__ import annotations

import uuid
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool import Objects, Project
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint


def object_info_accept(object_tool: Type[Objects]):
    name, abbreviation, group, pset, attribute, ident_value, ifc_mappings = object_tool.oi_get_values()
    active_object = object_tool.get_active_object()

    if group:
        active_object.name = name
        active_object.ifc_mapping = ifc_mappings
        if not active_object.is_concept:
            active_object.ident_attrib = str(uuid.uuid4())
            object_tool.fill_object_entry(active_object)
        return
    if not object_tool.abbreviation_is_allowed(abbreviation, active_object.abbreviation):
        print(f"Abkürzung existiert bereits")
        return
    if not object_tool.identifier_is_allowed(ident_value, active_object.ident_value):
        print(f"Identifier existiert bereits")
        return
    active_object.name = name
    active_object.ifc_mapping = ifc_mappings
    ident_attribute = object_tool.find_attribute(active_object, pset, attribute)
    active_object.ident_attrib = ident_attribute
    active_object.abbreviation = abbreviation
    object_tool.fill_object_entry(active_object)


def object_info_refresh(object_tool: Type[Objects]):
    name, abbreviation, group, pset, attribute, ident_value, ifc_mappings = object_tool.oi_get_values()
    object_tool.oi_set_values(name, abbreviation, group, pset, attribute, ident_value, ifc_mappings)
    if not object_tool.identifier_is_allowed(ident_value, object_tool.get_active_object().ident_value):
        object_tool.oi_set_ident_value_color("red")
    else:
        object_tool.oi_set_ident_value_color("black")

    if not object_tool.abbreviation_is_allowed(abbreviation, object_tool.get_active_object().abbreviation):
        object_tool.oi_set_abbrev_value_color("red")
    else:
        object_tool.oi_set_abbrev_value_color("black")

    object_tool.oi_change_visibility_identifiers(group)


def object_info_pset_changed(object_tool: Type[Objects]):
    object_tool.oi_update_attribute_combobox()


def object_info_add_ifc(object_tool: Type[Objects]):
    object_tool.add_ifc_mapping("")


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


def item_double_clicked(object_tool: Type[Objects]):
    object_tool.oi_fill_properties()
    object_tool.oi_update_dialog()


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
