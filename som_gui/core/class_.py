from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication

import SOMcreator
from som_gui import tool
from som_gui.core.property_set import repaint_pset_table as refresh_property_set_table

if TYPE_CHECKING:
    from som_gui.tool import Class, Project, Search, PropertySet, MainWindow

    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint

import uuid


def init_main_window(
    class_tool: Type[tool.Class], main_window: Type[tool.MainWindow]
) -> None:

    # Build Ckass Tree
    tree = class_tool.get_class_tree()
    tree.setColumnCount(0)
    class_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Class"),
        0,
        lambda o: getattr(o, "name"),
    )
    class_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Identifier"),
        1,
        lambda o: getattr(o, "ident_value"),
    )
    class_tool.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Optional"),
        2,
        lambda o: o.is_optional(ignore_hirarchy=True),
        class_tool.set_class_optional_by_tree_item_state,
    )

    # Add Class Activate Functions
    class_tool.add_class_activate_function(
        lambda o: main_window.get_class_name_label().setText(o.name)
    )
    # Add Creation Checks
    class_tool.add_class_creation_check(
        "ident_property_name", class_tool.is_ident_property_valid
    )
    class_tool.add_class_creation_check("ident_value", class_tool.is_identifier_unique)


def retranslate_ui(class_tool: Type[tool.Class]) -> None:
    header = class_tool.get_class_tree().headerItem()
    for column, name in enumerate(class_tool.get_header_names()):
        header.setText(column, name)


def add_shortcuts(
    class_tool: Type[Class],
    util: Type[tool.Util],
    search_tool: Type[Search],
    main_window: Type[tool.MainWindow],
    project: Type[tool.Project],
):
    util.add_shortcut("Ctrl+X", main_window.get(), class_tool.delete_selection)
    util.add_shortcut("Ctrl+G", main_window.get(), class_tool.group_selection)
    util.add_shortcut(
        "Ctrl+F",
        main_window.get(),
        lambda: search_class(search_tool, class_tool, project),
    )


def search_class(
    search_tool: Type[Search], class_tool: Type[Class], project: Type[tool.Project]
):
    """Open Search Window and select Class afterwards"""
    som_class = search_tool.search_class(list(project.get().get_classes(filter=True)))
    class_tool.select_class(som_class)


def reset_tree(class_tool: Type[Class]):
    class_tool.get_properties().first_paint = True


def resize_columns(class_tool: Type[Class]):
    """
    resizes Colums to Content
    """
    class_tool.resize_tree()




def load_context_menus(class_tool: Type[Class], util: Type[tool.Util]):
    class_tool.clear_context_menu_list()
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Copy"),
        lambda: class_tool.trigger_class_info_widget(2),
        True,
        False,
    )
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Delete"),
        class_tool.delete_selection,
        True,
        True,
    )
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Extend"),
        class_tool.expand_selection,
        True,
        True,
    )
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Collapse"),
        class_tool.collapse_selection,
        True,
        True,
    )
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Group"),
        lambda: create_group(class_tool),
        True,
        True,
    )
    class_tool.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Info"),
        lambda: class_tool.trigger_class_info_widget(1),
        True,
        False,
    )


def create_group(class_tool: Type[Class]):
    d = {
        "name": QCoreApplication.translate("Class", "NewGroup"),
        "is_group": True,
        "ifc_mappings": ["IfcGroup"],
    }
    is_allowed = class_tool.check_class_creation_input(d)
    if not is_allowed:
        return
    som_class = class_tool.create_class(d, None, None)
    selected_classes = set(class_tool.get_selected_classes())
    class_tool.group_classes(som_class, selected_classes)


def create_context_menu(pos: QPoint, class_tool: Type[Class]):
    menu = class_tool.create_context_menu()
    menu_pos = class_tool.get_class_tree().viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_class_tree(class_tool: Type[Class], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    logging.debug(f"Repaint Class Widget")
    load_classes(class_tool, project_tool)
    # class_tool.autofit_tree()


def load_classes(class_tool: Type[Class], project_tool: Type[Project]):
    root_classes = project_tool.get_root_classes(filter_classes=True)
    class_tree: QTreeWidget = class_tool.get_class_tree()
    class_tool.fill_class_tree(set(root_classes), class_tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, class_tool: Type[Class]):
    class_tool.update_check_state(item)
    pass


def item_selection_changed(
    class_tool: Type[Class], property_set_tool: Type[PropertySet]
):
    selected_items = class_tool.get_selected_items()
    if len(selected_items) == 1:
        selected_pset = property_set_tool.get_active_property_set()
        som_class = class_tool.get_class_from_item(selected_items[0])
        class_tool.set_active_class(som_class)
        property_set_tool.update_completer(som_class)
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


def item_dropped_on(pos: QPoint, class_tool: Type[Class]):
    selected_items = class_tool.get_selected_items()
    dropped_on_item = class_tool.get_item_from_pos(pos)
    dropped_classes = [class_tool.get_class_from_item(item) for item in selected_items]
    dropped_classes = [
        o
        for o in dropped_classes
        if o.parent not in dropped_classes or o.parent is None
    ]
    if dropped_on_item is None:
        for som_class in dropped_classes:
            som_class.remove_parent()
        return
    dropped_on_class = class_tool.get_class_from_item(dropped_on_item)

    if not class_tool.drop_indication_pos_is_on_item():
        dropped_on_class = dropped_on_class.parent

    for som_class in dropped_classes:
        if dropped_on_class is None:
            som_class.remove_parent()
        else:
            som_class.parent = dropped_on_class


def modify_class(class_tool: Type[tool.Class],class_info:Type[tool.ClassInfo]):
    data_dict = class_info.oi_get_values()
    focus_class = class_info.oi_get_focus_class()
    result = class_tool.change_class_info(focus_class, data_dict)
    if class_tool.handle_property_issue(result):
        class_tool.fill_class_entry(focus_class)


def copy_class(class_tool: Type[tool.Class],class_info:Type[tool.ClassInfo]):
    data_dict = class_info.oi_get_values()
    focus_class = class_info.oi_get_focus_class()
    result, focus_class = class_tool.copy_class(focus_class, data_dict)
    if class_tool.handle_property_issue(result):
        class_tool.fill_class_entry(focus_class)


def create_class(
    class_tool: Type[tool.Class],
    class_info:Type[tool.ClassInfo],
    project: Type[Project],
    property_set: Type[tool.PropertySet],
    predefined_property_set: Type[tool.PredefinedPropertySet],
    popup: Type[tool.Popups],
    util: Type[tool.Util],
):
    from som_gui.module.class_ import (
        IDENT_ISSUE,
        IDENT_PROPERTY_ISSUE,
        IDENT_PSET_ISSUE,
    )

    data_dict = class_info.oi_get_values()
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
        if identifier is None or not class_tool.is_identifier_allowed(identifier):
            return class_tool.handle_property_issue(IDENT_ISSUE)

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
        class_tool.create_class(data_dict, pset, ident_property)
        refresh_class_tree(class_tool, project)
