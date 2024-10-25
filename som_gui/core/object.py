from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette

import SOMcreator
from som_gui import tool
from som_gui.core.property_set import repaint_pset_table as refresh_property_set_table

if TYPE_CHECKING:
    from som_gui.tool import Object, Project, Search, PropertySet, MainWindow

    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint


def init_main_window(object_tool: Type[tool.Object], main_window: Type[tool.MainWindow]) -> None:
    tree = object_tool.get_object_tree()
    tree.setColumnCount(0)
    object_tool.add_column_to_tree(lambda: QCoreApplication.translate("Object", "Object"), 0,
                                   lambda o: getattr(o, "name"))
    object_tool.add_column_to_tree(lambda: QCoreApplication.translate("Object", "Identifier"), 1,
                                   lambda o: getattr(o, "ident_value"))
    object_tool.add_column_to_tree(lambda: QCoreApplication.translate("Object", "Optional"), 2,
                                   lambda o: o.is_optional(ignore_hirarchy=True),
                                   object_tool.set_object_optional_by_tree_item_state)

    object_tool.add_object_activate_function(lambda o: main_window.get_object_name_line_edit().setText(o.name))
    pset_le = main_window.get_ident_pset_name_line_edit()
    attribute_e = main_window.get_attribute_name_line_edit()
    object_tool.add_object_activate_function(lambda o: object_tool.fill_object_property_set_line_edit(pset_le, o))
    object_tool.add_object_activate_function(lambda o: object_tool.fill_object_attribute_line_edit(attribute_e, o))
    object_tool.add_object_activate_function(lambda o: main_window.get_ident_value_line_edit().setText(o.ident_value))

    object_tool.add_objects_infos_add_function("name", main_window.get_object_name_line_edit().text)
    object_tool.add_objects_infos_add_function("is_group", lambda: False)
    object_tool.add_objects_infos_add_function("ident_pset_name", main_window.get_ident_pset_name_line_edit().text)
    object_tool.add_object_creation_check("ident_pset_name", object_tool.check_if_ident_pset_is_valid)

    object_tool.add_objects_infos_add_function("ident_attribute_name", main_window.get_attribute_name_line_edit().text)
    object_tool.add_object_creation_check("ident_attribute_name", object_tool.check_if_ident_attribute_is_valid)

    object_tool.add_objects_infos_add_function("ident_value", main_window.get_ident_value_line_edit().text)
    object_tool.add_object_creation_check("ident_value", object_tool.check_if_identifier_is_unique)
    object_tool.add_objects_infos_add_function("ifc_mappings", lambda: ["IfcBuildingElementProxy"])


def retranslate_ui(object_tool: Type[tool.Object]) -> None:
    header = object_tool.get_object_tree().headerItem()
    for column, name in enumerate(object_tool.get_header_names()):
        header.setText(column, name)


def connect_object_input_widget(object_tool: Type[tool.Object], main_window: Type[tool.MainWindow],
                                predefined_pset: Type[tool.PredefinedPropertySet]):
    main_window.get_ui().lineEdit_ident_pSet.textChanged.connect(
        lambda: ident_pset_changed(object_tool, main_window, predefined_pset))
    main_window.get_ui().lineEdit_ident_attribute.textChanged.connect(
        lambda: ident_attribute_changed(object_tool, main_window, predefined_pset))


def ident_pset_changed(object_tool: Type[tool.Object], main_window: Type[tool.MainWindow],
                       predefined_pset: Type[tool.PredefinedPropertySet]):
    pset_names = sorted([p.name for p in predefined_pset.get_property_sets()])
    object_tool.create_completer(pset_names, main_window.get_ui().lineEdit_ident_pSet)


def ident_attribute_changed(object_tool: Type[tool.Object], main_window: Type[tool.MainWindow],
                            predefined_pset: Type[tool.PredefinedPropertySet]):
    ident_pset_name = object_tool.get_object_infos()["ident_pset_name"]
    predefined_pset: SOMcreator.PropertySet = {p.name: p for p in predefined_pset.get_property_sets()}.get(
        ident_pset_name)
    attribute_names = list()
    if predefined_pset:
        attribute_names = [a.name for a in predefined_pset.get_attributes(filter=True)]
    object_tool.create_completer(attribute_names, main_window.get_ui().lineEdit_ident_attribute)


def add_shortcuts(object_tool: Type[Object], util: Type[tool.Util], search_tool: Type[Search],
                  main_window: Type[tool.MainWindow]):
    util.add_shortcut("Ctrl+X", main_window.get(), object_tool.delete_selection)
    util.add_shortcut("Ctrl+G", main_window.get(), object_tool.group_selection)
    util.add_shortcut("Ctrl+F", main_window.get(), lambda: search_object(search_tool, object_tool))


def search_object(search_tool: Type[Search], object_tool: Type[Object]):
    obj = search_tool.search_object()
    object_tool.select_object(obj)


def reset_tree(object_tool: Type[Object]):
    object_tool.get_properties().first_paint = True


def resize_columns(object_tool: Type[Object]):
    object_tool.resize_tree()


