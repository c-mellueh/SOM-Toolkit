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
    def create_scene(cls) -> ui_view.AggregationScene:
        scene = ui_view.AggregationScene()
        cls.get_properties().active_scene = scene
        return scene

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

        scene_dict = cls.get_properties().scene_dict

        for scene_name, node_dict in import_scene_dict.items():
            if isinstance(node_dict[json_constants.NODES], list):
                logging.warning(
                    f"SOMJson was written in OLD version. Please open with SOM-Toolkit v2.11.3 and save it as new version.")
                return
            if scene_name not in scene_dict:
                scene_dict[scene_name] = list()

            for uuid, position in node_dict[json_constants.NODES].items():
                aggregation = aggregation_ref[uuid]
                scene_dict[scene_name].append((aggregation, QPointF(*position)))

    @classmethod
    def get_scene_names(cls) -> list[str]:
        return sorted(cls.get_properties().scene_dict.keys())
