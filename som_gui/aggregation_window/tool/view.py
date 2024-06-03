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
    def create_view(cls) -> ui_view.AggregationView:
        view = ui_view.AggregationView()
        cls.get_properties().aggregation_view = view
        return view

    @classmethod
    def create_scene(cls, scene_name: str) -> tuple[ui_view.AggregationScene, str]:
        if scene_name in cls.get_scene_names():
            scene_name = loop_name(scene_name, cls.get_scene_names(), 0)
        scene = ui_view.AggregationScene()
        cls.get_properties().scene_dict[scene_name] = scene
        cls.get_properties().aggregation_dict[scene_name] = list()
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

        aggregation_dict = cls.get_properties().aggregation_dict
        for scene_name, node_dict in import_scene_dict.items():
            if isinstance(node_dict[json_constants.NODES], list):
                logging.warning(
                    f"SOMJson was written in OLD version. Please open with SOM-Toolkit v2.11.3 and save it as new version.")
                return
            if scene_name not in aggregation_dict:
                scene, scene_name = cls.create_scene(scene_name)
                cls.get_properties().scene_dict[scene_name] = scene
                aggregation_dict[scene_name] = list()

            for uuid, position in node_dict[json_constants.NODES].items():
                aggregation = aggregation_ref[uuid]
                aggregation_dict[scene_name].append((aggregation, QPointF(*position)))

    @classmethod
    def get_scene_names(cls) -> list[str]:
        return sorted(cls.get_properties().aggregation_dict.keys())

    @classmethod
    def get_active_scene(cls):
        scene = cls.get_properties().active_scene
        if scene is None:
            cls.create_scene()
        return cls.get_properties().active_scene

    @classmethod
    def get_scene_dict(cls) -> dict[str, ui_view.AggregationScene]:
        return cls.get_properties().scene_dict

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
