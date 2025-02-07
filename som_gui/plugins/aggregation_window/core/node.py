from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QPointF, Qt, QCoreApplication
from PySide6.QtGui import QPainter, QPalette, QPen
from PySide6.QtWidgets import QTreeWidgetItem, QGraphicsSceneMouseEvent
import logging
import SOMcreator
from som_gui.core import property_set_window as property_set_window_core

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.tool import View, Node, Window
    from som_gui import tool
    from som_gui.plugins.aggregation_window.module.node.ui import (
        Header,
        NodeProxy,
        PropertySetTree,
        Circle,
    )


def rename_identity_text(
    active_node: NodeProxy,
    popups: Type[tool.Popups],
    window: Type[Window],
    node: Type[Node],
) -> None:
    """It pre-fills the input dialog with the current identity text and updates the identity text
    :param active_node: The active node whose identity text is to be renamed.
    :type active_node: NodeProxy
    :param popups: The popups utility for requesting text input from the user.
    :type popups: Type[tool.Popups]
    :param window: The window instance to use as the parent for the input dialog.
    :type window: Type[Window]
    :param node: The node type (not used in the function body).
    :type node: Type[Node]
    :returns: None
    :rtype: None"""

    prefill = active_node.aggregation.get_identity_text()
    title = QCoreApplication.translate("Connection", "Change label")
    request_text = QCoreApplication.translate("Connection", "Enter new label value:")
    parent = window.get_window()
    new_text = popups._request_text_input(title, request_text, prefill, parent)
    if new_text is None:
        return
    active_node.aggregation.set_identity_text(new_text)
    active_node.update()


def pset_tree_double_clicked(
    item: QTreeWidgetItem,
    node: Type[Node],
    property_set_window: Type[tool.PropertySetWindow],
    attribute_table: Type[tool.AttributeTable],
) -> None:
    """
    Handles the event when a tree item is double-clicked in the property set tree.
    This function determines whether the clicked item is an Attribute or a PropertySet,
    and then opens the corresponding property set window. If the item is an Attribute,
    it also activates the attribute in the property set window.
    :param item: The tree item that was double-clicked.
    :type item: QTreeWidgetItem
    :param node: The node associated with the tree item.
    :type node: Type[Node]
    :param property_set_window: The window class for displaying property sets.
    :type property_set_window: Type[tool.PropertySetWindow]
    :param attribute_table: The table class for displaying attributes.
    :type attribute_table: Type[tool.AttributeTable]
    :returns: None
    """

    linked_item = node.get_linked_item(item)
    active_attribute = None
    active_property_set = None
    if isinstance(linked_item, SOMcreator.Attribute):
        active_attribute = linked_item
        active_property_set = linked_item.property_set

    elif isinstance(linked_item, SOMcreator.PropertySet):
        active_property_set = linked_item

    if active_property_set is None:
        return

    window = property_set_window_core.open_pset_window(
        active_property_set, property_set_window, attribute_table
    )
    if active_attribute is None:
        return
    property_set_window_core.activate_attribute(
        active_attribute, window, property_set_window
    )


def header_click(
    header: Header, event: QGraphicsSceneMouseEvent, node: Type[Node]
) -> None:
    selected_node = header.node
    node.set_z_level_of_node(selected_node, node.increment_z_level())
    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
        node.lock_move_direction(True)
        node.set_last_move_direction(None)


def move_header(
    header: Header, event: QGraphicsSceneMouseEvent, view: Type[View], node: Type[Node]
) -> None:
    """
    Moves the header and subsequently the selected nodes by a given difference vector.
    :param header: The header object to be moved.
    :type header: Header
    :param dif: The difference vector by which to move the header and nodes.
    :type dif: QPointF
    :param view: The view object containing the active scene.
    :type view: Type[View]
    :param node: The node object to retrieve nodes from headers and move nodes.
    :type node: Type[Node]
    :return: None
    :rtype: None
    """
    if node.is_move_direction_locked():
        direction = node.get_last_move_direction()
        if direction is None:
            node.set_last_move_direction(event.pos() - event.lastPos())
        if direction == 1:
            event.setPos(QPointF(event.pos().x(), event.lastPos().y()))

        if direction == 2:
            event.setPos(QPointF(event.lastPos().x(), event.pos().y()))
    else:
        node.set_last_move_direction(event.pos() - event.lastPos())
    dif = event.pos() - event.lastPos()
    header.setPos(header.mapToParent(dif))
    selected_nodes = view.get_active_scene().selectedItems()
    active_node = node.get_node_from_header(header)
    for selected_node in selected_nodes:
        if active_node != selected_node:
            selected_node.header.moveBy(dif.x(), dif.y())
        node.move_node(selected_node, dif)
    return event


def paint_header(painter: QPainter, header: Header, node: Type[Node]) -> None:
    """
    Paints the header of a node in the aggregation window.
    Resizes the header to fit the title text.

    :param painter: The painter object used to draw the header.
    :type painter: QPainter
    :param header: The header object that needs to be painted.
    :type header: Header
    :param node: The node type that contains the header.
    :type node: Type[Node]
    :returns: None
    :rtype: None
    """
    active_node = node.get_node_from_header(header)

    logging.debug(f"Paint Header {active_node.aggregation.name} {header.rect()}")
    painter.save()
    painter.restore()
    painter.setBrush(QPalette().base())
    node.set_font_metric(painter.fontMetrics())

    # resize Header
    rect = node.get_header_geometry(header, header.node)
    header.setRect(rect)
    painter.drawRect(rect)

    # write Text into Header
    pset_name, attribute_name = node.get_title_settings()
    rows = node.get_title_rows(active_node, rect.width(), pset_name, attribute_name)
    node.draw_header_texts(painter, header, rows)

    # update Children
    for child_node in node.get_child_nodes(header.node):
        child_node.header.update()


def paint_pset_tree(tree_widget: PropertySetTree, node: Type[Node]) -> None:
    """
    Updates the property set tree widget with the values from the given node.
    This function performs the following steps:

    1. Retrieves the selected node from the tree widget.
    2. Logs the name of the aggregation associated with the selected node.
    3. Adds new values to the property set tree from the node.
    4. Deletes old values from the property set tree that are not present in the new values.

    :param tree_widget: The tree widget representing the property set.
    :type tree_widget: PropertySetTree
    :param node: The node containing the values to be painted on the tree widget.
    :type node: Type[Node]
    :returns: None
    :rtype: None
    """

    selected_node = node.get_node_from_tree_widget(tree_widget)
    logging.debug(f"Paint Property Set Tree {selected_node.aggregation.name}")
    pset_dict = node.add_new_values_to_pset_tree(tree_widget)
    node.delete_old_values_from_pset_tree(tree_widget, pset_dict)


def paint_node(active_node: NodeProxy, node: Type[Node]) -> None:
    """
    Paints the given node on the GUI.

    This function updates the visual representation of a node by setting its
    frame geometry and pen color based on whether it is selected or not.

    :param active_node: The proxy object representing the active node.
    :type active_node: NodeProxy
    :param node: The node class type to be painted.
    :type node: Type[Node]
    :returns: None
    :rtype: None
    """
    logging.debug(f"Paint Node {active_node.aggregation.name}")
    frame = active_node.frame
    frame.setRect(node.get_frame_geometry(active_node))
    if active_node.isSelected():
        frame.setPen(QPalette().accent().color())
    else:
        frame.setPen(QPen(QPalette().text().color()))
    node.update_circle_rect(active_node.circle)


def paint_circle(circle: Circle, node: Type[Node]) -> None:
    node.update_circle_rect(circle)
