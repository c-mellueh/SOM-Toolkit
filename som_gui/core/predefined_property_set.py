from __future__ import annotations
from som_gui.core import property_set_window as property_set_window_core
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_set_window.ui import PropertySetWindow


def create_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    if not predefined_pset.get_window():
        dialog = predefined_pset.create_predefined_pset_window()
        predefined_pset.connect_window_triggers(dialog)
    window = predefined_pset.get_window()
    window.show()


def predef_object_double_clicked(predefined_pset: Type[tool.PredefinedPropertySet],
                                 property_set: Type[tool.PropertySet], object_tool: Type[tool.Object]):
    item = predefined_pset.get_predefined_pset_inheritance_list().selectedItems()[0]
    pset = property_set.get_property_set_from_item(item)
    predefined_pset.close_predefined_pset_window()

    obj = pset.object
    obj_item = object_tool.get_item_from_object(obj)
    object_tool.select_object(obj)
    object_tool.expand_to_item(obj_item)
    property_set.select_property_set(pset)


def predef_selection_changed(predefined_pset: Type[tool.PredefinedPropertySet]):
    property_set = predefined_pset.get_selected_predef_property_set()
    predefined_pset.set_predef_property_set(property_set)
    repaint_predefined_pset_inheritance_list(predefined_pset)


def predefined_pset_item_changed(item, property_set: Type[tool.PropertySet]):
    pset = property_set.get_property_set_from_item(item)
    pset.name = item.text()


def predefined_pset_window_context_menu(pos, predefined_pset: Type[tool.PredefinedPropertySet],
                                        property_set: Type[tool.PropertySet]):
    functions = [
        ["Löschen", predefined_pset.delete_predefined_pset],
        ["Umbenennen", predefined_pset.rename_predefined_pset],
        ["Hinzufügen", predefined_pset.add_predefined_pset],
    ]
    list_widget = predefined_pset.get_predefine_pset_list_widget()
    property_set.create_context_menu(list_widget.mapToGlobal(pos), functions)


def pset_item_double_clicked(item, property_set: Type[tool.PropertySet],
                             property_set_window: Type[tool.PropertySetWindow]):
    pset = property_set.get_property_set_from_item(item)
    property_set_window_core.open_pset_window(pset, property_set_window)


def repaint_predefined_pset_inheritance_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    property_set = predefined_pset.get_active_predefined_pset()
    list_widget = predefined_pset.get_predefined_pset_inheritance_list()

    if property_set is None:
        list_widget.clear()
        return
    predefined_property_sets = set(property_set.children)
    existing_property_sets = predefined_pset.get_existing_psets_in_list(list_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)
    predefined_pset.remove_property_sets_from_list(delete_property_sets, list_widget)
    predefined_pset.add_property_sets_to_inheritance_list(sorted(add_property_sets, key=lambda p: p.name),
                                                          list_widget)
    predefined_pset.update_predefined_pset_inheritance_list()


def repaint_predefined_pset_list(predefined_pset: Type[tool.PredefinedPropertySet]):
    if predefined_pset.predefined_pset_list_is_editing():
        return
    predefined_pset.get_predefine_pset_list_widget()
    predefined_property_sets = set(predefined_pset.get_predefined_psets())
    list_widget = predefined_pset.get_predefine_pset_list_widget()
    existing_property_sets = predefined_pset.get_existing_psets_in_list(list_widget)
    delete_property_sets = existing_property_sets.difference(predefined_property_sets)
    add_property_sets = sorted(predefined_property_sets.difference(existing_property_sets), key=lambda p: p.name)
    predefined_pset.remove_property_sets_from_list(delete_property_sets, list_widget)
    predefined_pset.add_property_sets_to_list(sorted(add_property_sets), list_widget)
    predefined_pset.update_predefined_pset_list()


def repaint_predefined_pset_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    repaint_predefined_pset_list(predefined_pset)
    repaint_predefined_pset_inheritance_list(predefined_pset)
    pass


def predef_edit_started(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = True


def predef_edit_stopped(predefined_pset: Type[tool.PredefinedPropertySet]):
    props = predefined_pset.get_properties()
    props.is_renaming_predefined_pset = False


def close_predefined_pset_window(predefined_pset: Type[tool.PredefinedPropertySet]):
    predefined_pset.close_predefined_pset_window()
