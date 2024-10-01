from __future__ import annotations
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QSize, QPointF
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import QRectF

import SOMcreator
from SOMcreator import value_constants

import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window.module.node import constants as node_constants, ui as node_ui
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.node.prop import NodeProperties


class Node(som_gui.plugins.aggregation_window.core.tool.Node):
    @classmethod
    def get_properties(cls) -> NodeProperties:
        return som_gui.NodeProperties

    @classmethod
    def set_z_level_of_node(cls, node: node_ui.NodeProxy, z_level: int) -> None:
        node.setZValue(z_level)
        node.frame.setZValue(z_level)
        node.header.setZValue(z_level)
        node.resize_rect.setZValue(z_level)
        node.circle.setZValue(z_level)

    @classmethod
    def increment_z_level(cls) -> int:
        cls.get_properties().z_level += 1
        return cls.get_properties().z_level

    @classmethod
    def get_z_level(cls) -> int:
        return cls.get_properties().z_level

    @classmethod
    def add_property_set_to_tree(cls, property_set: SOMcreator.PropertySet,
                                 tree_widget: node_ui.PropertySetTree) -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setText(0, property_set.name)
        item.setData(0, CLASS_REFERENCE, property_set)
        tree_widget.addTopLevelItem(item)
        return item

    @classmethod
    def get_pset_subelement_dict(cls, item: QTreeWidgetItem) -> dict[
        SOMcreator.PropertySet | SOMcreator.Attribute, QTreeWidgetItem]:
        return {cls.get_linked_item(item.child(i)): item.child(i) for i in range(item.childCount())}

    @classmethod
    def add_attribute_to_property_set_tree(cls, attribute: SOMcreator.Attribute,
                                           property_set_item: QTreeWidgetItem) -> QTreeWidgetItem:
        attribute_item = QTreeWidgetItem()
        attribute_item.setText(0, attribute.name)
        attribute_item.setData(0, CLASS_REFERENCE, attribute)
        property_set_item.addChild(attribute_item)
        return attribute_item

    @classmethod
    def create_tree_widget(cls, node: node_ui.NodeProxy) -> node_ui.PropertySetTree:
        widget = node_ui.PropertySetTree()
        widget.setHeaderLabel("Name")
        widget.node = node
        return widget

    @classmethod
    def create_circle(cls, node: node_ui.NodeProxy) -> node_ui.Circle:
        circle = node_ui.Circle()
        circle.node = node
        circle.text.node = node
        node.circle = circle
        return circle

    @classmethod
    def create_node(cls, aggregation: SOMcreator.Aggregation) -> node_ui.NodeProxy:
        node = node_ui.NodeProxy()
        node_widget = node_ui.NodeWidget()
        node.setWidget(node_widget)
        node_widget.setMinimumSize(QSize(250, 150))
        node.aggregation = aggregation
        node.widget().layout().insertWidget(0, cls.create_tree_widget(node))
        cls.create_header(node)
        cls.create_frame(node)
        cls.create_resize_rect(node)
        cls.create_circle(node)
        cls.set_z_level_of_node(node, cls.get_z_level() + 1)
        return node

    @classmethod
    def get_header_geometry(cls, header, node: node_ui.NodeProxy) -> QRectF:
        line_width = header.pen().width()  # if ignore Line width: box of Node and Header won't match
        x = line_width / 2
        width = node.widget().width() - line_width
        height = node_constants.HEADER_HEIGHT
        return QRectF(x, -height, width, height)

    @classmethod
    def get_frame_geometry(cls, frame: node_ui.Frame, node: node_ui.NodeProxy) -> QRectF:
        line_width = frame.pen().width()
        rect = node.rect()
        rect.setWidth(rect.width() - line_width / 2)
        rect.setHeight(rect.height())
        rect.setY(rect.y() - node_constants.HEADER_HEIGHT)
        rect.setX(rect.x() + frame.pen().width() / 2)
        return rect

    @classmethod
    def create_header(cls, node: node_ui.NodeProxy) -> node_ui.Header:
        header = node_ui.Header()

        header.setRect(cls.get_header_geometry(header, node))
        node.header = header
        header.node = node
        return header

    @classmethod
    def create_frame(cls, node: node_ui.NodeProxy) -> node_ui.Frame:
        frame = node_ui.Frame()
        rect = cls.get_frame_geometry(frame, node)

        frame.setRect(rect)
        node.frame = frame
        frame.node = node
        return frame

    @classmethod
    def create_resize_rect(cls, node: node_ui.NodeProxy) -> node_ui.ResizeRect:
        size = node_constants.RESIZE_RECT_SIZE
        frame_rect = node.rect()
        x, y = frame_rect.width() - size / 2, frame_rect.height() - size / 2
        resize_rect = node_ui.ResizeRect()
        resize_rect.setRect(QRectF(x, y, size, size))
        node.resize_rect = resize_rect
        resize_rect.node = node
        return resize_rect

    @classmethod
    def get_linked_item(cls, pset_tree_item: QTreeWidgetItem) -> SOMcreator.PropertySet | SOMcreator.Attribute:
        return pset_tree_item.data(0, CLASS_REFERENCE)

    @classmethod
    def get_node_from_header(cls, header: node_ui.Header) -> node_ui.NodeProxy:
        return header.node

    @classmethod
    def get_frame_from_node(cls, node: node_ui.NodeProxy) -> node_ui.Frame:
        return node.frame

    @classmethod
    def move_node(cls, node: node_ui.NodeProxy, dif: QPointF) -> None:
        node.moveBy(dif.x(), dif.y())
        frame = cls.get_frame_from_node(node)
        frame.moveBy(dif.x(), dif.y())
        node.resize_rect.moveBy(dif.x(), dif.y())
        cls.update_circle_rect(node.circle)

    @classmethod
    def set_node_pos(cls, node: node_ui.NodeProxy, pos: QPointF) -> None:
        dif = pos - node.header.scenePos()
        node.header.moveBy(dif.x(), dif.y())
        cls.move_node(node, dif)

    @classmethod
    def update_circle_rect(cls, circle: node_ui.Circle) -> None:
        x = circle.node.sceneBoundingRect().center().x() - circle.DIAMETER / 2
        y = circle.node.sceneBoundingRect().bottom() - circle.DIAMETER / 2
        circle.setRect(QRectF(x, y, circle.DIAMETER, circle.DIAMETER))
        scene_pos = aw_tool.View.get_scene_cursor_pos()
        frame = circle.node.frame
        margin = 1.
        bounding_rect = frame.sceneBoundingRect().adjusted(-margin, -margin, margin, margin)
        circle.show() if bounding_rect.contains(scene_pos) else circle.hide()
        circle.text.setX(x + 4.5)
        circle.text.setY(y)

    @classmethod
    def get_id_group(cls, node: node_ui.NodeProxy) -> str:
        abbrev_list = list()

        def iter_id(element: SOMcreator.Aggregation):
            if element.parent_connection in (value_constants.AGGREGATION,
                                             value_constants.AGGREGATION + value_constants.INHERITANCE):
                abbrev_list.append(element.parent.object.abbreviation)
            if not element.is_root:
                iter_id(element.parent)

        if node.aggregation.is_root:
            return ""

        iter_id(node.aggregation)
        return "_xxx_".join(reversed(abbrev_list)) + "_xxx"

    @classmethod
    def get_identity(cls, node: node_ui.NodeProxy):
        return cls.get_id_group(node) + "_" + node.aggregation.object.abbreviation + "_xxx"

    @classmethod
    def get_title(cls, node: node_ui.NodeProxy, pset_name: str, attribute_name: str) -> str:
        aggregation = cls.get_aggregation_from_node(node)
        if not (pset_name and attribute_name):
            base_text = f"{aggregation.name} ({aggregation.object.abbreviation})"

            if aggregation.is_root:
                title = base_text
            else:
                title = f"{base_text}\nidGruppe: {cls.get_id_group(node)}"
            return title
        undef = f"{aggregation.name}\n{attribute_name}: undefined"
        obj = aggregation.object
        pset = obj.get_property_set_by_name(pset_name)
        if pset is None:
            return undef
        attribute = pset.get_attribute_by_name(attribute_name)
        if attribute is None:
            return undef

        if len(attribute.value) == 0:
            return undef
        return f"{aggregation.name}\n{attribute_name}: {attribute.value[0]}"

    @classmethod
    def get_aggregation_from_node(cls, node: node_ui.NodeProxy) -> SOMcreator.Aggregation:
        return node.aggregation

    @classmethod
    def get_title_settings(cls) -> tuple[str, str]:
        return cls.get_properties().title_pset, cls.get_properties().title_attribute

    @classmethod
    def set_title_settings(cls, pset_name: str, attribute_name: str) -> None:
        cls.get_properties().title_pset, cls.get_properties().title_attribute = pset_name, attribute_name

    @classmethod
    def reset_title_settings(cls) -> None:
        cls.get_properties().title_pset, cls.get_properties().title_attribute = None, None

    @classmethod
    def get_node_from_tree_widget(cls, tree_widget: node_ui.PropertySetTree) -> node_ui.NodeProxy:
        return tree_widget.node

    @classmethod
    def is_node_connected_to_node(cls, node1: node_ui.NodeProxy, node2: node_ui.NodeProxy) -> bool:
        if node1.top_connection and node1.top_connection.top_node == node2:
            return True
        if node2.top_connection and node2.top_connection.top_node == node1:
            return True
        return False

    @classmethod
    def item_is_resize_rect(cls, item: Any) -> bool:
        return isinstance(item, node_ui.ResizeRect)

    @classmethod
    def item_is_header(cls, item: Any) -> bool:
        return isinstance(item, node_ui.Header)

    @classmethod
    def item_is_frame(cls, item: Any) -> bool:
        return isinstance(item, node_ui.Frame)

    @classmethod
    def item_is_circle(cls, item: Any) -> bool:
        return isinstance(item, node_ui.Circle)

    @classmethod
    def item_is_circle_text(cls, item: Any) -> bool:
        return isinstance(item, node_ui.PlusText)

    @classmethod
    def resize_node(cls, node: node_ui.NodeProxy, last_pos: QPointF, new_pos: QPointF) -> None:
        dif = new_pos - last_pos
        dx, dy = dif.x(), dif.y()
        geom = node.geometry()
        height = geom.height() + dy
        width = geom.width() + dx
        if height >= node.minimumHeight():
            geom.setHeight(height)
            node.resize_rect.moveBy(0., dy)
        if width >= node.minimumWidth():
            geom.setWidth(width)
            node.resize_rect.moveBy(dx, 0.)
        node.setGeometry(geom)
        node.circle.update()

    @classmethod
    def set_connect_type(cls, node: node_ui.NodeProxy, parent_con_type: int) -> None:
        node.aggregation.parent_connection = parent_con_type

    @classmethod
    def is_root(cls, node: node_ui.NodeProxy) -> bool:
        return node.aggregation.is_root

    @classmethod
    def center_nodes(cls, nodes: set[node_ui.NodeProxy], orientation: int) -> None:
        func_name = "x" if orientation == 0 else "y"
        pos_list = [getattr(node.geometry(), func_name)() for node in nodes]
        center = min(pos_list) + (max(pos_list) - min(pos_list)) / 2
        for node in nodes:
            node_pos = getattr(node.geometry(), func_name)()
            dif = QPointF(center - node_pos, 0.) if orientation == 0 else QPointF(0., center - node_pos)
            cls.move_node(node, dif)
            node.header.moveBy(dif.x(), dif.y())

    @classmethod
    def distribute_by_layer(cls, nodes: set[node_ui.NodeProxy], orientation: int) -> None:
        node_dict = {cls.get_node_level(node): set() for node in nodes}
        [node_dict[cls.get_node_level(node)].add(node) for node in nodes]
        for level, node_set in node_dict.items():
            cls.distribute_nodes(node_set, orientation)

    @classmethod
    def distribute_nodes(cls, nodes: set[node_ui.NodeProxy], orientation: int) -> None:
        if len(nodes) < 2:
            return
        func_name = "x" if orientation == 0 else "y"

        pos_list = [getattr(node.geometry().center(), func_name)() for node in nodes]
        border_1, border_2 = min(pos_list), max(pos_list)
        full_length = border_2 - border_1
        distance_between_nodes = full_length / (len(nodes) - 1)

        for index, node in enumerate(sorted(nodes, key=lambda node: getattr(node.geometry().center(), func_name)())):
            new_pos = border_1 + index * distance_between_nodes
            old_pos = getattr(node.geometry().center(), func_name)()
            dif = QPointF(new_pos - old_pos, 0.) if orientation == 0 else QPointF(0., new_pos - old_pos)
            cls.move_node(node, dif)
            node.header.moveBy(dif.x(), dif.y())

    @classmethod
    def get_node_level(cls, node: node_ui.NodeProxy) -> int:
        parent_node = cls.get_parent_node(node)
        if parent_node is not None:
            return cls.get_node_level(parent_node) + 1
        return 0

    @classmethod
    def get_parent_node(cls, node: node_ui.NodeProxy) -> node_ui.NodeProxy | None:
        tc = node.top_connection
        if not tc:
            return None
        return tc.top_node
