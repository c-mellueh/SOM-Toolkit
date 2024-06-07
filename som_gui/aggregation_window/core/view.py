from __future__ import annotations

from typing import TYPE_CHECKING, Type
from PySide6.QtCore import Qt, QPointF
from SOMcreator import classes, value_constants

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool as aw_tool
    from som_gui import tool
    from PySide6.QtGui import QWheelEvent
    from som_gui.aggregation_window.module.node import ui as node_ui


def import_pos_from_project(view: Type[aw_tool.View], project: Type[tool.Project]) -> None:
    view.import_aggregations_from_project(project.get())


def paint_event(view: Type[aw_tool.View], node: Type[aw_tool.Node], connection: Type[aw_tool.Connection],
                project: Type[tool.Project]) -> None:
    scene = view.get_active_scene()
    if scene is None:
        scene, scene_name = view.create_scene("Undefined")
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
        for sub_aggregation in aggregation.children:
            sub_node = node_dict.get(sub_aggregation)
            if sub_node is None:
                continue
            if not node.is_node_connected_to_node(top_node, sub_node):
                new_connection = connection.create_connection(top_node, sub_node,
                                                              sub_node.aggregation.parent_connection)
                view.add_connection_to_scene(new_connection, scene)

        if not top_node.top_connection:
            continue
        if aggregation.parent_connection != top_node.top_connection.connection_type:
            top_node.top_connection.connection_type = aggregation.parent_connection
            top_node.top_connection.update()

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
                      connection: Type[aw_tool.Connection]) -> None:
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
                        connection: Type[aw_tool.Connection], search: Type[tool.Search]) -> None:
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5:  # Handle Connection Drawing
        if connection.is_drawing_started():
            view.create_connection_by_pos(connection.get_draw_node())
            connection.delete_draw_connection()
        else:
            obj = search.search_object()
            new_node = view.create_connection_by_search(connection.get_draw_node(), obj)
            con = connection.create_connection(connection.get_draw_node(), new_node, 1)
            view.add_connection_to_scene(con, view.get_active_scene())

    view.reset_cursor(position)
    new_cursor = view.get_hover_cursor(view.map_to_scene(position))
    view.set_cursor_style(new_cursor)


def mouse_wheel_event(wheel_event: QWheelEvent, view: Type[aw_tool.View]) -> None:
    x_angle, y_angle = wheel_event.angleDelta().x(), wheel_event.angleDelta().y()

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


def context_menu_requested(pos: QPointF, view: Type[aw_tool.View], node: Type[aw_tool.Node], search: Type[tool.Search],
                           connection: Type[aw_tool.Connection], project: Type[tool.Project]) -> None:
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

    node_under_mouse = view.get_node_under_mouse()
    if node_under_mouse:
        menu_list.append(["Node/Node hinzufügen", lambda: add_node_at_pos(view.map_to_scene(pos), view, search)])

        txt = "Node/Node Löschen" if len(selected_nodes) == 1 else "Nodes Löschen"
        menu_list.append([txt, lambda: [view.remove_node_from_scene(n, scene) for n in selected_nodes]])
        if not node.is_root(node_under_mouse):
            menu_list.append(["Verbindungsart/Aggregation",
                              lambda: node.set_connect_type(node_under_mouse, value_constants.AGGREGATION)])
            menu_list.append(["Verbindungsart/Vererbung",
                              lambda: node.set_connect_type(node_under_mouse, value_constants.INHERITANCE)])
            menu_list.append(["Verbindungsart/Aggregation+Vererbung",
                              lambda: node.set_connect_type(node_under_mouse,
                                                            value_constants.AGGREGATION + value_constants.INHERITANCE)])
    else:
        menu_list.append(["Node hinzufügen", lambda: add_node_at_pos(view.map_to_scene(pos), view, search)])

    menu = view.create_context_menu(menu_list)
    menu.exec(view.get_view().viewport().mapToGlobal(pos))
    paint_event(view, node, connection, project)


def add_node_at_pos(pos, view: Type[aw_tool.View], search: Type[tool.Search]) -> None:
    scene = view.get_active_scene()
    obj = search.search_object()
    if not obj:
        return
    aggregation = classes.Aggregation(obj)
    view.add_aggregation_to_import_list(scene, aggregation, pos)


def change_header_text(node: Type[aw_tool.Node], search: Type[tool.Search]) -> None:
    result = search.search_attribute()
    if result:
        node.set_title_settings(*result)
