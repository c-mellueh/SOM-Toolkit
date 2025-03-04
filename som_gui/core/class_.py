from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette

import SOMcreator
from som_gui import tool
from som_gui.core.property_set import repaint_pset_table as refresh_property_set_table

if TYPE_CHECKING:
    from som_gui.tool import Class, Project, Search, PropertySet, MainWindow

    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint

import uuid


def init_main_window(
    object_tool: Type[tool.Class], main_window: Type[tool.MainWindow]
) -> None:

    # Build Object Tree
    tree = object_tool.get_class_tree()
    tree.setColumnCount(0)
    object_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Object", "Class"),
        0,
        lambda o: getattr(o, "name"),
    )
    object_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Object", "Identifier"),
        1,
        lambda o: getattr(o, "ident_value"),
    )
    object_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Object", "Optional"),
        2,
        lambda o: o.is_optional(ignore_hirarchy=True),
        object_tool.set_object_optional_by_tree_item_state,
    )

    # Add Object Activate Functions
    object_tool.add_object_activate_function(
        lambda o: main_window.get_object_name_label().setText(o.name)
    )
    # Add Creation Checks
    object_tool.add_object_creation_check(
        "ident_property_name", object_tool.is_ident_property_valid
    )
    object_tool.add_object_creation_check(
        "ident_value", object_tool.is_identifier_unique
    )


def retranslate_ui(object_tool: Type[tool.Class]) -> None:
    header = object_tool.get_class_tree().headerItem()
    for column, name in enumerate(object_tool.get_header_names()):
        header.setText(column, name)


def add_shortcuts(
    object_tool: Type[Class],
    util: Type[tool.Util],
    search_tool: Type[Search],
    main_window: Type[tool.MainWindow],
    project: Type[tool.Project],
):
    util.add_shortcut("Ctrl+X", main_window.get(), object_tool.delete_selection)
    util.add_shortcut("Ctrl+G", main_window.get(), object_tool.group_selection)
    util.add_shortcut(
        "Ctrl+F",
        main_window.get(),
        lambda: search_object(search_tool, object_tool, project),
    )


def search_object(
    search_tool: Type[Search], object_tool: Type[Class], project: Type[tool.Project]
):
    """Open Search Window and select Object afterwards"""
    obj = search_tool.search_object(list(project.get().get_classes(filter=True)))
    object_tool.select_class(obj)


def reset_tree(object_tool: Type[Class]):
    object_tool.get_properties().first_paint = True


def resize_columns(object_tool: Type[Class]):
    """
    resizes Colums to Content
    """
    object_tool.resize_tree()


def create_object_info_widget(
    mode: int,
    object_tool: Type[Class],
    predefined_property_set: Type[tool.PredefinedPropertySet],
    util: Type[tool.Util],
):
    """
    Opens Object Info Widget can be used for creation (mode 0), modification (mode 1) or copying (mode 2)
    """
    logging.debug(f"Create Object Info Widget Mode= {mode}")
    title = util.get_window_title(
        QCoreApplication.translate("ObjectInfo", "Object Info")
    )
    dialog = object_tool.oi_create_dialog(title)

    predefined_psets = predefined_property_set.get_property_sets()
    object_tool.oi_connect_dialog(dialog, predefined_psets)
    object_tool.oi_fill_properties(mode=mode)
    object_tool.oi_update_dialog(dialog)
    if mode == 0:
        names = [p.name for p in predefined_psets]
        object_tool.create_completer(names, dialog.widget.combo_box_pset)
    if dialog.exec():
        if mode == 0:
            object_tool.trigger_object_creation()
        elif mode == 1:
            object_tool.trigger_object_modification()
        elif mode == 2:
            object_tool.trigger_object_copy()


def object_info_refresh(object_tool: Type[Class]):
    data_dict = object_tool.oi_get_values()
    object_tool.oi_set_values(data_dict)
    ident_value = data_dict["ident_value"]
    group = data_dict["is_group"]
    ident_filter = (
        object_tool.get_active_class().ident_value
        if object_tool.oi_get_mode() == 1
        else None
    )
    if not object_tool.is_identifier_allowed(ident_value, [ident_filter]):
        object_tool.oi_set_ident_value_color("red")
    else:
        object_tool.oi_set_ident_value_color(QPalette().color(QPalette.Text).name())
    object_tool.oi_change_visibility_identifiers(group)


def object_info_add_ifc(object_tool: Type[Class]):
    object_tool.add_ifc_mapping("")


def load_context_menus(object_tool: Type[Class], util: Type[tool.Util]):
    object_tool.clear_context_menu_list()
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Copy"),
        lambda: object_tool.trigger_object_info_widget(2),
        True,
        False,
    )
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Delete"),
        object_tool.delete_selection,
        True,
        True,
    )
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Extend"),
        object_tool.expand_selection,
        True,
        True,
    )
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Collapse"),
        object_tool.collapse_selection,
        True,
        True,
    )
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Group"),
        lambda: create_group(object_tool),
        True,
        True,
    )
    object_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Object", "Info"),
        lambda: object_tool.trigger_object_info_widget(1),
        True,
        False,
    )


