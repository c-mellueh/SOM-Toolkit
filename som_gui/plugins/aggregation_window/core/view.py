from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QPoint, QPointF, Qt
import logging
import SOMcreator
from SOMcreator import value_constants
from som_gui import tool
from som_gui.plugins.aggregation_window.module.view.constants import (
    AGGREGATIONSCENES,
    SCENE_SIZE,
    SCENE_MARGIN,
)
from SOMcreator.datastructure.som_json import NODES

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window import tool as aw_tool
    from PySide6.QtGui import QWheelEvent, QKeyEvent
    from som_gui.plugins.aggregation_window.module.node import ui as node_ui


def key_press_event(
    event: QKeyEvent,
    view: Type[aw_tool.View],
    connection: Type[aw_tool.Connection],
    node: Type[aw_tool.Node],
) -> None:
    logging.debug(f"Key pressed: {event.key()}")
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5 and event.key() == Qt.Key.Key_Escape:
        connection.delete_draw_connection()
        view.reset_cursor(view.get_scene_cursor_pos())

    if event.key() == Qt.Key.Key_Delete:
        nodes = view.get_selected_nodes()
        for node in nodes:
            view.remove_node_from_scene(node, view.get_active_scene())

    if mouse_mode == 2 and event.key() == Qt.Key.Key_Control:
        node.lock_move_direction(True)


def key_release_event(
    event: QKeyEvent, view: Type[aw_tool.View], node: Type[aw_tool.Node]
) -> None:
    logging.debug(f"Key released: {event.key()}")
    mouse_mode = view.get_mouse_mode()
    if event.key() == Qt.Key.Key_Control:
        node.lock_move_direction(False)


def activate(view: Type[aw_tool.View], project: Type[tool.Project]) -> None:
    proj = project.get()
    if proj is None:
        return
    plugin_dict = proj.import_dict or dict()
    if not plugin_dict:
        view.set_project_scene_dict(dict())
        return

    scene_dict = plugin_dict.get(AGGREGATIONSCENES)
    if scene_dict is None:
        view.set_project_scene_dict(dict())
        return
    view.set_project_scene_dict(scene_dict)
    aggregation_ref = {
        aggregation.uuid: aggregation
        for aggregation in proj.get_aggregations(filter=False)
    }

    for scene_name, node_dict in scene_dict.items():
        if isinstance(node_dict[NODES], list):
            logging.warning(
                f"SOMJson was written in OLD version. "
                f"Please open with SOM-Toolkit v2.11.3 and save it as new version."
            )
            return
        if scene_name not in view.get_existing_scene_names():
            scene, scene_name = view.create_scene(scene_name)

        scene = view.get_scene_by_name(scene_name)
        position_values = node_dict["Nodes"].values()
        if not position_values:
            continue
        x_values, y_values = zip(*position_values)
        x_min, y_min = min(x_values), min(y_values)
        for aggregation_uuid, pos in node_dict["Nodes"].items():
            x = SCENE_SIZE[0] / 2 + pos[0] - x_min
            y = SCENE_SIZE[1] / 2 + pos[1] - y_min
            aggregation = aggregation_ref[aggregation_uuid]
            view.add_aggregation_to_import_list(scene, aggregation, QPointF(x, y))
    view.reset_drawn_scenes()


def paint_event(
    view: Type[aw_tool.View],
    node: Type[aw_tool.Node],
    connection: Type[aw_tool.Connection],
    project: Type[tool.Project],
) -> None:
    scene = view.get_active_scene()
    if scene is None:
        scene, scene_name = view.create_scene(
            QCoreApplication.translate("Aggregation", "Undefined")
        )
        view.activate_scene(scene)
    scene_id = view.get_scene_index(scene)

    # Add Nodes from import_list
    for aggregation, position in view.get_import_list()[scene_id]:
        new_node = node.create_node(aggregation)
        view.add_node_to_scene(new_node, scene)
        node.set_node_pos(new_node, position)
    view.clean_import_list_of_scene(scene)

    # delete Nodes with deleted Aggregations
    view.remove_nodes_with_deleted_aggregations(scene, project.get())

    # create connections
    node_dict = {node.aggregation: node for node in view.get_nodes_in_scene(scene)}
    for aggregation, top_node in node_dict.items():
        for sub_aggregation in aggregation.get_children(filter=True):
            sub_node = node_dict.get(sub_aggregation)
            if sub_node is None:
                continue
            if not node.is_node_connected_to_node(top_node, sub_node):
                new_connection = connection.create_connection(
                    top_node, sub_node, sub_node.aggregation.parent_connection
                )
                view.add_connection_to_scene(new_connection, scene)

        if not top_node.top_connection:
            continue
        if aggregation.parent_connection != top_node.top_connection.connection_type:
            top_node.top_connection.connection_type = aggregation.parent_connection
            top_node.top_connection.update()

    if not view.scene_was_drawn(scene):
        view.autofit_view()


