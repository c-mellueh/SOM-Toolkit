from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QTransform
import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.view import ui as ui_view
import SOMcreator
from SOMcreator.constants import json_constants
from som_gui.aggregation_window.module.view.constants import AGGREGATIONSCENES, SCENE_SIZE, SCENE_MARGIN

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.view.prop import ViewProperties
    from som_gui.aggregation_window.module.node import ui as ui_node


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
    def get_view(cls) -> ui_view.AggregationView:
        return cls.get_properties().aggregation_view

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
        scene.setSceneRect(QRectF(0, 0, SCENE_SIZE[0], SCENE_SIZE[1]))
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
            position_values = node_dict["Nodes"].values()
            x_values, y_values = zip(*position_values)
            x_min = min(x_values)
            y_min = min(y_values)
            for aggregation_uuid, pos in node_dict["Nodes"].items():
                x = SCENE_SIZE[0] / 2 - pos[0] + x_min
                y = SCENE_SIZE[1] / 2 - pos[1] + y_min
                print(x, y)
                aggregation_tuple = (aggregation_ref[aggregation_uuid], QPointF(x, y))
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
    def add_node_to_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene):
        scene.addItem(node)
        scene.addItem(node.header)
        scene.addItem(node.frame)
        scene_index = cls.get_scene_index(scene)
        cls.get_properties().node_list[scene_index].add(node)

    @classmethod
    def clean_import_list_for_scene(cls, scene: ui_view.AggregationScene):
        index = cls.get_scene_index(scene)
        cls.get_properties().import_list[index] = list()

    @classmethod
    def autofit_view(cls):
        def get_bounding_rect():
            items = scene.items()
            rects = [item.sceneBoundingRect() for item in items]
            top_left, bottom_right = zip(*[(br.topLeft(), br.bottomRight()) for br in rects if br is not None])
            tl_x, tl_y = zip(*[[tl.x(), tl.y()] for tl in top_left])
            br_x, br_y = zip(*[[br.x(), br.y()] for br in bottom_right])
            x_min, x_max = min(tl_x), max(br_x)
            y_min, y_max = min(tl_y), max(br_y)
            return QRectF(QPointF(x_min, y_min), QPointF(x_max, y_max))

        scene = cls.get_active_scene()
        view = cls.get_view()
        bounding_rect = get_bounding_rect()
        marg = SCENE_MARGIN
        view.fitInView(bounding_rect.adjusted(-marg, -marg, marg, marg),
                       aspectRadioMode=Qt.AspectRatioMode.KeepAspectRatio)

    @classmethod
    def get_nodes_in_scene(cls, scene: ui_view.AggregationScene):
        scene_index = cls.get_scene_index(scene)
        return cls.get_properties().node_list[scene_index]

    @classmethod
    def remove_node_from_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene):
        logging.debug(f"Delete Node {node.aggregation.name}")

        scene_index = cls.get_scene_index(scene)
        prop = cls.get_properties()
        prop.node_list[scene_index].remove(node)
        scene.removeItem(node.header)
        scene.removeItem(node.frame)
        scene.removeItem(node)
        node.deleteLater()

    @classmethod
    def get_last_mouse_pos(cls) -> QPointF | None:
        return cls.get_properties().last_mouse_pos

    @classmethod
    def set_last_mouse_pos(cls, mouse_pos: QPointF | None):
        cls.get_properties().last_mouse_pos = mouse_pos

    @classmethod
    def get_item_under_mouse(cls, position: QPointF):
        scene = cls.get_active_scene()
        return scene.itemAt(position, QTransform())

    @classmethod
    def set_mouse_mode(cls, mode: int):
        """
        mode: 0= None 1= pan, 2= drag
        """
        cls.get_properties().mouse_mode = mode

    @classmethod
    def get_mouse_mode(cls) -> int:
        """
        mode: 0= None 1= pan, 2= drag
        """
        return cls.get_properties().mouse_mode

    @classmethod
    def pan(cls, last_pos: QPointF, new_pos: QPointF):
        dif = new_pos - last_pos
        print(dif)
        view = cls.get_view()
        print(view.translate(dif.x(), dif.y()))