def create_group(object_tool: Type[Class]):
    d = {
        "name": QCoreApplication.translate("Object", "NewGroup"),
        "is_group": True,
        "ifc_mappings": ["IfcGroup"],
    }
    is_allowed = object_tool.check_class_creation_input(d)
    if not is_allowed:
        return
    obj = object_tool.create_class(d, None, None)
    selected_objects = set(object_tool.get_selected_classes())
    object_tool.group_classes(obj, selected_objects)


def create_context_menu(pos: QPoint, object_tool: Type[Class]):
    menu = object_tool.create_context_menu()
    menu_pos = object_tool.get_class_tree().viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_object_tree(object_tool: Type[Class], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    logging.debug(f"Repaint Object Widget")
    load_objects(object_tool, project_tool)
    # object_tool.autofit_tree()


def load_objects(object_tool: Type[Class], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter_objects=True)
    object_tree: QTreeWidget = object_tool.get_class_tree()
    object_tool.fill_object_tree(set(root_objects), object_tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, object_tool: Type[Class]):
    object_tool.update_check_state(item)
    pass


def item_selection_changed(
    object_tool: Type[Class], property_set_tool: Type[PropertySet]
):
    selected_items = object_tool.get_selected_items()
    if len(selected_items) == 1:
        selected_pset = property_set_tool.get_active_property_set()
        obj = object_tool.get_object_from_item(selected_items[0])
        object_tool.set_active_object(obj)
        property_set_tool.update_completer(obj)
        property_set_tool.set_enabled(True)
        property_set_tool.trigger_table_repaint()

        # reselect the same pset that is allready selected
        if not selected_pset:
            return
        pset = {p.name: p for p in property_set_tool.get_property_sets()}.get(
            selected_pset.name
        )
        if pset:
            property_set_tool.select_property_set(pset)
    else:
        property_set_tool.clear_table()
        property_set_tool.set_enabled(False)


def item_dropped_on(pos: QPoint, object_tool: Type[Class]):
    selected_items = object_tool.get_selected_items()
    dropped_on_item = object_tool.get_item_from_pos(pos)
    dropped_objects = [
        object_tool.get_object_from_item(item) for item in selected_items
    ]
    dropped_objects = [
        o
        for o in dropped_objects
        if o.parent not in dropped_objects or o.parent is None
    ]
    if dropped_on_item is None:
        for obj in dropped_objects:
            obj.remove_parent()
        return
    dropped_on_object = object_tool.get_object_from_item(dropped_on_item)

    if not object_tool.drop_indication_pos_is_on_item():
        dropped_on_object = dropped_on_object.parent

    for obj in dropped_objects:
        if dropped_on_object is None:
            obj.remove_parent()
        else:
            obj.parent = dropped_on_object


def modify_object(object_tool: Type[tool.Class]):
    data_dict = object_tool.oi_get_values()
    focus_object = object_tool.oi_get_focus_object()
    result = object_tool.change_class_info(focus_object, data_dict)
    if object_tool.handle_property_issue(result):
        object_tool.fill_object_entry(focus_object)


def copy_object(object_tool: Type[tool.Class]):
    data_dict = object_tool.oi_get_values()
    focus_object = object_tool.oi_get_focus_object()
    result, focus_object = object_tool.copy_class(focus_object, data_dict)
    if object_tool.handle_property_issue(result):
        object_tool.fill_object_entry(focus_object)


def create_object(
    object_tool: Type[Class],
    project: Type[Project],
    property_set: Type[tool.PropertySet],
    predefined_property_set: Type[tool.PredefinedPropertySet],
    popup: Type[tool.Popups],
    util: Type[tool.Util],
):
    from som_gui.module.object import (
        IDENT_ISSUE,
        IDENT_PROPERTY_ISSUE,
        IDENT_PSET_ISSUE,
    )

    data_dict = object_tool.oi_get_values()
    predefined_psets = {p.name: p for p in predefined_property_set.get_property_sets()}

    name = data_dict["name"]
    is_group = data_dict["is_group"]
    abbreviation = data_dict.get("abbreviation")
    ifc_mappings = data_dict.get("ifc_mappings")
    identifier = data_dict.get("ident_value")
    pset_name = data_dict.get("ident_pset_name")
    attribute_name = data_dict.get("ident_property_name")

    if is_group:
        ident = str(uuid.uuid4())
        som_class = SOMcreator.SOMClass(
            name, ident, uuid=ident, project=tool.Project.get()
        )
    else:
        if identifier is None or not object_tool.is_identifier_allowed(identifier):
            return object_tool.handle_property_issue(IDENT_ISSUE)

        parent = None
        if pset_name in predefined_psets:
            connect_result = popup.request_property_set_merge(pset_name, 1)
            if connect_result is None:
                return
            if connect_result:
                parent = predefined_psets.get(pset_name)

        pset = property_set.create_property_set(pset_name, None, parent)
        ident_property: SOMcreator.SOMProperty = {
            a.name: a for a in pset.get_properties(filter=False)
        }.get(attribute_name)

        if not ident_property:
            ident_property = SOMcreator.SOMProperty(
                pset,
                attribute_name,
                [identifier],
                SOMcreator.value_constants.LIST,
            )
        else:
            ident_property.value = [identifier]
        object_tool.create_class(data_dict, pset, ident_property)
        refresh_object_tree(object_tool, project)