def mouse_move_event(
    position: QPoint,
    view: Type[aw_tool.View],
    node: Type[aw_tool.Node],
    connection: Type[aw_tool.Connection],
):
    last_pos = view.get_last_mouse_pos()
    mouse_mode = view.get_mouse_mode()

    if mouse_mode == 3:  # resize
        node.resize_node(view.get_resize_node(), last_pos, view.map_to_scene(position))
    if mouse_mode == 5:  # draw connection
        connection.draw_connection(view.get_active_scene(), view.map_to_scene(position))
        connection.set_draw_started(True)
    view.set_last_mouse_pos(view.map_to_scene(position))
    if mouse_mode == 0:
        cursor = view.get_hover_cursor(view.map_to_scene(position))
        view.set_cursor_style(cursor)


def mouse_press_event(
    position: QPoint,
    view: Type[aw_tool.View],
    node: Type[aw_tool.Node],
    connection: Type[aw_tool.Connection],
) -> None:
    modifier = view.get_keyboard_modifier()
    view.set_last_mouse_pos(view.map_to_scene(position))
    scene = view.get_active_scene()
    item_under_mouse = view.get_item_under_mouse(view.map_to_scene(position))

    if node.item_is_frame(item_under_mouse):  # Mouse is on Node
        active_node: node_ui.NodeProxy = item_under_mouse.node
        if (
            modifier != Qt.KeyboardModifier.ControlModifier
            and active_node not in scene.selectedItems()
        ):
            scene.clearSelection()
        active_node.setSelected(True)
        header: node_ui.Header = active_node.header
        if header.isUnderMouse():
            item_under_mouse = header

    cursor_style = view.get_press_cursor(view.map_to_scene(position))
    mouse_mode = view.get_mouse_mode_by_subitem(item_under_mouse)

    if mouse_mode == 1:  # handle Rubber band
        view.set_drag_mode(view.get_view().DragMode.ScrollHandDrag)
        if modifier == Qt.KeyboardModifier.ShiftModifier:
            mouse_mode = 4
            view.set_drag_mode(view.get_view().DragMode.RubberBandDrag)

    if mouse_mode == 5:  # Set node from which the line is drawn
        connection.set_draw_node(item_under_mouse.node)
        view.set_drag_mode(view.get_view().DragMode.NoDrag)
        connection.set_draw_started(False)
    view.set_cursor_style(cursor_style)
    view.set_mouse_mode(mouse_mode)

    if node.item_is_resize_rect(item_under_mouse):
        view.set_resize_node(item_under_mouse.node)
        view.set_drag_mode(view.get_view().DragMode.NoDrag)


def mouse_release_event(
    position: QPoint,
    view: Type[aw_tool.View],
    connection: Type[aw_tool.Connection],
    search: Type[tool.Search],
    project: Type[tool.Project],
) -> None:
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5:  # Handle Connection Drawing
        if connection.is_drawing_started():
            view.create_connection_by_pos(connection.get_draw_node())
            connection.delete_draw_connection()
        else:
            som_class = search.search_class(list(project.get().get_classes(filter=True)))
            if som_class is not None:
                view.create_child_node(connection.get_draw_node(), som_class)

    view.reset_cursor(view.map_to_scene(position))
    new_cursor = view.get_hover_cursor(view.map_to_scene(position))
    view.set_cursor_style(new_cursor)


