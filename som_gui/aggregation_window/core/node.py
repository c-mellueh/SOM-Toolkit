from __future__ import annotations
from typing import TYPE_CHECKING, Type

import SOMcreator
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import View, Window, Node
    from som_gui import tool
    from som_gui.aggregation_window.module.node.ui import Header
    from PySide6.QtGui import QPainter
from SOMcreator.classes import Aggregation
from som_gui.core import property_set_window as property_set_window_core


def add_node(view: Type[View], node: Type[Node]):
    from som_gui.tool import Project as project
    proj = project.get()
    aggregations = list(proj.get_all_aggregations())
    aggregation = aggregations[0]
    scene = view.get_active_scene()
    new_node = node.create_node(aggregation)
    view.add_node_to_scene(new_node, scene)
    node.create_header(new_node, scene)
    node.create_frame(new_node, scene)


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


def node_clicked(selected_node, node: Type[Node]):
    z_level = node.increment_z_level()
    node.set_z_level_of_node(selected_node, z_level)


def header_drag_move(header, dif, node: Type[Node]):
    active_node = node.get_node_from_header(header)
    node.move_node(active_node, dif)


def paint_header(painter: QPainter, header: Header, node: Type[Node]):
    painter.save()
    painter.restore()
    painter.setBrush(Qt.GlobalColor.white)
    painter.drawRect(header.rect())
    active_node = node.get_node_from_header(header)
    pset_name, attribute_name = node.get_title_settings()
    title_text = node.get_title(active_node, pset_name, attribute_name)
    painter.drawText(header.rect(), Qt.AlignmentFlag.AlignCenter, title_text)
