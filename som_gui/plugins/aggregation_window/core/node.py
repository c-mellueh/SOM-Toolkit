from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QPointF, Qt,QCoreApplication
from PySide6.QtGui import QPainter, QPalette, QPen
from PySide6.QtWidgets import QTreeWidgetItem
import logging
import SOMcreator
from som_gui.core import property_set_window as property_set_window_core
if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.tool import View, Node,Window
    from som_gui import tool
    from som_gui.plugins.aggregation_window.module.node.ui import Header, NodeProxy, PropertySetTree, Circle

def rename_identity_text(active_node:NodeProxy,  popups: Type[tool.Popups],window:Type[Window],node:Type[Node]) -> None:
    if not active_node.bottom_connections:
        return
    prefill = active_node.aggregation.get_identity_text()
    title = QCoreApplication.translate("Connection", "Change label")
    request_text = QCoreApplication.translate("Connection", "Enter new label value:")
    parent = window.get_window()
    new_text =  popups._request_text_input(title,request_text,prefill,parent)
    if new_text is None:
        return
    active_node.aggregation.set_identity_text(new_text)
    active_node.update()


def pset_tree_double_clicked(item: QTreeWidgetItem, node: Type[Node], property_set_window: Type[tool.PropertySetWindow],
     attribute_table: Type[tool.AttributeTable]) -> None:
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

    window = property_set_window_core.open_pset_window(active_property_set, property_set_window, attribute_table)
    if active_attribute is None:
        return
    property_set_window_core.activate_attribute(active_attribute, window, property_set_window)


def increment_z_of_node(selected_node: NodeProxy, node: Type[Node]) -> None:
    node.set_z_level_of_node(selected_node, node.increment_z_level())


def move_header(
    header: Header, dif: QPointF, view: Type[View], node: Type[Node]
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
    selected_nodes = view.get_active_scene().selectedItems()
    active_node = node.get_node_from_header(header)
    for selected_node in selected_nodes:
        if active_node != selected_node:
            selected_node.header.moveBy(dif.x(), dif.y())
        node.move_node(selected_node, dif)


def paint_header(painter: QPainter, header: Header, node: Type[Node]) -> None:
    logging.debug(f"Paint Header {node.get_node_from_header(header).aggregation.name} {header.rect()}")
    painter.save()
    painter.restore()
    painter.setBrush(QPalette().base())
    rect = node.get_header_geometry(header, header.node)
    pset_name, attribute_name = node.get_title_settings()

    active_node = node.get_node_from_header(header)
    title_rows = node.get_title_rows(painter,active_node,rect.width(),pset_name,attribute_name)
    row_height = painter.fontMetrics().lineSpacing()
    new_height = len(title_rows)*row_height
    rect.setY(-new_height)
    rect.setHeight(new_height)
    header.setRect(rect)
    painter.drawRect(rect)
    node.draw_header_texts(painter,header,title_rows)

    for child_node in node.get_child_nodes(header.node):
        child_node.header.update()
        


def paint_pset_tree(tree_widget: PropertySetTree, node: Type[Node]) -> None:
    selected_node = node.get_node_from_tree_widget(tree_widget)
    logging.debug(f"Paint Property Set Tree {selected_node.aggregation.name}")
    pset_dict = node.add_new_values_to_pset_tree(tree_widget)
    node.delete_old_values_from_pset_tree(tree_widget,pset_dict)


def paint_node(active_node: NodeProxy, node: Type[Node]) -> None:
    logging.debug(f"Paint Node {active_node.aggregation.name}")
    frame = active_node.frame
    frame.setRect(node.get_frame_geometry(frame, active_node))
    if active_node.isSelected():
        frame.setPen(QPalette().accent().color())
    else:
        frame.setPen(QPen(QPalette().text().color()))
    node.update_circle_rect(active_node.circle)

def paint_circle(circle: Circle, node: Type[Node]) -> None:
    node.update_circle_rect(circle)
