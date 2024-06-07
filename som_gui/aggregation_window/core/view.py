from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import Qt
from SOMcreator import classes, value_constants
from PySide6.QtWidgets import QMenu, QGraphicsTextItem
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool as aw_tool
    from som_gui import tool
    from PySide6.QtCore import QPointF
    from PySide6.QtGui import QWheelEvent
    from som_gui.aggregation_window.module.node import ui as node_ui


def import_positions(view: Type[aw_tool.View], project: Type[tool.Project]):
    proj = project.get()
    plugin_dict = proj.import_dict
    view.create_scene_dict(proj, plugin_dict)


def paint_event(view: Type[aw_tool.View], node: Type[aw_tool.Node], connection: Type[aw_tool.Connection],
                project: Type[tool.Project]):
    scene = view.get_active_scene()
    scene_id = view.get_scene_index(scene)

    # Add Nodes from import_list
    for aggregation, position in view.get_import_list()[scene_id]:
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

    # create connections
    node_dict = {node.aggregation: node for node in view.get_nodes_in_scene(scene)}
    for aggregation, top_node in node_dict.items():
        for sub_aggregation in aggregation.children:
            sub_node = node_dict.get(sub_aggregation)
            if sub_node is None:
                continue
            if not node.is_node_connected_to_node(top_node, sub_node):
                new_connection = connection.create_connection(top_node, sub_node,
                                                              sub_node.aggregation.parent_connection)
                view.add_connection_to_scene(new_connection, scene)

    if not view.scene_was_alleady_focused(scene):
        view.autofit_view()


def mouse_move_event(position: QPointF, view: Type[aw_tool.View], node: Type[aw_tool.Node],
                     connection: Type[aw_tool.Connection], ):
    last_pos = view.get_last_mouse_pos()
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 3:
        node.resize_node(view.get_resize_node(), last_pos, view.map_to_scene(position))
    if mouse_mode == 5:
        connection.draw_connection(view.get_active_scene(), view.map_to_scene(position))
        connection.set_draw_started(True)
    view.set_last_mouse_pos(view.map_to_scene(position))
    if mouse_mode == 0:
        cursor = view.get_hover_cursor(view.map_to_scene(position))
        view.set_cursor_style(cursor)


def mouse_press_event(position: QPointF, view: Type[aw_tool.View], node: Type[aw_tool.Node],
                      connection: Type[aw_tool.Connection], ):
    modifier = view.get_keyboard_modifier()
    view.set_last_mouse_pos(view.map_to_scene(position))
    scene = view.get_active_scene()
    item_under_mouse = view.get_item_under_mouse(view.map_to_scene(position))

    if node.item_is_frame(item_under_mouse):  # Mouse is on Node
        active_node: node_ui.NodeProxy = item_under_mouse.node
        if modifier != Qt.KeyboardModifier.ControlModifier and active_node not in scene.selectedItems():
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


def mouse_release_event(position: QPointF, view: Type[aw_tool.View],
                        connection: Type[aw_tool.Connection], search: Type[tool.Search]):
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5:  # Handle Connection Drawing
        if connection.get_draw_started():
            view.create_connection_by_pos(connection.get_draw_node(), view.map_to_scene(position))
            connection.delete_draw_connection()
        else:
            obj = search.search_object()
            new_node = view.create_connection_by_search(connection.get_draw_node(), obj)
            con = connection.create_connection(connection.get_draw_node(), new_node, 1)
            view.add_connection_to_scene(con, view.get_active_scene())

    view.reset_cursor(position)
    new_cursor = view.get_hover_cursor(view.map_to_scene(position))
    view.set_cursor_style(new_cursor)


def mouse_wheel_event(wheel_event: QWheelEvent, view: Type[aw_tool.View]):
    y_angle = wheel_event.angleDelta().y()
    x_angle = wheel_event.angleDelta().x()

    modifier = view.get_keyboard_modifier()
    if modifier == Qt.ControlModifier:
        angle = [x_angle, y_angle]
        if 0 in angle:
            angle.remove(0)

        view.scale_view(angle[0], wheel_event.position().toPoint())
        return

    if modifier == Qt.ShiftModifier:
        x_angle, y_angle = y_angle, x_angle

    view.scroll_view(x_angle, y_angle)


def context_menu_requested(pos: QPointF, view: Type[aw_tool.View], node: Type[aw_tool.Node], search: Type[tool.Search]):
    menu_list = list()
    scene = view.get_active_scene()
    menu_list.append(["Ansicht/Zoom zurücksetzen", view.autofit_view])
    selected_nodes = scene.selectedItems()
    if len(selected_nodes) > 1:
        menu_list.append(["Layout/Horizontal zentrieren", lambda: node.center_nodes(selected_nodes, 0)])
        menu_list.append(["Layout/Vertikal zentrieren", lambda: node.center_nodes(selected_nodes, 1)])
        menu_list.append(["Layout/Horizontal verteilen", lambda: node.distribute_by_layer(selected_nodes, 0)])
        menu_list.append(["Layout/Vertikal verteilen", lambda: node.distribute_nodes(selected_nodes, 1)])

    menu_list.append(["Info anpassen", lambda: change_header_text(node, search)])
    menu_list.append(["Info zurücksetzen", lambda: node.reset_title_settings()])
    menu_list.append(["Ansicht/Ansicht Drucken", lambda: view.print_scene(scene)])
    # menu_list.append(["Drucken/Alles Drucken",lambda: view.print_all_scenes()])

    menu_list.append(["Node hinzufügen", lambda: add_node_at_pos(view.map_to_scene(pos), view, search)])
    node_under_mouse = view.get_node_under_mouse(view.map_to_scene(pos))
    if node_under_mouse:
        txt = "Node Löschen" if len(selected_nodes) == 1 else "Nodes Löschen"
        menu_list.append([txt, lambda: [view.remove_node_from_scene(n, scene) for n in selected_nodes]])
        if not node.is_root(node_under_mouse):
            aggreg_func = lambda: node.set_connect_type(node_under_mouse, value_constants.AGGREGATION)
            menu_list.append(["Verbindungsart/Aggregation", aggreg_func])

            inher_func = lambda: node.set_connect_type(node_under_mouse, value_constants.INHERITANCE)
            menu_list.append(["Verbindungsart/Vererbung", inher_func])

            combi_func = lambda: node.set_connect_type(node_under_mouse,
                                                       value_constants.AGGREGATION + value_constants.INHERITANCE)
            menu_list.append(["Verbindungsart/Aggregation+Vererbung", combi_func])

    menu = view.create_context_menu(menu_list)
    menu.exec(view.get_view().viewport().mapToGlobal(pos))


def add_node_at_pos(pos, view: Type[aw_tool.View], search: Type[tool.Search]):
    scene = view.get_active_scene()
    obj = search.search_object()
    if not obj:
        return
    aggregation = classes.Aggregation(obj)
    view.add_aggregation_to_import_list(scene, aggregation, pos)


def change_header_text(node: Type[aw_tool.Node], search: Type[tool.Search]):
    result = search.search_attribute()
    if result:
        node.set_title_settings(*result)
