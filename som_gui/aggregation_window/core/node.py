from __future__ import annotations
from typing import TYPE_CHECKING, Type

import SOMcreator

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import View, Window, Node
    from som_gui import tool
from SOMcreator.classes import Aggregation
from som_gui.core import property_set_window as property_set_window_core


def add_node(view: Type[View], node: Type[Node]):
    from som_gui.tool import Project as project
    proj = project.get()

    aggregations = list(proj.get_all_aggregations())
    aggregation = aggregations[0]
    print(aggregation)
    scene = view.get_active_scene()
    new_node = node.create_node(aggregation)
    node.add_node_to_scene(new_node, scene)


def pset_tree_double_clicked(item, node: Type[Node], property_set_window: Type[tool.PropertySetWindow],
                             attribute: Type[tool.Attribute], attribute_table: Type[tool.AttributeTable]):
    linked_item = node.get_linked_item(item)
    active_attribute = None
    active_property_set = None
    if isinstance(linked_item, SOMcreator.Attribute):
        active_attribute = linked_item
        active_property_set = linked_item.property_set

    elif isinstance(linked_item, SOMcreator.PropertySet):
        active_property_set = linked_item

    if active_property_set is None:
        return

    window = property_set_window_core.open_pset_window(active_property_set, property_set_window, attribute_table)
    if active_attribute is None:
        return
    property_set_window_core.activate_attribute(active_attribute, window, attribute, property_set_window)
