from __future__ import annotations
from typing import Type, TYPE_CHECKING

import som_gui
from som_gui.core import attribute as attribute_core
from SOMcreator.constants.value_constants import RANGE
if TYPE_CHECKING:
    from som_gui.tool import PropertySet, Object, Attribute
    from som_gui.module.property_set.ui import PropertySetWindow


def refresh_table(property_set_tool: Type[PropertySet], object_tool: Type[Object]):
    if object_tool.get_active_object() is not None:
        property_set_tool.set_enabled(True)
    else:
        property_set_tool.set_enabled(False)
    new_property_sets = property_set_tool.get_property_sets()
    table = property_set_tool.get_table()

    existing_property_sets = property_set_tool.get_existing_psets_in_table(table)
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets, table)
    property_set_tool.add_property_sets_to_table(add_property_sets, table)
    table = property_set_tool.get_table()
    table.resizeColumnsToContents()


def pset_selection_changed(property_set_tool: Type[PropertySet], attribute_tool: Type[Attribute]):
    property_set = property_set_tool.get_selecte_property_set()
    property_set_tool.set_active_property_set(property_set)
    attribute_core.refresh_attribute_table(som_gui.MainUi.ui.table_attribute, attribute_tool)


def table_double_clicked(property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_selecte_property_set()
    property_set_tool.open_pset_window(property_set)
    pass


def repaint_pset_window(window: PropertySetWindow, property_set_tool: Type[PropertySet],
                        attribute_tool: Type[Attribute]):
    pset = property_set_tool.get_property_set_from_window(window)
    attribute_core.refresh_attribute_table(window.widget.table_widget, attribute_tool)
    attribute_name = property_set_tool.pw_get_attribute_name(window)
    if attribute_name in [a.name for a in pset.attributes]:
        property_set_tool.pw_set_add_button_text("Update", window)
    else:
        property_set_tool.pw_set_add_button_text("Hinzufügen", window)

    pass


def add_attribute_button_clicked(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    print(f"ADD")
    value_type = window.widget.combo_type.currentText()
    if value_type == RANGE:
        property_set_tool.pw_add_value_line(2, window)
    else:
        property_set_tool.pw_add_value_line(1, window)
