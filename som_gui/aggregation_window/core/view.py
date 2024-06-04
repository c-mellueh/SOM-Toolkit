from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool as aw_tool
    from som_gui import tool
    from PySide6.QtCore import QPointF

def import_positions(view: Type[aw_tool.View], project: Type[tool.Project]):
    proj = project.get()
    plugin_dict = proj.import_dict
    view.create_scene_dict(proj, plugin_dict)


def paint_event(view: Type[aw_tool.View], node: Type[aw_tool.Node], project: Type[tool.Project]):
    logging.debug("Paint View Event")
    scene = view.get_active_scene()
    scene_id = view.get_scene_index(scene)

    # Add Nodes from import_list
    for aggregation, position in view.get_properties().import_list[scene_id]:
        new_node = node.create_node(aggregation)
        view.add_node_to_scene(new_node, scene)
        node.set_node_pos(new_node, position)
    view.clean_import_list_for_scene(scene)

    # delete Nodes with deleted Aggregations
    nodes = view.get_nodes_in_scene(scene)
    existing_aggregations = list(project.get().get_all_aggregations())
    for existing_node in list(nodes):
        if existing_node.aggregation not in existing_aggregations:
            view.remove_node_from_scene(existing_node, scene)


def mouse_move_event(position: QPointF, view: Type[aw_tool.View]):
    last_pos = view.get_last_mouse_pos()
    mouse_mode = view.get_mouse_mode()

    if mouse_mode == 1:
        view.pan(last_pos, position)

    view.set_last_mouse_pos(position)


def mouse_press_event(position: QPointF, view: Type[aw_tool.View]):
    view.set_last_mouse_pos(position)
    item_under_mouse = view.get_item_under_mouse(position)
    if item_under_mouse is None:
        view.set_mouse_mode(1)


def mouse_release_event(view: Type[aw_tool.View]):
    view.set_last_mouse_pos(None)
    view.set_mouse_mode(0)