def create_object_info_widget(mode: int, object_tool: Type[Object], util: Type[tool.Util]):
    dialog = object_tool.oi_create_dialog()
    title = QCoreApplication.translate("ObjectInfo", "Object Info")
    dialog.setWindowTitle(util.get_window_title(title))
    widget = dialog.widget
    widget.button_add_ifc.pressed.connect(lambda: object_info_add_ifc(object_tool))
    widget.combo_box_pset.currentIndexChanged.connect(lambda: object_info_pset_changed(object_tool))
    object_tool.oi_fill_properties(mode=mode)
    object_tool.oi_update_dialog()
    if dialog.exec():
        object_info_accept(object_tool)


def object_info_accept(object_tool: Type[Object]):
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


def object_info_refresh(object_tool: Type[Object]):
    data_dict = object_tool.oi_get_values()
    object_tool.oi_set_values(data_dict)
    ident_value = data_dict["ident_value"]
    group = data_dict["is_group"]
    ident_filter = object_tool.get_active_object().ident_value if object_tool.oi_get_mode() == 1 else None
    if not object_tool.is_identifier_allowed(ident_value, ident_filter):
        object_tool.oi_set_ident_value_color("red")
    else:
        object_tool.oi_set_ident_value_color(QPalette().text())
    object_tool.oi_change_visibility_identifiers(group)


def object_info_pset_changed(object_tool: Type[Object]):
    object_tool.oi_update_attribute_combobox()


def object_info_add_ifc(object_tool: Type[Object]):
    object_tool.add_ifc_mapping("")


def load_context_menus(object_tool: Type[Object], util: Type[tool.Util]):
    object_tool.clear_context_menu_list()
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Copy"),
                                       lambda: create_object_info_widget(2, object_tool, util), True, False)
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Delete"),
                                       object_tool.delete_selection, True, True)
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Extend"),
                                       object_tool.expand_selection, True, True)
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Collapse"),
                                       object_tool.collapse_selection, True, True)
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Group"),
                                       lambda: create_group(object_tool), True, True)
    object_tool.add_context_menu_entry(lambda: QCoreApplication.translate("Object", "Info"),
                                       lambda: create_object_info_widget(1, object_tool, util), True, False)


def create_group(object_tool: Type[Object]):
    d = {
        "name":         QCoreApplication.translate("Object", "NewGroup"),
        "is_group":     True,
        "ifc_mappings": ["IfcGroup"]
    }
    is_allowed = object_tool.check_object_creation_input(d)
    if not is_allowed:
        return
    obj = object_tool.create_object(d, None, None)
    selected_objects = set(object_tool.get_selected_objects())
    object_tool.group_objects(obj, selected_objects)


def create_context_menu(pos: QPoint, object_tool: Type[Object]):
    menu = object_tool.create_context_menu()
    menu_pos = object_tool.get_object_tree().viewport().mapToGlobal(pos)
    menu.exec(menu_pos)


def refresh_object_tree(object_tool: Type[Object], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    logging.debug(f"Repaint Object Widget")
    load_objects(object_tool, project_tool)
    # object_tool.autofit_tree()


def load_objects(object_tool: Type[Object], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter_objects=True)
    object_tree: QTreeWidget = object_tool.get_object_tree()
    object_tool.fill_object_tree(set(root_objects), object_tree.invisibleRootItem())


def item_changed(item: QTreeWidgetItem, object_tool: Type[Object]):
    object_tool.update_check_state(item)
    pass


def item_selection_changed(object_tool: Type[Object], property_set_tool: Type[PropertySet]):
    selected_items = object_tool.get_selected_items()
    if len(selected_items) == 1:
        obj = object_tool.get_object_from_item(selected_items[0])
        object_tool.set_active_object(obj)
        property_set_tool.update_completer(obj)
        property_set_tool.set_enabled(True)
        refresh_property_set_table(property_set_tool, object_tool)
    else:
        property_set_tool.clear_table()
        property_set_tool.set_enabled(False)


def item_dropped_on(pos: QPoint, object_tool: Type[Object]):
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


def add_object_clicked(object_tool: Type[Object], project: Type[Project],
                       property_set: Type[tool.PropertySet], predefined_property_set: Type[tool.PredefinedPropertySet],
                       popup: Type[tool.Popups]):
    object_infos = object_tool.get_object_infos()
    is_allowed = object_tool.check_object_creation_input(object_infos)
    if not is_allowed:
        return

    pset_name = object_infos["ident_pset_name"]
    pset_dict = {p.name: p for p in predefined_property_set.get_property_sets()}

    connect_predefined_pset = False
    if pset_name in pset_dict:
        connect_predefined_pset = popup.request_property_set_merge(pset_name, 1)
        if connect_predefined_pset is None:
            return

    if connect_predefined_pset:
        parent = pset_dict.get(pset_name)
    else:
        parent = None

    pset = property_set.create_property_set(pset_name, None, parent)
    attribute_name = object_infos["ident_attribute_name"]
    attribute: SOMcreator.Attribute = {a.name: a for a in pset.get_attributes(filter=True)}.get(attribute_name)

    if not attribute:
        attribute = SOMcreator.Attribute(pset, attribute_name, [object_infos["ident_value"]],
                                         SOMcreator.value_constants.LIST)
    else:
        attribute.value = [object_infos["ident_value"]]

    object_tool.create_object(object_infos, pset, attribute)
    refresh_object_tree(object_tool, project)
