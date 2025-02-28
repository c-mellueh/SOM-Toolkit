from __future__ import annotations

from typing import TYPE_CHECKING, Type, Callable
import logging
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QStandardItemModel
from ifcopenshell.util.unit import unit_names, prefixes
from som_gui.module.attribute.constants import (
    UNITS_SECTION,
    ALLOWED_UNITS,
    ALLOWED_PREFIXES,
)
import SOMcreator

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.attribute import ui


def add_basic_attribute_data(attribute_tool: Type[tool.Attribute]):
    """
    defines Data which every Attribute needs. The Data is stored in a dictionary with getter and setter functions.
    You can use set_attribute_data_by_dict to fill an Attribute with values like name, data_type,etc...
    """
    attribute_tool.add_attribute_data_value(
        "name", lambda a: a.name, lambda v, a: setattr(a, "name", v)
    )
    attribute_tool.add_attribute_data_value(
        "data_type", lambda a: a.data_type, lambda v, a: setattr(a, "data_type", v)
    )
    attribute_tool.add_attribute_data_value(
        "value_type", lambda a: a.value_type, lambda v, a: setattr(a, "value_type", v)
    )
    attribute_tool.add_attribute_data_value(
        "values", lambda a: a.value, lambda v, a: setattr(a, "value", v)
    )
    attribute_tool.add_attribute_data_value(
        "description",
        lambda a: a.description,
        lambda v, a: setattr(a, "description", v),
    )
    attribute_tool.add_attribute_data_value(
        "optional", lambda a: a.is_optional(True), lambda v, a: a.set_optional(v)
    )
    attribute_tool.add_attribute_data_value(
        "inherit_value",
        lambda a: a.child_inherits_values,
        lambda v, a: setattr(a, "child_inherits_values", v),
    )
    attribute_tool.add_attribute_data_value(
        "unit", lambda a: a.unit, lambda v, a: setattr(a, "unit", v)
    )


# Attribute Compare


def add_attribute_compare_widget(
    attribute_compare: Type[tool.AttributeCompare],
    compare_window: Type[tool.CompareWindow],
):
    """
    add Attribute-Tab to CompareWidget
    """
    from som_gui.module.attribute import trigger

    name_getter = lambda: QCoreApplication.translate("Compare", "Attributes")
    compare_window.add_tab(
        name_getter,
        attribute_compare.create_widget,
        trigger.init_attribute_compare,
        attribute_compare,
        trigger.export_attribute_differences,
    )


def create_compare_widget(
    project0, project1, attribute_compare: Type[tool.AttributeCompare]
):
    """
    Sets up the Attribute Compare Widget to function properly
    """
    # Define Projects
    attribute_compare.set_projects(
        project0, project1
    )  # defines which projects will be compared

    # Create widget
    widget = attribute_compare.create_widget()

    # get UI-elements
    object_tree_widget = attribute_compare.get_object_tree(widget)
    pset_tree = attribute_compare.get_pset_tree(widget)
    value_table = attribute_compare.get_value_table(widget)
    info_table = attribute_compare.get_info_table(widget)

    # fill ObjectTree with objects
    attribute_compare.create_object_lists()
    attribute_compare.fill_object_tree(object_tree_widget, add_missing=True)

    # define and set header labels
    header_labels = [
        attribute_compare.get_header_name_from_project(project0),
        attribute_compare.get_header_name_from_project(project1),
    ]
    attribute_compare.set_header_labels(
        [object_tree_widget, pset_tree], [value_table], header_labels
    )
    attribute_compare.set_header_labels([], [info_table], ["Name"] + header_labels)

    # Add Color
    root = object_tree_widget.invisibleRootItem()
    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))

    # Create Triggers
    attribute_compare.create_tree_selection_trigger(widget)


def export_attribute_differences(file, attribute_compare: Type[tool.AttributeCompare]):
    """
    Write All found differences between Attributes in file
    """
    objects0: list[SOMcreator.SOMClass] = attribute_compare.get_missing_objects(0)
    objects1: list[SOMcreator.SOMClass] = attribute_compare.get_missing_objects(1)
    title = QCoreApplication.translate("Compare", "ATTRIBUTE COMPARISON")
    file.write(f"\n{title}\n\n")

    for obj in sorted(objects0, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was deleted").format(
            obj, obj.ident_value
        )
        file.write(f"{text}\n")

    for obj in sorted(objects1, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was added").format(
            obj, obj.ident_value
        )

        file.write(f"{text}\n")

    if objects0 or objects1:
        file.write("\n\n")

    attribute_compare.export_object_differences(file)


