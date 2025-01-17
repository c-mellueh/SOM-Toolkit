from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, QPoint, QPointF, Qt

import SOMcreator
from SOMcreator import value_constants
from som_gui import tool

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window import tool as aw_tool
    from PySide6.QtGui import QWheelEvent, QKeyEvent
    from som_gui.plugins.aggregation_window.module.node import ui as node_ui


def key_press_event(event: QKeyEvent, view: Type[aw_tool.View], connection: Type[aw_tool.Connection]) -> None:
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5 and event.key() == Qt.Key.Key_Escape:
        connection.delete_draw_connection()
        view.reset_cursor(view.get_scene_cursor_pos())

    if event.key() == Qt.Key.Key_Delete:
        nodes = view.get_selected_nodes()
        for node in nodes:
            view.remove_node_from_scene(node, view.get_active_scene())


def import_pos_from_project(view: Type[aw_tool.View], project: Type[tool.Project]) -> None:
    view.import_aggregations_from_project(project.get())


def paint_event(view: Type[aw_tool.View], node: Type[aw_tool.Node], connection: Type[aw_tool.Connection],
                project: Type[tool.Project]) -> None:
    scene = view.get_active_scene()
    if scene is None:
        scene, scene_name = view.create_scene(QCoreApplication.translate("Aggregation", "Undefined"))
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


def mouse_move_event(position: QPoint, view: Type[aw_tool.View], node: Type[aw_tool.Node],
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


def mouse_press_event(position: QPoint, view: Type[aw_tool.View], node: Type[aw_tool.Node],
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


def mouse_release_event(position: QPoint, view: Type[aw_tool.View],
                        connection: Type[aw_tool.Connection], search: Type[tool.Search],
                        project: Type[tool.Project]) -> None:
    mouse_mode = view.get_mouse_mode()
    if mouse_mode == 5:  # Handle Connection Drawing
        if connection.is_drawing_started():
            view.create_connection_by_pos(connection.get_draw_node())
            connection.delete_draw_connection()
        else:
            obj = search.search_object(list(project.get().get_objects(filter=True)))
            if obj is not None:
                view.create_child_node(connection.get_draw_node(), obj)

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


def context_menu_requested(pos: QPoint, view: Type[aw_tool.View], node: Type[aw_tool.Node], search: Type[tool.Search],
                           connection: Type[aw_tool.Connection], project: Type[tool.Project],
                           util: Type[tool.Util]) -> None:
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
        menu_list.append([f"{layout}/{ch}", lambda: node.center_nodes(selected_nodes, 0)])
        menu_list.append([f"{layout}/{cv}", lambda: node.center_nodes(selected_nodes, 1)])
        menu_list.append([f"{layout}/{dh}", lambda: node.distribute_by_layer(selected_nodes, 0)])
        menu_list.append([f"{layout}/{dv}", lambda: node.distribute_nodes(selected_nodes, 1)])

    menu_list.append(
        [QCoreApplication.translate("Aggregation", "Modify Info"), lambda: change_header_text(node, search, project)])
    menu_list.append([QCoreApplication.translate("Aggregation", "Reset Info"), lambda: node.reset_title_settings()])

    node_under_mouse = view.get_node_under_mouse()
    if node_under_mouse:
        node_text = QCoreApplication.translate("Aggregation", "Node")
        add = QCoreApplication.translate("Aggregation", "Add Node")
        delete_node = QCoreApplication.translate("Aggregation", "Delete Node")
        delete_nodes = QCoreApplication.translate("Aggregation", "Delete Nodes")

        menu_list.append([f"{node_text}/{add}", lambda: add_node_at_pos(view.map_to_scene(pos), view, search, project)])

        txt = delete_node if len(selected_nodes) == 1 else delete_nodes
        del_text = f"{node_text}/{txt}"
        menu_list.append([del_text, lambda: [view.remove_node_from_scene(n, scene) for n in selected_nodes]])

        connection_type = QCoreApplication.translate("Aggregation", "Connection Type")
        aggregation = QCoreApplication.translate("Aggregation", "Aggregation")
        inheritance = QCoreApplication.translate("Aggregation", "Inheritance")
        if not node.is_root(node_under_mouse):
            menu_list.append([f"{connection_type}/{aggregation}",
                              lambda: node.set_connect_type(node_under_mouse, value_constants.AGGREGATION)])
            menu_list.append([f"{connection_type}/{inheritance}",
                              lambda: node.set_connect_type(node_under_mouse, value_constants.INHERITANCE)])
            menu_list.append([f"{connection_type}/{aggregation}+{inheritance}",
                              lambda: node.set_connect_type(node_under_mouse,
                                                            value_constants.AGGREGATION + value_constants.INHERITANCE)])
    else:
        add = QCoreApplication.translate("Aggregation", "Add Node")

        menu_list.append([add, lambda: add_node_at_pos(view.map_to_scene(pos), view, search, project)])

    menu = util.create_context_menu(menu_list)
    menu.exec(view.get_view().viewport().mapToGlobal(pos))
    paint_event(view, node, connection, project)


def add_node_at_pos(pos, view: Type[aw_tool.View], search: Type[tool.Search], project: Type[tool.Project]) -> None:
    scene = view.get_active_scene()
    obj = search.search_object(list(project.get().get_objects(filter=True)))
    if not obj:
        return
    aggregation = SOMcreator.Aggregation(obj)
    view.add_aggregation_to_import_list(scene, aggregation, pos)


def change_header_text(node: Type[aw_tool.Node], search: Type[tool.Search], project: Type[tool.Project]) -> None:
    searchable_attributes = list()
    search_values = list()
    for attribute in project.get().get_attributes(filter=False):
        value = [attribute.property_set.name, attribute.name]
        if value not in search_values:
            searchable_attributes.append(attribute)
            search_values.append(value)
    attribute = search.search_attribute(searchable_attributes)
    if attribute:
        node.set_title_settings(attribute.property_set.name, attribute.name)


def add_object_to_scene(obj: SOMcreator.Object, scene, parent_node: node_ui.NodeProxy | None, pos: QPoint | None,
                        view: Type[aw_tool.View], connection: Type[aw_tool.Connection], node: Type[aw_tool.Node]):
    if scene is None:
        scene = view.get_active_scene()
    if pos is None:
        pos = QPointF(100., 100.)

    aggregation = SOMcreator.Aggregation(obj)
    new_node = node.create_node(aggregation)
    view.add_node_to_scene(new_node, scene)
    node.set_node_pos(new_node, pos)

    if parent_node is not None:
        con = connection.create_connection(parent_node, new_node, 1)
        view.add_connection_to_scene(con, view.get_active_scene())
    return new_node
