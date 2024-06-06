from __future__ import annotations

import os
import logging
from typing import TYPE_CHECKING, Callable
from PySide6.QtCore import QPointF, QRectF, Qt, QPoint
from PySide6.QtGui import QTransform, QAction, QImage, QPainter
from PySide6.QtWidgets import QApplication, QMenu, QFileDialog, QGraphicsTextItem
import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.view import ui as ui_view
import SOMcreator
from SOMcreator.constants import json_constants
from som_gui.aggregation_window.module.view.constants import AGGREGATIONSCENES, SCENE_SIZE, SCENE_MARGIN
from som_gui.aggregation_window.module.node import ui as ui_node
from som_gui.aggregation_window import tool as aw_tool

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.view.prop import ViewProperties
    from som_gui.aggregation_window.module.connection import ui as ui_connection


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
    def get_scene_by_name(cls, scene_name: str) -> ui_view.AggregationScene | None:
        if scene_name not in cls.get_properties().scene_name_list:
            return None
        return cls.get_properties().scene_list[cls.get_scene_index(scene_name)]

    @classmethod
    def get_scene_name(cls, scene: ui_view.AggregationScene) -> str:
        index = cls.get_scene_index(scene)
        if index is None:
            return None
        return cls.get_properties().scene_name_list[index]

    @classmethod
    def create_view(cls) -> ui_view.AggregationView:
        view = ui_view.AggregationView()
        cls.get_properties().aggregation_view = view
        return view

    @classmethod
    def create_scene(cls, scene_name: str) -> tuple[ui_view.AggregationScene, str]:
        if scene_name in cls.get_scene_names():
            scene_name = loop_name(scene_name, cls.get_scene_names(), 0)
        logging.debug(f"Create Scene '{scene_name}'")
        scene = ui_view.AggregationScene()
        scene.name = scene_name
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
    def delete_scene(cls, scene: ui_view.AggregationScene):
        for node in list(cls.get_nodes_in_scene(scene)):
            cls.remove_node_from_scene(node, scene)
        logging.debug(f"delete {scene}")
        scene_index = cls.get_scene_index(scene)
        prop = cls.get_properties()
        scene = prop.scene_list[scene_index]
        lists = [prop.scene_name_list, prop.node_list, prop.import_list, prop.connections_list, prop.focus_list,
                 prop.scene_settings_list, prop.scene_list]
        [l.pop(scene_index) for l in lists]
        scene.deleteLater()

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
                    f"SOMJson was written in OLD version. "
                    f"Please open with SOM-Toolkit v2.11.3 and save it as new version.")
                return
            if scene_name not in existing_scene_names:
                scene, scene_name = cls.create_scene(scene_name)

            scene_id = cls.get_scene_index(scene_name)
            position_values = node_dict["Nodes"].values()
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
    def get_active_scene(cls):
        return cls.get_properties().active_scene

    @classmethod
    def activate_scene(cls, scene: ui_view.AggregationScene):
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

        prop.aggregation_view.setScene(scene)
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
    def test(cls):
        pass

    @classmethod
    def set_cursor_style(cls, cursor_style):
        cls.get_properties().aggregation_view.viewport().setCursor(cursor_style)

    @classmethod
    def reset_cursor_style(cls):
        cls.get_properties().aggregation_view.viewport().unsetCursor()

    @classmethod
    def add_node_to_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene):
        scene.addItem(node)
        scene.addItem(node.header)
        scene.addItem(node.frame)
        scene.addItem(node.resize_rect)
        scene.addItem(node.circle)
        scene.addItem(node.circle.text)
        scene_index = cls.get_scene_index(scene)
        cls.get_properties().node_list[scene_index].add(node)

    @classmethod
    def clean_import_list_for_scene(cls, scene: ui_view.AggregationScene):
        index = cls.get_scene_index(scene)
        cls.get_properties().import_list[index] = list()

    @classmethod
    def autofit_view(cls):
        def get_bounding_rect():
            items = {item for item in scene.items() if isinstance(item, ui_node.Frame)}
            items = scene.items()
            if not items:
                return QRectF()
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
        scene_id = cls.get_scene_index(scene)
        cls.get_properties().focus_list[scene_id] = True

    @classmethod
    def get_nodes_in_scene(cls, scene: ui_view.AggregationScene):
        scene_index = cls.get_scene_index(scene)
        return cls.get_properties().node_list[scene_index]

    @classmethod
    def remove_node_from_scene(cls, node: ui_node.NodeProxy, scene: ui_view.AggregationScene):
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
        node.aggregation.delete()
    @classmethod
    def remove_connection_from_scene(cls, connection: ui_connection.Connection, scene: ui_view.AggregationScene):
        if connection is None:
            return

        logging.debug(
            f"Remove Con : {connection.bottom_node.aggregation.name} -> {connection.top_node.aggregation.name}")

        scene.removeItem(connection)
        connection.top_node.bottom_connections.remove(connection)
        connection.bottom_node.top_connection = None
        cls.get_properties().connections_list[cls.get_scene_index(scene)].remove(connection)

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
    def pan(cls, last_pos: QPointF, new_pos: QPointF):
        if last_pos is None:
            return
        dif = new_pos - last_pos
        view = cls.get_view()
        view.translate(dif.x(), dif.y())

    @classmethod
    def map_to_scene(cls, pos: QPointF):
        return cls.get_properties().aggregation_view.mapToScene(pos)

    @classmethod
    def get_keyboard_modifier(cls):
        return QApplication.keyboardModifiers()

    @classmethod
    def scale_view(cls, agle: float, target_viewport_pos: QPoint):
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
    def scroll_view(cls, x_angle, y_angle):
        view = cls.get_view()
        view.horizontalScrollBar().setValue(view.horizontalScrollBar().value() - x_angle)
        view.verticalScrollBar().setValue(view.verticalScrollBar().value() - y_angle)

    @classmethod
    def add_connection_to_scene(cls, connection: ui_connection.Connection, scene: ui_view.AggregationScene):
        scene.addItem(connection)
        cls.get_properties().connections_list[cls.get_scene_index(scene)].add(connection)

    @classmethod
    def set_resize_node(cls, node: ui_node.NodeProxy | None):
        cls.get_properties().resize_node = node

    @classmethod
    def get_resize_node(cls) -> ui_node.NodeProxy:
        return cls.get_properties().resize_node

    @classmethod
    def get_cursor_style_by_subitem(cls, sub_item, mode):
        """
        sub_item_type: type() of subitem
        mode: 0 = click, 1 = release
        """
        sub_item_type = type(sub_item)
        cursor_dict = {
            ui_node.Header:     [Qt.CursorShape.ClosedHandCursor, Qt.CursorShape.OpenHandCursor],
            ui_node.ResizeRect: [Qt.CursorShape.SizeFDiagCursor, Qt.CursorShape.SizeFDiagCursor],
            type(None): [Qt.CursorShape.ClosedHandCursor, Qt.CursorShape.ArrowCursor]
        }
        val = cursor_dict.get(sub_item_type)
        if val is None:
            val = [Qt.CursorShape.ArrowCursor, Qt.CursorShape.ArrowCursor]
        return val[mode]

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
    def scene_was_alleady_focused(cls, scene: ui_view.AggregationScene):
        scene_id = cls.get_scene_index(scene)
        return cls.get_properties().focus_list[scene_id]

    @classmethod
    def add_aggregation_to_import_list(cls, scene, aggregation, pos):
        scene_id = cls.get_scene_index(scene)
        cls.get_properties().import_list[scene_id].append((aggregation, pos))

    @classmethod
    def create_action(cls, menu_dict: dict[str, QAction | QMenu], name: str, action_func: Callable | None,
                      is_sub_menu: bool):
        parent_structure = "/".join(name.split("/")[:-1])
        if parent_structure not in menu_dict:
            parent: QMenu = cls.create_action(menu_dict, parent_structure, None, True)
        else:
            parent: QMenu = menu_dict[parent_structure]

        if is_sub_menu:
            menu = parent.addMenu(name.split("/")[-1])
            menu_dict[name] = menu
            return menu

        action = parent.addAction(name.split("/")[-1])
        if action_func is not None:
            action.triggered.connect(action_func)
        menu_dict[name] = action
        return action

    @classmethod
    def create_context_menu(cls, menu_list):
        menu_dict = dict()
        menu = QMenu()
        menu_dict[""] = menu
        for text, function in menu_list:
            cls.create_action(menu_dict, text, function, False)
        return menu

    @classmethod
    def get_node_under_mouse(cls, pos: QPointF) -> ui_node.NodeProxy | None:
        nodes = cls.get_nodes_in_scene(cls.get_active_scene())
        for node in nodes:
            if node.frame.isUnderMouse():
                return node
        return None

    @classmethod
    def print_scene(cls, scene: ui_view.AggregationScene, path: str | None = None):
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
    def print_all_scenes(cls):
        view = cls.get_view()
        folder_path = QFileDialog.getExistingDirectory(view, "Safe Aggregation", "")
        for scene_index, scene in enumerate(cls.get_properties().scene_list):
            scene_name = cls.get_scene_names()[scene_index]
            cls.activate_scene(scene)
            cls.autofit_view()
            path = os.path.join(folder_path, f"{scene_name}.png")
            cls.print_scene(scene, path)

    @classmethod
    def set_drag_mode(cls, mode):
        cls.get_view().setDragMode(mode)

    @classmethod
    def search_node(cls):
        pass

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
    def get_import_list(cls) -> list[list[tuple[SOMcreator.classes.Aggregation, QPointF]]]:
        return cls.get_properties().import_list

    @classmethod
    def zoom_to_selected(cls):
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
