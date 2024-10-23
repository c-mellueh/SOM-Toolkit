from __future__ import annotations

from typing import TYPE_CHECKING, Type
import SOMcreator
from PySide6.QtCore import QCoreApplication

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.attribute import ui

def add_basic_attribute_data(attribute_tool: Type[tool.Attribute]):
    attribute_tool.add_attribute_data_value("name", attribute_tool.get_attribute_name,
                                            attribute_tool.set_attribute_name)
    attribute_tool.add_attribute_data_value("data_type", attribute_tool.get_attribute_data_type,
                                            attribute_tool.set_attribute_data_type)
    attribute_tool.add_attribute_data_value("value_type", attribute_tool.get_attribute_value_type,
                                            attribute_tool.set_attribute_value_type)
    attribute_tool.add_attribute_data_value("values", attribute_tool.get_attribute_values,
                                            attribute_tool.set_attribute_values)
    attribute_tool.add_attribute_data_value("description", attribute_tool.get_attribute_description,
                                            attribute_tool.set_attribute_description)
    attribute_tool.add_attribute_data_value("optional", attribute_tool.is_attribute_optional,
                                            attribute_tool.set_attribute_optional)
    attribute_tool.add_attribute_data_value("inherit_value", attribute_tool.get_inherit_state,
                                            attribute_tool.set_inherit_state)


def add_attribute_compare_widget(attribute_compare: Type[tool.AttributeCompare],
                                 compare_window: Type[tool.CompareWindow]):
    from som_gui.module.attribute import trigger
    name_getter = lambda: QCoreApplication.translate("Compare", "Attributes")
    compare_window.add_tab(name_getter, attribute_compare.create_widget, trigger.init_attribute_compare,
                           attribute_compare, trigger.export_attribute_differences)


def export_attribute_differences(file, attribute_compare: Type[tool.AttributeCompare]):
    objects0: list[SOMcreator.Object] = attribute_compare.get_missing_objects(0)
    objects1: list[SOMcreator.Object] = attribute_compare.get_missing_objects(1)
    title = QCoreApplication.translate("Compare", "ATTRIBUTE COMPARISON")
    file.write(f"\n{title}\n\n")

    for obj in sorted(objects0, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was deleted").format(obj, obj.ident_value)
        file.write(f"{text}\n")

    for obj in sorted(objects1, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was added").format(obj, obj.ident_value)

        file.write(f"{text}\n")

    if objects0 or objects1:
        file.write("\n\n")

    attribute_compare.export_object_differences(file)


def init_attribute_compare(project0, project1, attribute_compare: Type[tool.AttributeCompare]):
    attribute_compare.set_projects(project0, project1)
    attribute_compare.create_object_lists()
    widget = attribute_compare.create_widget()
    object_tree_widget = attribute_compare.get_object_tree(widget)
    pset_tree = attribute_compare.get_pset_tree(widget)
    value_table = attribute_compare.get_value_table(widget)
    info_table = attribute_compare.get_info_table(widget)
    attribute_compare.fill_object_tree(object_tree_widget, add_missing=True)
    root = object_tree_widget.invisibleRootItem()
    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))

    header_labels = [attribute_compare.get_header_name_from_project(project0),
                     attribute_compare.get_header_name_from_project(project1)]
    attribute_compare.set_header_labels([object_tree_widget, pset_tree], [value_table], header_labels)
    attribute_compare.set_header_labels([], [info_table], ["Name"] + header_labels)

    attribute_compare.create_tree_selection_trigger(widget)

def object_tree_selection_changed(widget: ui.AttributeWidget,
                                  attribute_compare: Type[tool.AttributeCompare]):
    attribute_compare.clear_table(attribute_compare.get_info_table(widget))
    attribute_compare.clear_table(attribute_compare.get_value_table(widget))
    obj = attribute_compare.get_selected_entity(attribute_compare.get_object_tree(widget))
    tree = attribute_compare.get_pset_tree(widget)
    pset_list = attribute_compare.get_pset_list(obj)
    attribute_compare.fill_pset_tree(tree, pset_list, add_missing=True)
    attribute_compare.add_attributes_to_pset_tree(tree, True)
    root = tree.invisibleRootItem()


    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))


def pset_tree_selection_changed(widget: ui.AttributeWidget, attribute_compare: Type[tool.AttributeCompare]):
    item = attribute_compare.get_selected_item(attribute_compare.get_pset_tree(widget))
    entity0, entity1 = attribute_compare.get_entities_from_item(item)
    attribute_compare.style_table(attribute_compare.get_value_table(widget))
    table = attribute_compare.get_info_table(widget)
    attribute_compare.clear_table(table)

    if isinstance(entity0 or entity1, SOMcreator.PropertySet):
        attribute_compare.fill_value_table_pset(widget)
        attribute_compare.fill_table(table, attribute_compare.get_pset_info_list(), (entity0, entity1))
    else:
        attribute_compare.fill_value_table(attribute_compare.get_value_table(widget), entity0 or entity1)
        attribute_compare.fill_table(table, attribute_compare.get_attribute_info_list(), (entity0, entity1))

    attribute_compare.style_table(table, 1)
    attribute_compare.style_table(attribute_compare.get_value_table(widget))