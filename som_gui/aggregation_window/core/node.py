from __future__ import annotations
from typing import TYPE_CHECKING, Type

import SOMcreator
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import View, Window, Node
    from som_gui import tool
    from som_gui.aggregation_window.module.node.ui import Header, NodeProxy, PropertySetTree, ResizeRect
    from PySide6.QtGui import QPainter, QPainterPath
    from PySide6.QtCore import QPointF
    from PySide6.QtWidgets import QTreeWidget
from SOMcreator.classes import Aggregation
from som_gui.core import property_set_window as property_set_window_core


def pset_tree_double_clicked(item, node: Type[Node], property_set_window: Type[tool.PropertySetWindow],
                             attribute: Type[tool.Attribute], attribute_table: Type[tool.AttributeTable]):
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


def node_clicked(selected_node: NodeProxy, node: Type[Node]):
    z_level = node.increment_z_level()
    node.set_z_level_of_node(selected_node, z_level)


def header_drag_move(header: Header, dif: QPointF, node: Type[Node]):
    active_node = node.get_node_from_header(header)
    node.move_node(active_node, dif)


def paint_header(painter: QPainter, header: Header, node: Type[Node]):
    painter.save()
    painter.restore()
    painter.setBrush(Qt.GlobalColor.white)
    rect = node.get_header_geometry(header, header.node)
    header.setRect(rect)
    painter.drawRect(rect)
    active_node = node.get_node_from_header(header)
    pset_name, attribute_name = node.get_title_settings()
    title_text = node.get_title(active_node, pset_name, attribute_name)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, title_text)


def paint_pset_tree(tree_widget: PropertySetTree, node: Type[Node]):
    selected_node = node.get_node_from_tree_widget(tree_widget)
    obj = selected_node.aggregation.object
    ir = tree_widget.invisibleRootItem()
    property_set_dict = node.get_pset_subelement_dict(ir)

    # add new property_sets and attributes
    for property_set in obj.property_sets:
        if property_set not in property_set_dict:
            property_set_item = node.add_property_set_to_tree(property_set, tree_widget)
            property_set_dict[property_set] = property_set_item

        property_set_item = property_set_dict[property_set]
        if property_set_item.text(0) != property_set.name:
            property_set_item.setText(0, property_set.name)

        attribute_dict = node.get_pset_subelement_dict(property_set_item)

        for attribute in property_set.attributes:
            if attribute not in attribute_dict:
                attribute_item = node.add_attribute_to_property_set_tree(attribute, property_set_item)
                attribute_dict[attribute] = attribute_item
            attribute_item = attribute_dict[attribute]
            if attribute_item.text(0) != attribute.name:
                attribute_item.setText(0, attribute.name)

    # delete old property_sets and attributes
    for property_set, pset_item in property_set_dict.items():
        if property_set not in obj.property_sets:
            ir.removeChild(pset_item)
            continue

        attribute_dict = node.get_pset_subelement_dict(pset_item)
        for attribute, attribute_item in attribute_dict.items():
            if attribute not in property_set.attributes:
                pset_item.removeChild(attribute_item)


def paint_node(active_node: NodeProxy, node: Type[Node]):
    frame = active_node.frame
    frame.setRect(node.get_frame_geometry(frame, active_node))


def hover_enter_resize_rect(resize_rect: ResizeRect, view: Type[View]):
    view.set_cursor_style(Qt.CursorShape.SizeFDiagCursor)


def hover_leave_resize_rect(resize_rect: ResizeRect, view: Type[View]):
    view.reset_cursor_style()


def hover_enter_header(header: Header, view: Type[View]):
    view.set_cursor_style(Qt.CursorShape.OpenHandCursor)


def hover_leave_header(header: Header, view: Type[View]):
    view.reset_cursor_style()
