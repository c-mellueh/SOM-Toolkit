from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool import PropertySet, Object
    from som_gui.module.property_set.ui import PropertySetWindow


def refresh_table(property_set_tool: Type[PropertySet], object_tool: Type[Object]):
    if object_tool.get_active_object() is not None:
        property_set_tool.set_enabled(True)
    else:
        property_set_tool.set_enabled(False)
    new_property_sets = property_set_tool.get_property_sets()
    existing_property_sets = property_set_tool.get_existing_psets_in_table()
    delete_property_sets = existing_property_sets.difference(new_property_sets)
    add_property_sets = new_property_sets.difference(existing_property_sets)
    property_set_tool.remove_property_sets_from_table(delete_property_sets)
    property_set_tool.add_property_sets_to_table(add_property_sets)
    table = property_set_tool.get_table()
    table.resizeColumnsToContents()


def pset_selection_changed(property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_selecte_property_set()
    print(f"PropertySet: {property_set}")
    property_set_tool.set_active_pset(property_set)


def table_double_clicked(property_set_tool: Type[PropertySet]):
    property_set = property_set_tool.get_selecte_property_set()
    property_set_tool.open_pset_window(property_set)
    pass


def repaint_pset_window(window: PropertySetWindow, property_set_tool: Type[PropertySet]):
    print(f"repaint")
    pass
