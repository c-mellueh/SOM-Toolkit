from __future__ import annotations

from typing import TYPE_CHECKING, Type, Callable
import logging
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QStandardItemModel
from ifcopenshell.util.unit import unit_names, prefixes
from som_gui.module.property_.constants import (
    UNITS_SECTION,
    ALLOWED_UNITS,
    ALLOWED_PREFIXES,
)
import SOMcreator

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_ import ui


def add_basic_property_data(property_tool: Type[tool.Property]):
    """
    defines Data which every Property needs. The Data is stored in a dictionary with getter and setter functions.
    You can use set_property_data_by_dict to fill an Property with values like name, data_type,etc...
    """
    property_tool.add_property_data_value(
        "name", lambda a: a.name, lambda v, a: setattr(a, "name", v)
    )
    property_tool.add_property_data_value(
        "data_type", lambda a: a.data_type, lambda v, a: setattr(a, "data_type", v)
    )
    property_tool.add_property_data_value(
        "value_type", lambda a: a.value_type, lambda v, a: setattr(a, "value_type", v)
    )
    property_tool.add_property_data_value(
        "values",
        lambda a: a.allowed_values,
        lambda v, a: setattr(a, "allowed_values", v),
    )
    property_tool.add_property_data_value(
        "description",
        lambda a: a.description,
        lambda v, a: setattr(a, "description", v),
    )
    property_tool.add_property_data_value(
        "optional", lambda a: a.is_optional(True), lambda v, a: a.set_optional(v)
    )
    property_tool.add_property_data_value(
        "inherit_value",
        lambda a: a.child_inherits_values,
        lambda v, a: setattr(a, "child_inherits_values", v),
    )
    property_tool.add_property_data_value(
        "unit", lambda a: a.unit, lambda v, a: setattr(a, "unit", v)
    )


# Property Compare


def add_compare_widget(
    property_compare: Type[tool.PropertyCompare],
    compare_window: Type[tool.CompareWindow],
):
    """
    add Property-Tab to CompareWidget
    """
    from som_gui.module.property_ import trigger

    name_getter = lambda: QCoreApplication.translate("Compare", "Properties")
    compare_window.add_tab(
        name_getter,
        property_compare.create_widget,
        trigger.init_property_compare,
        property_compare,
        trigger.export_property_differences,
    )


def create_compare_widget(
    project0: SOMcreator.SOMProject,
    project1: SOMcreator.SOMProject,
    property_compare: Type[tool.PropertyCompare],
):
    """
    Sets up the Property Compare Widget to function properly
    """
    # Define Projects
    property_compare.set_projects(
        project0, project1
    )  # defines which projects will be compared

    # Create widget
    widget = property_compare.create_widget()

    # get UI-elements
    class_tree_widget = property_compare.get_class_tree(widget)
    pset_tree = property_compare.get_pset_tree(widget)
    value_table = property_compare.get_value_table(widget)
    info_table = property_compare.get_info_table(widget)

    # fill ClassTree with classes
    property_compare.create_class_lists()
    property_compare.fill_class_tree(class_tree_widget, add_missing=True)

    # define and set header labels
    header_labels = [
        property_compare.get_header_name_from_project(project0),
        property_compare.get_header_name_from_project(project1),
    ]
    property_compare.set_header_labels(
        [class_tree_widget, pset_tree], [value_table], header_labels
    )
    property_compare.set_header_labels([], [info_table], ["Name"] + header_labels)

    # Add Color
    root = class_tree_widget.invisibleRootItem()
    for child_index in range(root.childCount()):
        property_compare.style_tree_item(root.child(child_index))

    # Create Triggers
    property_compare.create_tree_selection_trigger(widget)


def export_differences(file, property_compare: Type[tool.PropertyCompare]):
    """
    Write All found differences between Properties in file
    """
    Classes_0: list[SOMcreator.SOMClass] = property_compare.get_missing_classes(0)
    classes_1: list[SOMcreator.SOMClass] = property_compare.get_missing_classes(1)
    title = QCoreApplication.translate("Compare", "PROPERTY COMPARISON")
    file.write(f"\n{title}\n\n")

    for som_class in sorted(Classes_0, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was deleted").format(
            som_class, som_class.ident_value
        )
        file.write(f"{text}\n")

    for som_class in sorted(classes_1, key=lambda x: x.name):
        text = QCoreApplication.translate("Compare", "{} ({}) was added").format(
            som_class, som_class.ident_value
        )

        file.write(f"{text}\n")

    if Classes_0 or classes_1:
        file.write("\n\n")

    property_compare.export_class_differences(file)