def mouse_wheel_event(wheel_event: QWheelEvent, view: Type[aw_tool.View]) -> None:
    x_angle, y_angle = wheel_event.angleDelta().x(), wheel_event.angleDelta().y()

    modifier = view.get_keyboard_modifier()
    if modifier == Qt.KeyboardModifier.ControlModifier:
        angle = [x_angle, y_angle]
        if 0 in angle:
            angle.remove(0)

        view.scale_view(angle[0], wheel_event.position().toPoint())
        return

    if modifier == Qt.KeyboardModifier.ShiftModifier:
        x_angle, y_angle = y_angle, x_angle

    view.scroll_view(x_angle, y_angle)


def context_menu_requested(
    pos: QPoint,
    view: Type[aw_tool.View],
    node: Type[aw_tool.Node],
    search: Type[tool.Search],
    connection: Type[aw_tool.Connection],
    buchheim: Type[aw_tool.Buchheim],
    project: Type[tool.Project],
    util: Type[tool.Util],
) -> None:
    menu_list = list()
    scene = view.get_active_scene()

    selected_nodes = scene.selectedItems()
    view_text = QCoreApplication.translate("Aggregation", "View")
    reset_zoom = QCoreApplication.translate("Aggregation", "Reset Zoom")
    print_view = QCoreApplication.translate("Aggregation", "Print View")
    menu_list.append([f"{view_text}/{reset_zoom}", view.autofit_view])
    menu_list.append([f"{view_text}/{print_view}", lambda: view.print_scene(scene)])

    if len(selected_nodes) > 1:
        layout = QCoreApplication.translate("Aggregation", "Layout")
        ch = QCoreApplication.translate("Aggregation", "Center horizontally")
        cv = QCoreApplication.translate("Aggregation", "Center vertically")
        dh = QCoreApplication.translate("Aggregation", "Distribute horizontally")
        dv = QCoreApplication.translate("Aggregation", "Distribute vertically")
        menu_list.append(
            [f"{layout}/{ch}", lambda: node.center_nodes(selected_nodes, 0)]
        )
        menu_list.append(
            [f"{layout}/{cv}", lambda: node.center_nodes(selected_nodes, 1)]
        )
        menu_list.append(
            [f"{layout}/{dh}", lambda: node.distribute_by_layer(selected_nodes, 0)]
        )
        menu_list.append(
            [f"{layout}/{dv}", lambda: node.distribute_nodes(selected_nodes, 1)]
        )

    menu_list.append(
        [
            QCoreApplication.translate("Aggregation", "Modify Info"),
            lambda: change_header_text(node, search, project),
        ]
    )
    menu_list.append(
        [
            QCoreApplication.translate("Aggregation", "Reset Info"),
            lambda: node.reset_title_settings(),
        ]
    )

    node_under_mouse = view.get_node_under_mouse()
    if node_under_mouse:
        node_text = QCoreApplication.translate("Aggregation", "Node")
        add = QCoreApplication.translate("Aggregation", "Add Node")
        delete_node = QCoreApplication.translate("Aggregation", "Delete Node")
        delete_nodes = QCoreApplication.translate("Aggregation", "Delete Nodes")

        menu_list.append(
            [
                f"{node_text}/{add}",
                lambda: add_node_at_pos(view.map_to_scene(pos), view, search, project),
            ]
        )

        txt = delete_node if len(selected_nodes) == 1 else delete_nodes
        del_text = f"{node_text}/{txt}"
        menu_list.append(
            [
                del_text,
                lambda: [view.remove_node_from_scene(n, scene) for n in selected_nodes],
            ]
        )

        connection_type = QCoreApplication.translate("Aggregation", "Connection Type")
        aggregation = QCoreApplication.translate("Aggregation", "Aggregation")
        inheritance = QCoreApplication.translate("Aggregation", "Inheritance")
        if not node.is_root(node_under_mouse):
            menu_list.append(
                [
                    f"{connection_type}/{aggregation}",
                    lambda: node.set_connect_type(
                        node_under_mouse, value_constants.AGGREGATION
                    ),
                ]
            )
            menu_list.append(
                [
                    f"{connection_type}/{inheritance}",
                    lambda: node.set_connect_type(
                        node_under_mouse, value_constants.INHERITANCE
                    ),
                ]
            )
            menu_list.append(
                [
                    f"{connection_type}/{aggregation}+{inheritance}",
                    lambda: node.set_connect_type(
                        node_under_mouse,
                        value_constants.AGGREGATION + value_constants.INHERITANCE,
                    ),
                ]
            )
    else:
        add = QCoreApplication.translate("Aggregation", "Add Node")

        menu_list.append(
            [
                add,
                lambda: add_node_at_pos(view.map_to_scene(pos), view, search, project),
            ]
        )

    menu_list.append(
        [
            QCoreApplication.translate("Aggregation", "Rearange"),
            lambda: rearange(buchheim, view, node, connection),
        ]
    )

    menu = util.create_context_menu(menu_list)
    menu.exec(view.get_view().viewport().mapToGlobal(pos))

    paint_event(view, node, connection, project)


