from __future__ import annotations

import SOMcreator
from som_gui.core import property_set_window as property_set_window_core
from typing import TextIO, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window.ui import PropertySetWindow


def open_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    if not predefined_pset.get_window():
        dialog = predefined_pset.create_window()
        predefined_pset.connect_triggers(dialog)
    window = predefined_pset.get_window()
    window.show()


def close_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    predefined_pset.close_window()


def pset_context_menu(pos, predefined_pset: Type[tool.PredefinedPropertySet],
                      property_set: Type[tool.PropertySet]):
    functions = [
        ["Löschen", predefined_pset.delete_selected_property_set],
        ["Umbenennen", predefined_pset.rename_selected_property_set],
        ["Hinzufügen", predefined_pset.create_property_set],
    ]
    list_widget = predefined_pset.get_pset_list_widget()
    property_set.create_context_menu(list_widget.mapToGlobal(pos), functions)


def pset_selection_changed(predefined_pset: Type[tool.PredefinedPropertySet]):
    property_set = predefined_pset.get_selected_property_set()
    predefined_pset.set_active_property_set(property_set)
    repaint_object_list(predefined_pset)


def pset_double_clicked(item, property_set: Type[tool.PropertySet],
                        property_set_window: Type[tool.PropertySetWindow], attribute_table: Type[tool.AttributeTable]):
    pset = property_set.get_property_set_from_item(item)
    property_set_window_core.open_pset_window(pset, property_set_window, attribute_table)


def object_context_menu(pos, predefined_pset: Type[tool.PredefinedPropertySet],
                        property_set: Type[tool.PropertySet]):
    functions = [
        ["Löschen", predefined_pset.delete_selected_objects],
        ["Verknüpfung entfernen", predefined_pset.remove_selected_links],
    ]
    table_widget = predefined_pset.get_object_table_widget()
    property_set.create_context_menu(table_widget.mapToGlobal(pos), functions)


def object_double_clicked(predefined_pset: Type[tool.PredefinedPropertySet],
                          property_set: Type[tool.PropertySet], object_tool: Type[tool.Object]):
    item = predefined_pset.get_object_table_widget().selectedItems()[0]
    pset = property_set.get_property_set_from_item(item)
    predefined_pset.close_window()

    obj = pset.object
    obj_item = object_tool.get_item_from_object(obj)
    object_tool.select_object(obj)
    object_tool.expand_to_item(obj_item)
    property_set.select_property_set(pset)


def name_edit_started(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = True


def name_edit_stopped(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = False


def pset_data_changed(item, property_set: Type[tool.PropertySet]):
    pset = property_set.get_property_set_from_item(item)
    pset.name = item.text()


#################################################################################
# PAINT EVENTS

def repaint_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    repaint_pset_list(predefined_pset)
    repaint_object_list(predefined_pset)
    pass


def repaint_object_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    property_set = predefined_pset.get_active_property_set()
    table_widget = predefined_pset.get_object_table_widget()

    if property_set is None:
        predefined_pset.clear_object_table()
        return
    predefined_property_sets = set(property_set.children)
    existing_property_sets = predefined_pset.get_existing_psets_in_table_widget(table_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)

    predefined_pset.remove_property_sets_from_table_widget(delete_property_sets, table_widget)
    predefined_pset.add_objects_to_table_widget(sorted(add_property_sets, key=lambda p: p.object.name),
                                                table_widget)

    table_widget.resizeColumnToContents(0)
    predefined_pset.update_object_widget()


def repaint_pset_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    if predefined_pset.is_edit_mode_active():
        return
    predefined_pset.get_pset_list_widget()
    predefined_property_sets = set(predefined_pset.get_property_sets())
    list_widget = predefined_pset.get_pset_list_widget()
    existing_property_sets = predefined_pset.get_existing_psets_in_list_widget(list_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)
    predefined_pset.remove_property_sets_from_list_widget(delete_property_sets, list_widget)
    predefined_pset.add_property_sets_to_widget(sorted(add_property_sets), list_widget)
    predefined_pset.update_pset_widget()


def add_compare_widget(pset_compare: Type[tool.PredefinedPropertySetCompare],
                       attribute_compare: Type[tool.AttributeCompare],
                       compare_window: Type[tool.CompareWindow]):
    compare_window.add_tab("Predefined Pset", pset_compare.get_widget,
                           lambda p0, p1: init_compare_window(p0, p1, pset_compare, attribute_compare),
                           pset_compare,
                           lambda file: export_compare(file, pset_compare, attribute_compare))


def init_compare_window(project0: SOMcreator.Project, project1: SOMcreator.Project,
                        pset_compare: Type[tool.PredefinedPropertySetCompare],
                        attribute_compare: Type[tool.AttributeCompare]):
    widget = pset_compare.get_widget()
    pset_tree = attribute_compare.get_pset_tree(widget)
    value_table = attribute_compare.get_value_table(widget)
    info_table = attribute_compare.get_info_table(widget)
    pset_compare.create_tree_selection_trigger(widget)

    psets0, psets1 = project0.get_predefined_psets(filter=False), project1.get_predefined_psets(filter=False)
    pset_compare.set_predefined_psets(psets0, psets1)

    pset_list = pset_compare.create_pset_list()
    for pset0, pset1 in [x for x in pset_list if not None in x]:
        attribute_compare.compare_property_sets(pset0, pset1)


    header_labels = [attribute_compare.get_header_name_from_project(project0),
                     attribute_compare.get_header_name_from_project(project1)]
    attribute_compare.set_header_labels([pset_tree], [value_table], header_labels)
    attribute_compare.set_header_labels([], [info_table], ["Name"] + header_labels)


    attribute_compare.fill_pset_tree(pset_tree, pset_compare.get_pset_lists(), True)
    attribute_compare.add_attributes_to_pset_tree(pset_tree, True)
    root = pset_tree.invisibleRootItem()
    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))


def export_compare(file: TextIO, pset_compare: Type[tool.PredefinedPropertySetCompare],
                   attribute_compare: Type[tool.AttributeCompare]):
    file.write("\nPREDEFINED PROPERTYSETS\n\n")
    attribute_compare.export_pset_differences(file, pset_compare.get_pset_lists(), True)