def activate_class_in_compare_tree(
    widget: ui.PropertyWidget, property_compare: Type[tool.PropertyCompare]
):
    """
    Selection handling of Class Tree in Property Compare Widget
    """
    property_compare.clear_table(property_compare.get_info_table(widget))
    property_compare.clear_table(property_compare.get_value_table(widget))
    cls = property_compare.get_selected_entity(property_compare.get_class_tree(widget))
    if not isinstance(cls, SOMcreator.SOMClass):
        return
    tree = property_compare.get_pset_tree(widget)
    pset_list = property_compare.get_pset_list(cls)
    property_compare.fill_pset_tree(tree, pset_list, add_missing=True)
    property_compare.add_properties_to_pset_tree(tree, True)
    root = tree.invisibleRootItem()

    for child_index in range(root.childCount()):
        property_compare.style_tree_item(root.child(child_index))


def pset_tree_selection_changed(
    widget: ui.PropertyWidget, property_compare: Type[tool.PropertyCompare]
):
    """
    Selection Handling of PSetTree in Property Compare Widget
    """
    item = property_compare.get_selected_item(property_compare.get_pset_tree(widget))
    entity0, entity1 = property_compare.get_entities_from_item(item)
    property_compare.style_table(property_compare.get_value_table(widget))
    table = property_compare.get_info_table(widget)
    property_compare.clear_table(table)
    target = entity0 or entity1

    if isinstance(target, SOMcreator.SOMPropertySet):
        property_compare.fill_value_table_pset(widget)
        property_compare.fill_table(
            table, property_compare.get_pset_info_list(), (entity0, entity1)
        )
    elif isinstance(target, SOMcreator.SOMProperty):
        property_compare.fill_value_table(
            property_compare.get_value_table(widget), target
        )
        property_compare.fill_table(
            table, property_compare.get_property_info_list(), (entity0, entity1)
        )

    property_compare.style_table(table, 1)
    property_compare.style_table(property_compare.get_value_table(widget))


#### Settings Window


def fill_unit_settings(
    widget: ui.UnitSettings,
    property_tool: Type[tool.Property],
    appdata: Type[tool.Appdata],
    util: Type[tool.Util],
):
    property_tool.set_unit_settings_widget(widget)

    all_units = [un.capitalize() for un in unit_names]
    allowed_units = property_tool.get_allowed_units(appdata)
    util.fill_list_widget_with_checkstate(
        widget.ui.list_units, allowed_units, all_units
    )

    all_prefixes = [pf.capitalize() for pf in prefixes.keys()]
    allowed_prefixes = property_tool.get_allowed_unit_prefixes(appdata)

    util.fill_list_widget_with_checkstate(
        widget.ui.list_prefixes, allowed_prefixes, all_prefixes
    )


def unit_settings_accepted(
    property_tool: Type[tool.Property], appdata: Type[tool.Appdata]
):
    widget = property_tool.get_unit_settings_widget()
    if not widget:
        return
    allowed_units = property_tool.get_checked_texts_from_list_widget(
        widget.ui.list_units
    )
    appdata.set_setting(UNITS_SECTION, ALLOWED_UNITS, allowed_units)

    allowed_prefixes = property_tool.get_checked_texts_from_list_widget(
        widget.ui.list_prefixes
    )
    appdata.set_setting(UNITS_SECTION, ALLOWED_PREFIXES, allowed_prefixes)


def update_unit_combobox(
    cb: ui.UnitComboBox, property_tool: Type[tool.Property], appdata: Type[tool.Appdata]
):
    logging.debug(f"Update unit combobox")
    model: QStandardItemModel = cb.mod
    tree_view = cb.tree_view
    allowed_units = property_tool.get_allowed_units(appdata)
    allowed_prefixes = property_tool.get_allowed_unit_prefixes(appdata)
    for row in range(model.rowCount()):
        item = model.item(row)
        index = item.index()
        hide_item = item.text() not in allowed_units
        tree_view.setRowHidden(row, index.parent(), hide_item)

        for child_row in range(item.rowCount()):
            child_item = item.child(child_row)
            hide_item = child_item.text() not in allowed_prefixes
            tree_view.setRowHidden(child_row, index, hide_item)
