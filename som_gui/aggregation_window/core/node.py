from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import View, Window, Node
from SOMcreator.classes import Aggregation


def add_node(view: Type[View], node: Type[Node]):
    from som_gui.tool import Project as project
    proj = project.get()

    aggregations = list(proj.get_all_aggregations())
    aggregation = aggregations[0]
    print(aggregation)
    scene = view.get_active_scene()
    new_node = node.create_node(aggregation)
    node.add_node_to_scene(new_node, scene)
