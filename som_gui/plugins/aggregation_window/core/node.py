from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPalette, QPen
from PySide6.QtWidgets import QTreeWidgetItem

import SOMcreator
from som_gui.core import property_set_window as property_set_window_core

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.tool import View, Node
    from som_gui import tool
    from som_gui.plugins.aggregation_window.module.node.ui import Header, NodeProxy, PropertySetTree, Circle


def pset_tree_double_clicked(item: QTreeWidgetItem, node: Type[Node], property_set_window: Type[tool.PropertySetWindow],
                             attribute: Type[tool.Attribute], attribute_table: Type[tool.AttributeTable]) -> None:
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
    property_set_window_core.activate_attribute(active_attribute, window, attribute, property_set_window)


def node_clicked(selected_node: NodeProxy, node: Type[Node]) -> None:
    node.set_z_level_of_node(selected_node, node.increment_z_level())


def header_drag_move(header: Header, dif: QPointF, view: Type[View], node: Type[Node]) -> None:
    selected_nodes = view.get_active_scene().selectedItems()
    active_node = node.get_node_from_header(header)
    for selected_node in selected_nodes:
        if active_node != selected_node:
            selected_node.header.moveBy(dif.x(), dif.y())
        node.move_node(selected_node, dif)


def paint_header(painter: QPainter, header: Header, node: Type[Node]) -> None:
    painter.save()
    painter.restore()

    painter.setBrush(QPalette().base())
    rect = node.get_header_geometry(header, header.node)
    header.setRect(rect)
    painter.drawRect(rect)
    active_node = node.get_node_from_header(header)
    pset_name, attribute_name = node.get_title_settings()
    title_text = node.get_title(active_node, pset_name, attribute_name)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, title_text)


def paint_pset_tree(tree_widget: PropertySetTree, node: Type[Node]) -> None:
    selected_node = node.get_node_from_tree_widget(tree_widget)
    obj = selected_node.aggregation.object
    ir = tree_widget.invisibleRootItem()
    property_set_dict = node.get_pset_subelement_dict(ir)

    # add new property_sets and attributes
    for property_set in obj.get_property_sets(filter=True):
        if property_set not in property_set_dict:
            property_set_item = node.add_property_set_to_tree(property_set, tree_widget)
            property_set_dict[property_set] = property_set_item

        property_set_item = property_set_dict[property_set]
        if property_set_item.text(0) != property_set.name:
            property_set_item.setText(0, property_set.name)

        attribute_dict = node.get_pset_subelement_dict(property_set_item)

        for attribute in property_set.get_attributes(filter=True):
            if attribute not in attribute_dict:
                attribute_item = node.add_attribute_to_property_set_tree(attribute, property_set_item)
                attribute_dict[attribute] = attribute_item
            attribute_item = attribute_dict[attribute]
            if attribute_item.text(0) != attribute.name:
                attribute_item.setText(0, attribute.name)

    # delete old property_sets and attributes
    for property_set, pset_item in property_set_dict.items():
        if property_set not in obj.get_property_sets(filter=True):
            ir.removeChild(pset_item)
            continue

        attribute_dict = node.get_pset_subelement_dict(pset_item)
        for attribute, attribute_item in attribute_dict.items():
            if attribute not in property_set.get_attributes(filter=True):
                pset_item.removeChild(attribute_item)


def paint_node(active_node: NodeProxy, node: Type[Node]) -> None:
    frame = active_node.frame
    frame.setRect(node.get_frame_geometry(frame, active_node))
    if active_node.isSelected():
        frame.setPen(QPalette().accent().color())
    else:
        frame.setPen(QPen(QPalette().text().color()))

    node.update_circle_rect(active_node.circle)


def paint_circle(circle: Circle, node: Type[Node]) -> None:
    node.update_circle_rect(circle)
