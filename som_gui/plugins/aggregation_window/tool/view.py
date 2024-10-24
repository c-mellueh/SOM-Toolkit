from __future__ import annotations

import os
import logging
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QPointF, QRectF, Qt, QPoint
from PySide6.QtGui import QTransform, QImage, QPainter, QCursor
from PySide6.QtWidgets import QApplication, QFileDialog, QGraphicsView

import SOMcreator
from SOMcreator.datastructure.som_json import NODES
from som_gui.plugins.aggregation_window.module.view.constants import AGGREGATIONSCENES, SCENE_SIZE, SCENE_MARGIN
from som_gui.plugins.aggregation_window.module.node import ui as ui_node
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.module.view import ui as ui_view
from som_gui.plugins.aggregation_window.module.view import trigger

import som_gui.plugins.aggregation_window.core.tool

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.view.prop import ViewProperties
    from som_gui.plugins.aggregation_window.module.connection import ui as ui_connection


def loop_name(name, names, index: int) -> str:
    new_name = f"{name}_{str(index).zfill(2)}"
    if new_name in names:
        index += 1
        return loop_name(name, names, index)
    return new_name


class View(som_gui.plugins.aggregation_window.core.tool.View):
    @classmethod
    def create_aggregation_scenes_dict(cls, agrgegation_uuid_dict: dict):
        main_dict = {"AggregationScenes": dict()}
        aggregation_scenes_dict = main_dict["AggregationScenes"]
        for scene_index, scene in enumerate(cls.get_all_scenes()):
            scene_name = cls.get_scene_name(scene)
            aggregation_scenes_dict[scene_name] = dict()

            position_list = cls.get_aggregations_in_scene(scene)
            node_dict = dict()
            for aggregation, pos in position_list:
                if aggregation not in agrgegation_uuid_dict:
                    continue  # object and aggregation were deleted without refreshing the widget
                node_dict[agrgegation_uuid_dict[aggregation]] = [pos.x(), pos.y()]
            aggregation_scenes_dict[scene_name]["Nodes"] = node_dict
        return aggregation_scenes_dict

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
    def get_scene_by_name(cls, scene_name: str) -> ui_view.AggregationScene | None:
        if scene_name not in cls.get_properties().scene_name_list:
            return None
        return cls.get_properties().scene_list[cls.get_scene_index(scene_name)]

    @classmethod
    def get_scene_name(cls, scene: ui_view.AggregationScene) -> str | None:
        index = cls.get_scene_index(scene)
        if index is None:
            return None
        return cls.get_properties().scene_name_list[index]

    @classmethod
    def set_scene_name(cls, scene: ui_view.AggregationScene | int, name: str):
        if isinstance(scene, ui_view.AggregationScene):
            scene_index = cls.get_scene_index(scene)
        else:
            scene_index = scene
        cls.get_properties().scene_name_list[scene_index] = name

    @classmethod
    def set_view(cls, view: ui_view.AggregationView):
        cls.get_properties().aggregation_view = view
        return view

    @classmethod
    def create_scene(cls, scene_name: str) -> tuple[ui_view.AggregationScene, str]:
        if scene_name in cls.get_scene_names():
            scene_name = loop_name(scene_name, cls.get_scene_names(), 0)
        logging.debug(f"Create Scene '{scene_name}'")
        scene = ui_view.AggregationScene()
        scene.setSceneRect(QRectF(0, 0, SCENE_SIZE[0], SCENE_SIZE[1]))
        prop = cls.get_properties()
        prop.scene_name_list.append(scene_name)
        prop.scene_list.append(scene)
        prop.node_list.append(set())
        prop.import_list.append(list())
        prop.connections_list.append(set())
        prop.focus_list.append(False)
        prop.scene_settings_list.append(None)
        return scene, scene_name

    @classmethod
    def delete_scene(cls, scene: ui_view.AggregationScene) -> None:
        for node in list(cls.get_nodes_in_scene(scene)):
            cls.remove_node_from_scene(node, scene)
        logging.debug(f"delete {scene}")
        scene_index = cls.get_scene_index(scene)
        prop = cls.get_properties()
        scene = prop.scene_list[scene_index]
        lists = [prop.scene_name_list, prop.node_list, prop.import_list, prop.connections_list, prop.focus_list,
                 prop.scene_settings_list, prop.scene_list]
        [scene_list.pop(scene_index) for scene_list in lists]
        scene.deleteLater()

    @classmethod
    def import_aggregations_from_project(cls, proj: SOMcreator.Project) -> None:
        plugin_dict = proj.import_dict
        if not plugin_dict:
            return

        aggregation_ref = {aggregation.uuid: aggregation for aggregation in proj.get_aggregations(filter=False)}
        import_scene_dict = plugin_dict.get(AGGREGATIONSCENES)

        if import_scene_dict is None:
            logging.warning(
                f"SOMJson was written in OLD version. Please open with SOM-Toolkit v2.11.3 and save it as new version.")
            return

        existing_scene_names = cls.get_properties().scene_name_list
        for scene_name, node_dict in import_scene_dict.items():
            if isinstance(node_dict[NODES], list):
                logging.warning(
                    f"SOMJson was written in OLD version. "
                    f"Please open with SOM-Toolkit v2.11.3 and save it as new version.")
                return
            if scene_name not in existing_scene_names:
                scene, scene_name = cls.create_scene(scene_name)

            scene_id = cls.get_scene_index(scene_name)
            position_values = node_dict["Nodes"].values()
            if not position_values:
                continue
            x_values, y_values = zip(*position_values)
            x_min, y_min = min(x_values), min(y_values)
            for aggregation_uuid, pos in node_dict["Nodes"].items():
                x = SCENE_SIZE[0] / 2 + pos[0] - x_min
                y = SCENE_SIZE[1] / 2 + pos[1] - y_min
                aggregation_tuple = (aggregation_ref[aggregation_uuid], QPointF(x, y))
                cls.get_properties().import_list[scene_id].append(aggregation_tuple)

    @classmethod
    def get_scene_names(cls) -> list[str]:
        return cls.get_properties().scene_name_list

    @classmethod
    def get_active_scene(cls) -> None | ui_view.AggregationScene:
        return cls.get_properties().active_scene

    @classmethod
    def activate_scene(cls, scene: ui_view.AggregationScene) -> None:
        if scene == cls.get_active_scene():
            return

        view = cls.get_view()
        old_scene = cls.get_active_scene()
        prop = cls.get_properties()

        if old_scene is not None and old_scene in cls.get_properties().scene_list:
            old_index = cls.get_scene_index(old_scene)
            horizontal = view.horizontalScrollBar().value()
            vertical = view.verticalScrollBar().value()
            prop.scene_settings_list[old_index] = view.transform(), horizontal, vertical

        cls.get_view().setScene(scene)
        prop.active_scene = scene
        new_scene_index = cls.get_scene_index(scene)
        value = prop.scene_settings_list[new_scene_index]
        if value is None:
            return
        trans, horizontal, vertical = value
        view.setTransform(trans)
        view.horizontalScrollBar().setValue(horizontal)
        view.verticalScrollBar().setValue(vertical)

    @classmethod
    def set_cursor_style(cls, cursor_style: Qt.CursorShape) -> None:
        cls.get_view().viewport().setCursor(cursor_style)

    @classmethod
    def add_node_to_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene) -> None:
        scene.addItem(node)
        scene.addItem(node.header)
        scene.addItem(node.frame)
        scene.addItem(node.resize_rect)
        scene.addItem(node.circle)
        scene_index = cls.get_scene_index(scene)
        cls.get_properties().node_list[scene_index].add(node)

    @classmethod
    def clean_import_list_of_scene(cls, scene: ui_view.AggregationScene) -> None:
        index = cls.get_scene_index(scene)
        cls.get_properties().import_list[index] = list()

    @classmethod
    def autofit_view(cls) -> None:
        scene = cls.get_active_scene()
        bounding_rect = QRectF()
        for item in scene.items():
            bounding_rect = bounding_rect.united(item.sceneBoundingRect())
        cls.get_view().fitInView(bounding_rect.adjusted(-SCENE_MARGIN, -SCENE_MARGIN, SCENE_MARGIN, SCENE_MARGIN),
                                 aspectRadioMode=Qt.AspectRatioMode.KeepAspectRatio)
        scene_id = cls.get_scene_index(scene)
        cls.get_properties().focus_list[scene_id] = True

    @classmethod
    def get_nodes_in_scene(cls, scene: ui_view.AggregationScene) -> set[ui_node.NodeProxy]:
        scene_index = cls.get_scene_index(scene)
        return cls.get_properties().node_list[scene_index]

    @classmethod
    def get_aggregations_in_scene(cls, scene):
        scene_index = cls.get_scene_index(scene)
        aggregation_list = list(cls.get_import_list()[scene_index])
        nodes = cls.get_nodes_in_scene(scene)
        aggregation_list += [(n.aggregation, n.scenePos()) for n in nodes]
        return aggregation_list

    @classmethod
    def remove_node_from_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene) -> None:
        logging.debug(f"Delete Node {node.aggregation.name}")
        if node.top_connection:
            cls.remove_connection_from_scene(node.top_connection, scene)
        [cls.remove_connection_from_scene(c, scene) for c in list(node.bottom_connections)]
        scene_index = cls.get_scene_index(scene)
        prop = cls.get_properties()
        prop.node_list[scene_index].remove(node)
        scene.removeItem(node.header)
        scene.removeItem(node.frame)
        scene.removeItem(node.resize_rect)
        scene.removeItem(node.circle)
        scene.removeItem(node)
        node.deleteLater()
        if node.aggregation in node.aggregation.project.get_aggregations(filter=False):
            node.aggregation.delete()

    @classmethod
    def remove_connection_from_scene(cls, connection: ui_connection.Connection,
                                     scene: ui_view.AggregationScene) -> None:
        if connection is None:
            return

        scene.removeItem(connection)
        connection.top_node.bottom_connections.remove(connection)
        connection.bottom_node.top_connection = None
        cls.get_properties().connections_list[cls.get_scene_index(scene)].remove(connection)

    @classmethod
    def get_last_mouse_pos(cls) -> QPointF | None:
        return cls.get_properties().last_mouse_pos

    @classmethod
    def set_last_mouse_pos(cls, mouse_pos: QPointF | None) -> None:
        cls.get_properties().last_mouse_pos = mouse_pos

    @classmethod
    def get_item_under_mouse(cls, position: QPointF) -> Any:
        scene = cls.get_active_scene()
        return scene.itemAt(position, QTransform())

    @classmethod
    def set_mouse_mode(cls, mode: int) -> None:
        """
        mode: 0= None 1= pan, 2= drag, 3 = resize 4 = selection_rect
        """
        cls.get_properties().mouse_mode = mode

    @classmethod
    def get_mouse_mode(cls) -> int:
        """
        mode: 0= None 1= pan, 2= drag 3 = resize
        """
        return cls.get_properties().mouse_mode

    @classmethod
    def map_to_scene(cls, pos: QPoint) -> QPointF:
        return cls.get_view().mapToScene(pos)

    @classmethod
    def get_keyboard_modifier(cls) -> Qt.KeyboardModifiers:
        return QApplication.keyboardModifiers()

    @classmethod
    def scale_view(cls, agle: float, target_viewport_pos: QPoint) -> None:
        # copied from https://stackoverflow.com/questions/19113532/
        # qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel

        view = cls.get_view()
        factor = 1.0015 ** agle
        target_scene_pos = cls.map_to_scene(target_viewport_pos)

        view.scale(factor, factor)
        view.centerOn(target_scene_pos)
        delta_viewport_pos = target_viewport_pos.toPointF() - QPointF(view.viewport().width() / 2.0,
                                                                      view.viewport().height() / 2.0)
        viewport_center = view.mapFromScene(target_scene_pos).toPointF() - delta_viewport_pos
        view.centerOn(view.mapToScene(viewport_center.toPoint()))

    @classmethod
    def scroll_view(cls, x_angle, y_angle) -> None:
        view = cls.get_view()
        view.horizontalScrollBar().setValue(view.horizontalScrollBar().value() - x_angle)
        view.verticalScrollBar().setValue(view.verticalScrollBar().value() - y_angle)

    @classmethod
    def set_resize_node(cls, node: ui_node.NodeProxy | None):
        cls.get_properties().resize_node = node

    @classmethod
    def get_resize_node(cls) -> ui_node.NodeProxy:
        return cls.get_properties().resize_node

    @classmethod
    def get_mouse_mode_by_subitem(cls, sub_item) -> int:
        """
                return: 0= None 1= pan, 2= drag, 3 = resize 4 = selection_rect  5 = draw connection
        """
        sub_item_type = type(sub_item)
        cursor_dict = {
            ui_node.Header:     2,
            ui_node.ResizeRect: 3,
            type(None):         1,
            ui_node.Circle:     5,
            ui_node.PlusText:   5,
        }
        val = cursor_dict.get(sub_item_type) or 1
        return val

    @classmethod
    def scene_was_alleady_focused(cls, scene: ui_view.AggregationScene) -> bool:
        scene_id = cls.get_scene_index(scene)
        return cls.get_properties().focus_list[scene_id]

    @classmethod
    def add_aggregation_to_import_list(cls, scene, aggregation, pos: QPointF) -> None:
        scene_id = cls.get_scene_index(scene)
        cls.get_properties().import_list[scene_id].append((aggregation, pos))

    @classmethod
    def get_node_under_mouse(cls) -> ui_node.NodeProxy | None:
        nodes = cls.get_nodes_in_scene(cls.get_active_scene())
        for node in nodes:
            if node.frame.isUnderMouse():
                return node
        return None

    @classmethod
    def print_scene(cls, scene: ui_view.AggregationScene, path: str | None = None) -> None:
        view = cls.get_view()
        if path is None:
            file_text = "png Files (*.png);;"
            path = QFileDialog.getSaveFileName(view, "Aggregationsansicht speichern", "", file_text)[0]
        cls.activate_scene(scene)
        rect = view.viewport().rect()
        image = QImage(rect.size() * 8, QImage.Format.Format_RGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        view.render(painter)
        image.save(path)
        painter.end()

    @classmethod
    def set_drag_mode(cls, mode: QGraphicsView.DragMode) -> None:
        cls.get_view().setDragMode(mode)

    @classmethod
    def get_all_scenes(cls) -> list[ui_view.AggregationScene]:
        return list(cls.get_properties().scene_list)

    @classmethod
    def get_objects_in_scene(cls, scene: ui_view.AggregationScene) -> set[SOMcreator.Object]:
        nodes = cls.get_nodes_in_scene(scene)
        scene_index = cls.get_scene_index(scene)
        objects = {a.object for a, pos in cls.get_import_list()[scene_index]}
        objects.update({n.aggregation.object for n in nodes})
        return objects

    @classmethod
    def get_import_list(cls) -> list[list[tuple[SOMcreator.Aggregation, QPointF]]]:
        return cls.get_properties().import_list

    @classmethod
    def zoom_to_selected(cls) -> None:
        scene = cls.get_active_scene()
        selected_items = [node.frame for node in scene.selectedItems()]
        if not selected_items:
            return
        view = cls.get_view()
        rect: QRectF = selected_items[0].sceneBoundingRect()
        for item in selected_items:
            rect = rect.united(item.sceneBoundingRect())
        margin = 50
        rect.adjust(-margin, -margin, margin, margin)
        view.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    @classmethod
    def get_bounding_box_of_nodes(cls, nodes: set[ui_node.NodeProxy]) -> QRectF:
        if not nodes:
            return QRectF()
        items = [n.frame for n in nodes]
        rect: QRectF = items[0].sceneBoundingRect()
        for item in items:
            rect = rect.united(item.sceneBoundingRect())
        return rect

    @classmethod
    def get_selected_nodes(cls) -> set[ui_node.NodeProxy]:
        scene = cls.get_active_scene()
        return {node for node in scene.selectedItems() if isinstance(node, ui_node.NodeProxy)}

    @classmethod
    def set_copy_list(cls, copy_list: list[tuple[SOMcreator.Aggregation, QPointF]]) -> None:
        cls.get_properties().copy_list = copy_list

    @classmethod
    def get_copy_list(cls) -> list[tuple[SOMcreator.Aggregation, QPointF]]:
        return list(cls.get_properties().copy_list)

    @classmethod
    def get_scene_cursor_pos(cls) -> QPointF:
        view = cls.get_view()
        cursor_pos = view.mapToScene(view.mapFromGlobal(QCursor.pos()))
        return cursor_pos

    @classmethod
    def add_connection_to_scene(cls, connection: ui_connection.Connection, scene: ui_view.AggregationScene) -> None:
        scene.addItem(connection)
        cls.get_properties().connections_list[cls.get_scene_index(scene)].add(connection)

    @classmethod
    def create_connection_by_pos(cls, top_node: ui_node.NodeProxy):
        if top_node is None:
            return
        scene = cls.get_active_scene()
        bottom_node = cls.get_node_under_mouse()
        if bottom_node is None:
            return
        if bottom_node.aggregation.parent is not None:
            bottom_node.aggregation.parent.remove_child(bottom_node.aggregation)
            cls.remove_connection_from_scene(bottom_node.top_connection, scene)
        top_node.aggregation.add_child(bottom_node.aggregation, 1)

    @classmethod
    def reset_cursor(cls, position) -> None:
        cls.set_mouse_mode(0)
        cls.set_resize_node(None)
        cls.set_last_mouse_pos(position)
        cls.get_view().viewport().unsetCursor()

    @classmethod
    def get_hover_cursor(cls, scene_pos: QPointF) -> Qt.CursorShape:
        item_under_mouse = cls.get_item_under_mouse(scene_pos)
        if aw_tool.Node.item_is_resize_rect(item_under_mouse):
            return Qt.CursorShape.SizeFDiagCursor
        if aw_tool.Node.item_is_frame(item_under_mouse):
            item_under_mouse: ui_node.Frame
            node = item_under_mouse.node
            if node.header.isUnderMouse():
                return Qt.CursorShape.OpenHandCursor
            if node.circle.isUnderMouse():
                return Qt.CursorShape.CrossCursor
        if aw_tool.Node.item_is_circle(item_under_mouse):
            return Qt.CursorShape.CrossCursor
        if aw_tool.Node.item_is_circle_text(item_under_mouse):
            return Qt.CursorShape.CrossCursor
        return Qt.CursorShape.ArrowCursor

    @classmethod
    def get_press_cursor(cls, scene_pos: QPointF) -> Qt.CursorShape:
        item_under_mouse = cls.get_item_under_mouse(scene_pos)
        if aw_tool.Node.item_is_resize_rect(item_under_mouse):
            return Qt.CursorShape.SizeFDiagCursor
        if aw_tool.Node.item_is_frame(item_under_mouse):
            item_under_mouse: ui_node.Frame
            node = item_under_mouse.node
            if node.header.isUnderMouse():
                return Qt.CursorShape.ClosedHandCursor
            if node.circle.isUnderMouse():
                return Qt.CursorShape.CrossCursor
        if aw_tool.Node.item_is_circle(item_under_mouse):
            return Qt.CursorShape.CrossCursor
        if aw_tool.Node.item_is_circle_text(item_under_mouse):
            return Qt.CursorShape.CrossCursor
        if item_under_mouse is None:
            return Qt.CursorShape.ClosedHandCursor
        return Qt.CursorShape.ArrowCursor

    @classmethod
    def remove_nodes_with_deleted_aggregations(cls, scene: ui_view.AggregationScene, proj: SOMcreator.Project) -> None:
        nodes = cls.get_nodes_in_scene(scene)
        existing_aggregations = list(proj.get_aggregations(filter=False))
        for existing_node in list(nodes):
            if existing_node.aggregation not in existing_aggregations:
                cls.remove_node_from_scene(existing_node, scene)

    @classmethod
    def create_child_node(cls, top_node: ui_node.NodeProxy,
                          obj: SOMcreator.Object) -> ui_node.NodeProxy | None:
        scene = top_node.scene()
        pos = top_node.sceneBoundingRect().bottomLeft() + QPointF(100., 60.)
        return trigger.add_object_to_scene(obj, scene, top_node, pos)
