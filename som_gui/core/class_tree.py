from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QMimeData
from PySide6.QtGui import QDropEvent

import SOMcreator
from som_gui import tool
from som_gui.core.property_set import repaint_pset_table as refresh_property_set_table
import som_gui.module.class_tree.constants as constants
import copy as cp

if TYPE_CHECKING:
    from som_gui.tool import Project, Search, PropertySet, MainWindow
    from som_gui.module.class_info.prop import ClassDataDict
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint
    from som_gui.module.class_tree import ui

import uuid


def init_main_window(
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
    main_window: Type[tool.MainWindow],
) -> None:

    # Build Ckass Tree
    tree = class_tree.get_class_tree()
    tree.setColumnCount(0)
    class_tree.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Class"),
        0,
        lambda c: getattr(c, "name"),
    )
    class_tree.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Identifier"),
        1,
        lambda o: (
            getattr(o, "ident_value")
            if isinstance(o.identifier_property, SOMcreator.SOMProperty)
            else ""
        ),
    )
    class_tree.add_column_to_tree(
        lambda: QCoreApplication.translate("Class", "Optional"),
        2,
        lambda o: o.is_optional(ignore_hirarchy=True),
        class_tree.set_class_optional_by_tree_item_state,
    )

    # Add Class Activate Functions
    class_tree.add_class_activate_function(
        lambda o: main_window.get_class_name_label().setText(o.name)
    )
    # Add Creation Checks
    class_tree.add_class_creation_check(
        "ident_property_name", class_info.is_ident_property_valid
    )
    class_tree.add_class_creation_check("ident_value", class_info.is_identifier_unique)


def retranslate_ui(class_tree: Type[tool.ClassTree]) -> None:
    header = class_tree.get_class_tree().headerItem()
    for column, name in enumerate(class_tree.get_header_names()):
        header.setText(column, name)


def create_mime_data(
    items: QTreeWidgetItem, mime_data: QMimeData, class_tree: Type[tool.ClassTree]
):
    classes = {class_tree.get_class_from_item(i) for i in items}
    class_tree.write_classes_to_mimedata(classes, mime_data)
    return mime_data


def add_shortcuts(
    class_tree: Type[tool.ClassTree],
    util: Type[tool.Util],
    search_tool: Type[Search],
    main_window: Type[tool.MainWindow],
    project: Type[tool.Project],
    class_info: Type[tool.ClassInfo],
):
    util.add_shortcut("Ctrl+X", main_window.get(), class_tree.delete_selection)
    util.add_shortcut("Ctrl+G", main_window.get(), class_tree.group_selection)
    util.add_shortcut(
        "Ctrl+F",
        main_window.get(),
        lambda: search_class(search_tool, class_tree, project),
    )
    util.add_shortcut(
        "Ctrl+C", main_window.get(), lambda: class_info.trigger_class_info_widget(2)
    )


def search_class(
    search_tool: Type[Search], class_tree: Type[tool.ClassTree], project: Type[tool.Project]
):
    """Open Search Window and select Class afterwards"""
    som_class = search_tool.search_class(list(project.get().get_classes(filter=True)))
    class_tree.select_class(som_class)


def reset_tree(class_tree: Type[tool.ClassTree]):
    class_tree.get_properties().first_paint = True


def resize_columns(class_tree: Type[tool.ClassTree]):
    """
    resizes Colums to Content
    """
    class_tree.resize_tree()


def load_context_menus(
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
    project: Type[tool.Project],
):
    class_tree.clear_context_menu_list()
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Copy"),
        lambda: class_info.trigger_class_info_widget(2),
        True,
        True,
        False,
    )
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Delete"),
        class_tree.delete_selection,
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Extend"),
        class_tree.expand_selection,
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Collapse"),
        class_tree.collapse_selection,
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Group"),
        class_tree.group_selection,
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        lambda: QCoreApplication.translate("Class", "Info"),
        lambda: class_info.trigger_class_info_widget(1),
        True,
        True,
        False,
    )


def create_group(class_tree: Type[tool.ClassTree], project: Type[tool.Project]):
    d = {
        "name": QCoreApplication.translate("Class", "NewGroup"),
        "is_group": True,
        "ifc_mappings": ["IfcGroup"],
    }
    is_allowed = class_tree.check_class_creation_input(d)
    if not is_allowed:
        return
    som_class = class_tree.create_class(d, None, None)
    som_class.project = project.get()
    selected_classes = set(class_tree.get_selected_classes())
    class_tree.group_classes(som_class, selected_classes)


