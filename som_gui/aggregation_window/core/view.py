from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool as aw_tool
    from som_gui import tool


def import_positions(view: Type[aw_tool.View], project: Type[tool.Project]):
    proj = project.get()
    plugin_dict = proj.import_dict
    view.create_scene_dict(proj, plugin_dict)


def paint_event(view: Type[aw_tool.View], node: Type[aw_tool.Node]):
    add_aggregations_from_import_list(view, node)


def add_aggregations_from_import_list(view: Type[aw_tool.View], node: Type[aw_tool.Node]):
    scene = view.get_active_scene()
    scene_id = view.get_scene_index(scene)
    for aggregation, position in view.get_properties().import_list[scene_id]:
        new_node = node.create_node(aggregation)
        view.add_node_to_scene(new_node, scene)
        node.create_header(new_node, scene)
        node.create_frame(new_node, scene)
        node.set_node_pos(new_node, position)
    view.clean_import_list_for_scene(scene)