def activate_object_in_compare_tree(
    widget: ui.AttributeWidget, attribute_compare: Type[tool.AttributeCompare]
):
    """
    Selection handling of Object Tree in Attribute Compare Widget
    """
    attribute_compare.clear_table(attribute_compare.get_info_table(widget))
    attribute_compare.clear_table(attribute_compare.get_value_table(widget))
    obj = attribute_compare.get_selected_entity(
        attribute_compare.get_object_tree(widget)
    )
    tree = attribute_compare.get_pset_tree(widget)
    pset_list = attribute_compare.get_pset_list(obj)
    attribute_compare.fill_pset_tree(tree, pset_list, add_missing=True)
    attribute_compare.add_attributes_to_pset_tree(tree, True)
    root = tree.invisibleRootItem()

    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))


def pset_tree_selection_changed(
    widget: ui.AttributeWidget, attribute_compare: Type[tool.AttributeCompare]
):
    """
    Selection Handling of PSetTree in Attribute Compare Widget
    """
    item = attribute_compare.get_selected_item(attribute_compare.get_pset_tree(widget))
    entity0, entity1 = attribute_compare.get_entities_from_item(item)
    attribute_compare.style_table(attribute_compare.get_value_table(widget))
    table = attribute_compare.get_info_table(widget)
    attribute_compare.clear_table(table)

    if isinstance(entity0 or entity1, SOMcreator.PropertySet):
        attribute_compare.fill_value_table_pset(widget)
        attribute_compare.fill_table(
            table, attribute_compare.get_pset_info_list(), (entity0, entity1)
        )
    else:
        attribute_compare.fill_value_table(
            attribute_compare.get_value_table(widget), entity0 or entity1
        )
        attribute_compare.fill_table(
            table, attribute_compare.get_attribute_info_list(), (entity0, entity1)
        )

    attribute_compare.style_table(table, 1)
    attribute_compare.style_table(attribute_compare.get_value_table(widget))


#### Settings Window


def fill_unit_settings(
    widget: ui.UnitSettings,
    attribute: Type[tool.Attribute],
    appdata: Type[tool.Appdata],
    util: Type[tool.Util],
):
    attribute.set_unit_settings_widget(widget)

    all_units = [un.capitalize() for un in unit_names]
    allowed_units = attribute.get_allowed_units(appdata)
    util.fill_list_widget_with_checkstate(
        widget.ui.list_units, allowed_units, all_units
    )

    all_prefixes = [pf.capitalize() for pf in prefixes.keys()]
    allowed_prefixes = attribute.get_allowed_unit_prefixes(appdata)

    util.fill_list_widget_with_checkstate(
        widget.ui.list_prefixes, allowed_prefixes, all_prefixes
    )


def unit_settings_accepted(
    attribute: Type[tool.Attribute], appdata: Type[tool.Appdata]
):
    widget = attribute.get_unit_settings_widget()
    allowed_units = attribute.get_checked_texts_from_list_widget(widget.ui.list_units)
    appdata.set_setting(UNITS_SECTION, ALLOWED_UNITS, allowed_units)

    allowed_prefixes = attribute.get_checked_texts_from_list_widget(
        widget.ui.list_prefixes
    )
    appdata.set_setting(UNITS_SECTION, ALLOWED_PREFIXES, allowed_prefixes)


def update_unit_combobox(
    cb: ui.UnitComboBox, attribute: Type[tool.Attribute], appdata: Type[tool.Appdata]
):
    logging.debug(f"Update unit combobox")
    model: QStandardItemModel = cb.model()
    tree_view = cb.tree_view
    allowed_units = attribute.get_allowed_units(appdata)
    allowed_prefixes = attribute.get_allowed_unit_prefixes(appdata)
    for row in range(model.rowCount()):
        item = model.item(row)
        index = item.index()
        hide_item = item.text() not in allowed_units
        tree_view.setRowHidden(row, index.parent(), hide_item)

        for child_row in range(item.rowCount()):
            child_item = item.child(child_row)
            hide_item = child_item.text() not in allowed_prefixes
            tree_view.setRowHidden(child_row, index, hide_item)