def rearange(
    buchheim: Type[aw_tool.Buchheim],
    view: Type[aw_tool.View],
    node: Type[aw_tool.Node],
    connection: Type[aw_tool.Connection],
):
    scene = view.get_active_scene()
    all_nodes = view.get_nodes_in_scene(scene)
    root_nodes = [n for n in all_nodes if node.is_root(n)]
    if not root_nodes:
        return
    # create helper to structure multiple root nodes
    helper_class = SOMcreator.SOMClass("INV", None)
    helper_aggregation = SOMcreator.SOMAggregation(helper_class)
    helper_node = node.create_node(helper_aggregation)
    for root_node in root_nodes:
        connection.create_connection(helper_node, root_node, 1)

    # calculate extremes and midpoints
    root_x_pos = [n.pos().x() for n in root_nodes]
    root_y_pos = [n.pos().y() for n in root_nodes]
    root_mid_x = (min(root_x_pos) + max(root_x_pos)) / 2
    root_mid_y = (min(root_y_pos) + max(root_y_pos)) / 2
    min_x = min(n.pos().x() for n in all_nodes)
    min_y = min(n.pos().y() for n in all_nodes)

    # position helper node in the center of all root_nodes
    node.set_node_pos(helper_node, QPointF(root_mid_x, root_mid_y))

    # run buchheim algorithm for restructuring hirarchical trees
    # see https://github.com/llimllib/personal_code/blob/4006951b133305e1dd9bc12cf7a2cb4c7048213b/python/trees/buchheim.py

    buchheim.intialize(helper_node)
    buchheim.buchheim(helper_node)
    buchheim.rearrange(helper_node, QPointF(min_x, min_y))

    # delete Helpers which won't be needed anymore
    helper_node.deleteLater()
    helper_class.delete()


def add_node_at_pos(
    pos,
    view: Type[aw_tool.View],
    search: Type[tool.Search],
    project: Type[tool.Project],
) -> None:
    scene = view.get_active_scene()
    som_class = search.search_class(list(project.get().get_classes(filter=True)))
    if not som_class:
        return
    aggregation = SOMcreator.SOMAggregation(som_class)
    view.add_aggregation_to_import_list(scene, aggregation, pos)


def change_header_text(
    node: Type[aw_tool.Node], search: Type[tool.Search], project: Type[tool.Project]
) -> None:
    searchable_properties = list()
    search_values = list()
    for som_property in project.get().get_properties(filter=False):
        value = [som_property.property_set.name, som_property.name]
        if value not in search_values:
            searchable_properties.append(som_property)
            search_values.append(value)
    som_property = search.search_property(searchable_properties)
    if som_property:
        node.set_title_settings(som_property.property_set.name, som_property.name)


def add_class_to_scene(
    som_class: SOMcreator.SOMClass,
    scene,
    parent_node: node_ui.NodeProxy | None,
    pos: QPoint | None,
    view: Type[aw_tool.View],
    connection: Type[aw_tool.Connection],
    node: Type[aw_tool.Node],
):
    if scene is None:
        scene = view.get_active_scene()
    if pos is None:
        pos = QPointF(100.0, 100.0)

    aggregation = SOMcreator.SOMAggregation(som_class)
    new_node = node.create_node(aggregation)
    view.add_node_to_scene(new_node, scene)
    node.set_node_pos(new_node, pos)

    if parent_node is not None:
        con = connection.create_connection(parent_node, new_node, 1)
        view.add_connection_to_scene(con, view.get_active_scene())
    return new_node


def reset(view: aw_tool.View):
    import som_gui
    from som_gui.plugins.aggregation_window.module.view import prop

    logging.info(f"Reset View Module")
    som_gui.ViewProperties = prop.ViewProperties()
    prop = view.get_properties()