def create_context_menu(pos: QPoint, class_tree: Type[tool.ClassTree]):
    menu = class_tree.create_context_menu()
    menu_pos = class_tree.get_class_tree().viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_class_tree(class_tree: Type[tool.ClassTree], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    logging.debug(f"Repaint Class Widget")
    load_classes(class_tree, project_tool)
    # class_tree.autofit_tree()


def load_classes(class_tree: Type[tool.ClassTree], project_tool: Type[Project]):

    root_classes = project_tool.get_root_classes(filter_classes=True)
    tree: QTreeWidget = class_tree.get_class_tree()
    if class_tree.get_properties().first_paint:
        class_tree.clear_tree()
        class_tree.get_properties().first_paint = False
        retranslate_ui(class_tree)
    class_tree.fill_class_tree(set(root_classes), tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, class_tree: Type[tool.ClassTree]):
    class_tree.update_check_state(item)
    pass


def item_selection_changed(
    class_tree: Type[tool.ClassTree], property_set_tool: Type[PropertySet]
):
    selected_items = class_tree.get_selected_items()
    if len(selected_items) == 1:
        selected_pset = property_set_tool.get_active_property_set()
        som_class = class_tree.get_class_from_item(selected_items[0])
        class_tree.set_active_class(som_class)
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


def drop_event(
    event: QDropEvent,
    target: ui.ClassTreeWidget,
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    pos = event.pos()
    source_table = event.source()
    if source_table == target:
        dropped_on_item = class_tree.get_item_from_pos(pos)
        class_tree.handle_class_move(dropped_on_item)
        return
    classes = class_tree.get_classes_from_mimedata(event.mimeData())
    if not classes:
        return
    for som_class in classes:
        project.get().add_item(som_class)


def modify_class(
    som_class: SOMcreator.SOMClass,
    data_dict: ClassDataDict,
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
    property_set: Type[tool.PropertySet],
    predefined_psets: Type[tool.PredefinedPropertySet],
):

    data_dict = class_info.generate_datadict()
    identifer = data_dict.get("ident_value")
    pset_name = data_dict.get("ident_pset_name")
    property_name = data_dict.get("ident_property_name")
    ident_value = data_dict.get("ident_value")
    is_group = (
        som_class.is_concept
        if data_dict.get("is_group") is None
        else data_dict.get("is_group")
    )

    # check if identifier is allowed
    if not class_tree.is_identifier_allowed(identifer, som_class.ident_value, is_group):
        class_tree.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle Plugin checks
    result = class_info.are_plugin_requirements_met(som_class, data_dict)
    if result != constants.OK:
        class_tree.handle_property_issue(result)
        return
    if not is_group and property_name and pset_name:
        pset = som_class.get_property_set_by_name(pset_name)
        if not pset:
            # create identifier property_set
            parent = property_set.search_for_parent(
                pset_name,
                predefined_psets.get_property_sets(),
                property_set.get_inheritable_property_sets(som_class),
            )
            if parent == False:
                # action aborted
                return
            pset = property_set.create_property_set(pset_name, som_class, parent)
        ident_property = pset.get_property_by_name(property_name)
        if not ident_property:
            # create ident property
            ident_property = SOMcreator.SOMProperty(
                name=property_name,
            )
            pset.add_property(ident_property)
        ident_property.allowed_values = [ident_value]

    class_tree.modify_class(som_class, data_dict)
    class_info.add_plugin_infos_to_class(som_class, data_dict)
    class_tree.fill_class_entry(som_class)


def copy_class(
    som_class: SOMcreator.SOMClass,
    data_dict: ClassDataDict,
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
):

    # handle Group
    if data_dict.get("is_group"):
        group = cp.copy(som_class)
        group.identifier_property = uuid.uuid4()
        group.description = data_dict.get("description") or ""
        class_tree.trigger_class_modification(group, data_dict)
        return
    # handle Identifier Value
    ident_value = data_dict.get("ident_value")
    if not class_tree.is_identifier_allowed(ident_value):
        class_tree.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle plugin checks
    result = class_info.are_plugin_requirements_met(som_class, data_dict)
    if result != constants.OK:
        class_tree.handle_property_issue(result)
        return

    new_class = cp.copy(som_class)
    class_tree.trigger_class_modification(new_class, data_dict)


def create_class(
    data_dict: ClassDataDict,
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
    project: Type[Project],
    property_set: Type[tool.PropertySet],
    predefined_property_set: Type[tool.PredefinedPropertySet],
):
    name = data_dict["name"]
    is_group = data_dict["is_group"]
    identifier = data_dict.get("ident_value")
    pset_name = data_dict.get("ident_pset_name")
    property_name = data_dict.get("ident_property_name")
    description = data_dict.get("description") or ""
    proj = project.get()
    # handle group
    if is_group:
        som_class = SOMcreator.SOMClass(name, project=proj)
        som_class.ident_value = str(som_class.uuid)
        som_class.description = description
        return

    # handle identifier
    if not class_tree.is_identifier_allowed(identifier):
        class_tree.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle plugin checks
    result = class_info.are_plugin_requirements_met(None, data_dict)
    if result != constants.OK:
        class_tree.handle_property_issue(result)
        return
    som_class = SOMcreator.SOMClass(name, project=proj)
    som_class.description = description

    # create identifier property_set
    parent_pset = property_set.search_for_parent(
        pset_name,
        predefined_property_set.get_property_sets(),
    )
    pset = property_set.create_property_set(pset_name, som_class, parent_pset)

    # create identifier property
    ident_property = pset.get_property_by_name(property_name)
    if not ident_property:
        ident_property = SOMcreator.SOMProperty(
            pset,
            property_name,
        )
    ident_property.allowed_values = [identifier]
    ident_property.project = proj
    class_info.add_plugin_infos_to_class(som_class, data_dict)
    class_tree.modify_class(som_class, data_dict)
    refresh_class_tree(class_tree, project)
