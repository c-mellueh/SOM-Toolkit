from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF

import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.view import ui as ui_view
import SOMcreator
from SOMcreator.constants import json_constants
from som_gui.aggregation_window.module.view.constants import AGGREGATIONSCENES

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.view.prop import ViewProperties


def loop_name(name, names, index: int):
    new_name = f"{name}_{str(index).zfill(2)}"
    if new_name in names:
        index += 1
        return loop_name(name, names, index)
    return new_name


class View(som_gui.aggregation_window.core.tool.View):
    @classmethod
    def get_properties(cls) -> ViewProperties:
        return som_gui.ViewProperties

    @classmethod
    def get_scene_index(cls, scene: str | ui_view.AggregationScene) -> int:
        if isinstance(scene, str):
            return cls.get_properties().scene_name_list.index(scene)
        if isinstance(scene, ui_view.AggregationScene):
            return cls.get_properties().scene_list.index(scene)
        raise TypeError(f"type {type(scene)} not supported for function 'get_scene_index'")

    @classmethod
    def get_scene_by_name(cls, scene_name: str) -> ui_view.AggregationScene:
        return cls.get_properties().scene_list[cls.get_scene_index(scene_name)]

    @classmethod
    def create_view(cls) -> ui_view.AggregationView:
        view = ui_view.AggregationView()
        cls.get_properties().aggregation_view = view
        return view

    @classmethod
    def create_scene(cls, scene_name: str) -> tuple[ui_view.AggregationScene, str]:
        if scene_name in cls.get_scene_names():
            scene_name = loop_name(scene_name, cls.get_scene_names(), 0)
        scene = ui_view.AggregationScene()
        cls.get_properties().scene_name_list.append(scene_name)
        cls.get_properties().scene_list.append(scene)
        cls.get_properties().node_list.append(set())
        cls.get_properties().import_list.append(list())
        return scene, scene_name

    @classmethod
    def create_scene_dict(cls, proj: SOMcreator.Project, plugin_dict: dict) -> None:
        if not plugin_dict:
            return

        aggregation_ref = {aggregation.uuid: aggregation for aggregation in proj.get_all_aggregations()}
        import_scene_dict = plugin_dict.get(AGGREGATIONSCENES)

        if import_scene_dict is None:
            logging.warning(
                f"SOMJson was written in OLD version. Please open with SOM-Toolkit v2.11.3 and save it as new version.")
            return

        existing_scene_names = cls.get_properties().scene_name_list
        for scene_name, node_dict in import_scene_dict.items():
            if isinstance(node_dict[json_constants.NODES], list):
                logging.warning(
                    f"SOMJson was written in OLD version. Please open with SOM-Toolkit v2.11.3 and save it as new version.")
                return
            if scene_name not in existing_scene_names:
                scene, scene_name = cls.create_scene(scene_name)

            scene_id = cls.get_scene_index(scene_name)
            for aggregation_uuid, pos in node_dict["Nodes"].items():
                aggregation_tuple = (aggregation_ref[aggregation_uuid], QPointF(pos[0], pos[1]))
                cls.get_properties().import_list[scene_id].append(aggregation_tuple)

    @classmethod
    def get_scene_names(cls) -> list[str]:
        return cls.get_properties().scene_name_list

    @classmethod
    def get_active_scene(cls):
        scene = cls.get_properties().active_scene
        if scene is None:
            cls.create_scene("Undefined")
        return cls.get_properties().active_scene

    @classmethod
    def activate_scene(cls, scene: ui_view.AggregationScene):
        cls.get_properties().aggregation_view.setScene(scene)
        cls.get_properties().active_scene = scene

    @classmethod
    def set_cursor(cls, cursor_style):
        cls.get_properties().aggregation_view.viewport().setCursor(cursor_style)

    @classmethod
    def get_hovered_node(cls):
        scene = cls.get_active_scene()

    @classmethod
    def add_node_to_scene(cls, node, scene: ui_view.AggregationScene):
        scene.addItem(node)
        scene_index = cls.get_scene_index(scene)
        cls.get_properties().node_list[scene_index].add(node)

    @classmethod
    def clean_import_list_for_scene(cls, scene: ui_view.AggregationScene):
        index = cls.get_scene_index(scene)
        cls.get_properties().import_list[index] = list()
