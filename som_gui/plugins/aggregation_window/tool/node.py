from __future__ import annotations
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QSize, QPointF, QRectF, QCoreApplication, Qt
from PySide6.QtWidgets import QTreeWidgetItem, QVBoxLayout
from PySide6.QtGui import QPainter, QFontMetrics, QFont
import logging
import SOMcreator
from SOMcreator import value_constants

import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window.module.node import (
    constants as node_constants,
    ui as node_ui,
)
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
        """
        Set the Z level of the given node and its components.

        This method updates the Z level (stacking order) of the specified node and its
        associated graphical components (frame, header, resize rectangle, and circle).

        :param node_ui.NodeProxy node: The node whose Z level is to be set.
        :param int z_level: The Z level to set for the node and its components.
        :returns: None
        :rtype: None
        """
        node.setZValue(z_level)
        node.frame.setZValue(z_level)
        node.header.setZValue(z_level)
        node.resize_rect.setZValue(z_level)
        node.circle.setZValue(z_level)

    @classmethod
    def increment_z_level(cls) -> int:
        """
        Increments the z_level property of the class by 1.
        :return: The updated z_level value.
        :rtype: int
        """
        cls.get_properties().z_level += 1
        return cls.get_properties().z_level

    @classmethod
    def get_z_level(cls) -> int:
        return cls.get_properties().z_level

    @classmethod
    def add_property_set_to_tree(
        cls,
        property_set: SOMcreator.SOMPropertySet,
        tree_widget: node_ui.PropertySetTree,
    ) -> QTreeWidgetItem:
        """
        Add a property set to the tree widget.

        This method creates a new QTreeWidgetItem for the given property set and adds it
        to the specified tree widget. The item's text is set to the name of the property
        set, and its data is set to reference the property set.

        :param property_set: The property set to add to the tree.
        :type property_set: SOMcreator.PropertySet
        :param tree_widget: The tree widget to which the property set item will be added.
        :type tree_widget: node_ui.PropertySetTree
        :return: The created QTreeWidgetItem representing the property set.
        :rtype: QTreeWidgetItem
        """
        item = QTreeWidgetItem()
        item.setText(0, property_set.name)
        item.setData(0, CLASS_REFERENCE, property_set)
        tree_widget.addTopLevelItem(item)
        return item

    @classmethod
    def get_pset_subelement_dict(
        cls, item: QTreeWidgetItem
    ) -> dict[SOMcreator.SOMPropertySet | SOMcreator.SOMProperty, QTreeWidgetItem]:
        """
        Generate a dictionary mapping property sets or properties to their corresponding tree widget items.

        This method iterates over the children of the given QTreeWidgetItem and creates a dictionary
        where the keys are the linked property sets or properties, and the values are the corresponding
        QTreeWidgetItem instances.

        :param item: The QTreeWidgetItem whose children are to be processed.
        :type item: QTreeWidgetItem
        :return: A dictionary mapping property sets or properties to their corresponding tree widget items.
        :rtype: dict[SOMcreator.PropertySet | SOMcreator.SOMProperty, QTreeWidgetItem]
        """
        return {
            cls.get_linked_item(item.child(i)): item.child(i)
            for i in range(item.childCount())
        }

    @classmethod
    def add_property_to_property_set_tree(
        cls, som_property: SOMcreator.SOMProperty, property_set_item: QTreeWidgetItem
    ) -> QTreeWidgetItem:
        """
        Add an property to a property set tree item.

        This method creates a new QTreeWidgetItem for the given property and adds it
        as a child to the specified property set item. The item's text is set to the
        name of the property, and its data is set to reference the property.

        :param property: The property to add to the property set tree item.
        :type property: SOMcreator.SOMProperty
        :param property_set_item: The property set item to which the property item will be added.
        :type property_set_item: QTreeWidgetItem
        :return: The created QTreeWidgetItem representing the property.
        :rtype: QTreeWidgetItem
        """
        item = QTreeWidgetItem()
        item.setText(0, som_property.name)
        item.setData(0, CLASS_REFERENCE, som_property)
        property_set_item.addChild(item)
        return item

    @classmethod
    def create_tree_widget(cls, node: node_ui.NodeProxy) -> node_ui.PropertySetTree:
        """
        Create a tree widget for a node.

        This method creates a new PropertySetTree widget, sets its header label to "Name",
        and associates it with the given node.

        :param node: The node for which to create the tree widget.
        :type node: node_ui.NodeProxy
        :return: The created PropertySetTree widget.
        :rtype: node_ui.PropertySetTree
        """
        widget = node_ui.PropertySetTree()
        widget.setHeaderLabel("Name")
        widget.node = node
        return widget

    @classmethod
    def create_circle(cls, node: node_ui.NodeProxy) -> node_ui.Circle:
        """
        Create a circle for a node.

        This method creates a new Circle instance, associates it with the given node,
        and sets the node's circle property to the created circle. The Circle will contain the "+" sign.

        :param node: The node for which to create the circle.
        :type node: node_ui.NodeProxy
        :return: The created Circle instance.
        :rtype: node_ui.Circle
        """
        circle = node_ui.Circle()
        circle.node = node
        circle.text.node = node
        node.circle = circle
        return circle

    @classmethod
    def create_node(cls, aggregation: SOMcreator.SOMAggregation) -> node_ui.NodeProxy:
        """
        Create a node for an aggregation.

        This method creates a new NodeProxy instance, sets up its widget, header, frame,
        resize rectangle, and circle, and sets its Z level.

        :param aggregation: The aggregation for which to create the node.
        :type aggregation: SOMcreator.Aggregation
        :return: The created NodeProxy instance.
        :rtype: node_ui.NodeProxy
        """
        node = node_ui.NodeProxy()
        node_widget = node_ui.NodeWidget()
        node.setWidget(node_widget)
        node_widget.setMinimumSize(QSize(250, 150))
        node.aggregation = aggregation
        tree_widget = cls.create_tree_widget(node)
        layout: QVBoxLayout = node.widget().layout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(node.spacer)
        layout.insertWidget(1, tree_widget)
        cls.create_header(node)
        cls.create_frame(node)
        cls.create_resize_rect(node)
        cls.create_circle(node)
        cls.set_z_level_of_node(node, cls.get_z_level() + 1)
        return node

    @classmethod
    def get_header_geometry(cls, header, node: node_ui.NodeProxy) -> QRectF:
        """
        Get the geometry of a header for a node.

        This method calculates and returns the geometry of the header based on the node's
        widget size and the header's line width.

        :param header: The header for which to get the geometry.
        :type header: node_ui.Header
        :param node: The node associated with the header.
        :type node: node_ui.NodeProxy
        :return: The calculated geometry of the header.
        :rtype: QRectF
        """
        font_metric = cls.get_font_metric()
        line_width = header.pen().width()
        width = node.widget().width() - line_width
        pset_name, property_name = cls.get_title_settings()
        row_height = font_metric.lineSpacing()
        rows = cls.get_title_rows(node, width, pset_name, property_name)
        height = len(rows) * row_height

        x = line_width / 2
        y = 0
        return QRectF(x, y, width, height)

    @classmethod
    def get_frame_geometry(cls, node: node_ui.NodeProxy) -> QRectF:
        """
        Get the geometry of a frame for a node.

        This method calculates and returns the geometry of the frame based on the node's
        rectangle and the frame's line width.

        :param frame: The frame for which to get the geometry.
        :type frame: node_ui.Frame
        :param node: The node associated with the frame.
        :type node: node_ui.NodeProxy
        :return: The calculated geometry of the frame.
        :rtype: QRectF
        """
        frame = cls.get_frame_from_node(node)
        line_width = frame.pen().width()
        rect = node.rect()
        rect.setWidth(rect.width() - line_width / 2)
        rect.setHeight(rect.height())
        rect.setY(rect.y())
        rect.setX(rect.x() + frame.pen().width() / 2)
        return rect

    @classmethod
    def create_header(cls, node: node_ui.NodeProxy) -> node_ui.Header:
        """
        Create a header for a node.

        This method creates a new Header instance, sets its geometry based on the node,
        and associates it with the node.

        :param node: The node for which to create the header.
        :type node: node_ui.NodeProxy
        :return: The created Header instance.
        :rtype: node_ui.Header
        """
        header = node_ui.Header()
        header.setRect(cls.get_header_geometry(header, node))
        node.header = header
        header.node = node
        return header

    @classmethod
    def create_frame(cls, node: node_ui.NodeProxy) -> node_ui.Frame:
        """
        Create a frame for a node.

        This method creates a new Frame instance, sets its geometry based on the node,
        and associates it with the node.

        :param node: The node for which to create the frame.
        :type node: node_ui.NodeProxy
        :return: The created Frame instance.
        :rtype: node_ui.Frame
        """
        frame = node_ui.Frame()
        node.frame = frame
        frame.node = node
        rect = cls.get_frame_geometry(node)
        frame.setRect(rect)
        return frame

    @classmethod
    def create_resize_rect(cls, node: node_ui.NodeProxy) -> node_ui.ResizeRect:
        """
        Create a resize rectangle for a node.

        This method creates a new ResizeRect instance, sets its geometry based on the node,
        and associates it with the node.

        :param node: The node for which to create the resize rectangle.
        :type node: node_ui.NodeProxy
        :return: The created ResizeRect instance.
        :rtype: node_ui.ResizeRect
        """
        size = node_constants.RESIZE_RECT_SIZE
        frame_rect = node.rect()
        x, y = frame_rect.width() - size / 2, frame_rect.height() - size / 2
        resize_rect = node_ui.ResizeRect()
        resize_rect.setRect(QRectF(x, y, size, size))
        node.resize_rect = resize_rect
        resize_rect.node = node
        return resize_rect

    @classmethod
    def get_linked_item(
        cls, pset_tree_item: QTreeWidgetItem
    ) -> SOMcreator.SOMPropertySet | SOMcreator.SOMProperty:
        """
        Get the linked item from a property set tree item.

        This method retrieves the data associated with the given property set tree item,
        which can be either a PropertySet or a Property.

        :param pset_tree_item: The property set tree item from which to get the linked item.
        :type pset_tree_item: QTreeWidgetItem
        :return: The linked item, either a PropertySet or a Propert.
        :rtype: SOMcreator.PropertySet | SOMcreator.SOMProperty
        """
        return pset_tree_item.data(0, CLASS_REFERENCE)

    @classmethod
    def get_node_from_header(cls, header: node_ui.Header) -> node_ui.NodeProxy:
        """
        Get the node associated with a header.

        This method retrieves the node associated with the given header.

        :param header: The header from which to get the associated node.
        :type header: node_ui.Header
        :return: The node associated with the header.
        :rtype: node_ui.NodeProxy
        """
        return header.node

    @classmethod
    def get_frame_from_node(cls, node: node_ui.NodeProxy) -> node_ui.Frame:
        """
        Get the frame associated with a node.

        This method retrieves the frame associated with the given node.

        :param node: The node from which to get the associated frame.
        :type node: node_ui.NodeProxy
        :return: The frame associated with the node.
        :rtype: node_ui.Frame
        """
        return node.frame

    @classmethod
    def move_node(cls, node: node_ui.NodeProxy, dif: QPointF) -> None:
        """
        Move a node by a given difference.

        This method moves the node and its associated components (frame, resize rectangle, and circle)
        by the specified difference in position.

        :param node: The node to move.
        :type node: node_ui.NodeProxy
        :param dif: The difference in position by which to move the node.
        :type dif: QPointF
        :return: None
        """

        node.moveBy(dif.x(), dif.y())
        frame = cls.get_frame_from_node(node)
        frame.moveBy(dif.x(), dif.y())
        node.resize_rect.moveBy(dif.x(), dif.y())
        cls.update_circle_rect(node.circle)

    @classmethod
    def set_node_pos(cls, node: node_ui.NodeProxy, pos: QPointF) -> None:
        """
        Set the position of a node.

        This method sets the position of the node and its header to the specified position.

        :param node: The node to set the position for.
        :type node: node_ui.NodeProxy
        :param pos: The position to set for the node.
        :type pos: QPointF
        :return: None
        """
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
        margin = 1.0
        bounding_rect = frame.sceneBoundingRect().adjusted(
            -margin, -margin, margin, margin
        )
        circle.show() if bounding_rect.contains(scene_pos) else circle.hide()
        circle.text.setX(x + 4.5)
        circle.text.setY(y)

    @classmethod
    def split_text(cls, text: str, seperator: str, max_width: int) -> list[str]:
        font_metrics = cls.get_font_metric()
        lines = []
        current_line = ""
        for word in text.split(seperator):
            if font_metrics.horizontalAdvance(current_line + " " + word) <= max_width:
                current_line += seperator + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())
        lines[0] = lines[0][1:]
        return lines

    @classmethod
    def draw_header_texts(
        cls, painter: QPainter, header: node_ui.Header, lines: list[str]
    ):
        rect = header.rect()
        y_offset = rect.y()

        max_width = rect.width()
        line_height = painter.fontMetrics().lineSpacing()
        for line in lines:
            painter.drawText(
                rect.x(),
                y_offset,
                max_width,
                line_height,
                Qt.AlignmentFlag.AlignCenter,
                line,
            )
            y_offset += line_height

    @classmethod
    def get_title_rows(
        cls,
        node: node_ui.NodeProxy,
        max_width: float,
        pset_name: str | None = None,
        property_name: str | None = None,
    ) -> list[str]:
        aggregation = cls.get_aggregation_from_node(node)
        if not (pset_name and property_name):
            base_text = (
                f"{aggregation.som_class.name} ({aggregation.som_class.abbreviation})"
            )
            id_text = QCoreApplication.translate("Aggregation Window", "id: {}").format(
                node.aggregation.identity()
            )
            id_texts = cls.split_text(id_text, "_", max_width)
            return [base_text] + id_texts
        undef = [f"{aggregation.name}\n{property_name}: undefined"]
        obj = aggregation.som_class
        pset = obj.get_property_set_by_name(pset_name)
        if pset is None:
            return undef
        som_property = pset.get_property_by_name(property_name)
        if som_property is None:
            return undef

        if len(som_property.allowed_values) == 0:
            return undef
        return [f"{aggregation.name}\n{property_name}: {som_property.allowed_values[0]}"]

    @classmethod
    def get_aggregation_from_node(
        cls, node: node_ui.NodeProxy
    ) -> SOMcreator.SOMAggregation:
        return node.aggregation

    @classmethod
    def get_title_settings(cls) -> tuple[str, str]:
        return cls.get_properties().title_pset, cls.get_properties().title_property

    @classmethod
    def set_title_settings(cls, pset_name: str, property_name: str) -> None:
        cls.get_properties().title_pset, cls.get_properties().title_property = (
            pset_name,
            property_name,
        )

    @classmethod
    def reset_title_settings(cls) -> None:
        cls.get_properties().title_pset, cls.get_properties().title_property = (
            None,
            None,
        )

    @classmethod
    def get_node_from_tree_widget(
        cls, tree_widget: node_ui.PropertySetTree
    ) -> node_ui.NodeProxy:
        return tree_widget.node

    @classmethod
    def is_node_connected_to_node(
        cls, node1: node_ui.NodeProxy, node2: node_ui.NodeProxy
    ) -> bool:
        if node1.top_connection and node1.top_connection.top_node == node2:
            return True
        if node2.top_connection and node2.top_connection.top_node == node1:
            return True
        return False

    @classmethod
    def item_is_resize_rect(cls, item: Any) -> bool:
        return isinstance(item, node_ui.ResizeRect)

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
    def resize_node(
        cls, node: node_ui.NodeProxy, last_pos: QPointF, new_pos: QPointF
    ) -> None:
        dif = new_pos - last_pos
        dx, dy = dif.x(), dif.y()
        geom = node.geometry()
        height = geom.height() + dy
        width = geom.width() + dx
        if height >= node.minimumHeight():
            geom.setHeight(height)
            node.resize_rect.moveBy(0.0, dy)
        if width >= node.minimumWidth():
            geom.setWidth(width)
            node.resize_rect.moveBy(dx, 0.0)
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
            dif = (
                QPointF(center - node_pos, 0.0)
                if orientation == 0
                else QPointF(0.0, center - node_pos)
            )
            cls.move_node(node, dif)
            node.header.moveBy(dif.x(), dif.y())

    @classmethod
    def distribute_by_layer(
        cls, nodes: set[node_ui.NodeProxy], orientation: int
    ) -> None:
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

        for index, node in enumerate(
            sorted(
                nodes, key=lambda node: getattr(node.geometry().center(), func_name)()
            )
        ):
            new_pos = border_1 + index * distance_between_nodes
            old_pos = getattr(node.geometry().center(), func_name)()
            dif = (
                QPointF(new_pos - old_pos, 0.0)
                if orientation == 0
                else QPointF(0.0, new_pos - old_pos)
            )
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

    @classmethod
    def get_child_nodes(cls, node: node_ui.NodeProxy) -> set[node_ui.NodeProxy]:
        """
        Retrieve the child nodes of a given node.

        Args:
            node (node_ui.NodeProxy): The node for which to retrieve child nodes.

        Returns:
            set[node_ui.NodeProxy]: A set of child nodes connected to the given node.
        """
        return [connection.bottom_node for connection in node.bottom_connections]

    @classmethod
    def add_new_values_to_pset_tree(
        cls, tree_widget: node_ui.PropertySetTree
    ) -> dict[SOMcreator.SOMPropertySet | SOMcreator.SOMProperty, QTreeWidgetItem]:
        selected_node = cls.get_node_from_tree_widget(tree_widget)
        obj = selected_node.aggregation.som_class
        ir = tree_widget.invisibleRootItem()
        property_set_dict = cls.get_pset_subelement_dict(ir)
        for property_set in obj.get_property_sets(filter=True):
            if property_set not in property_set_dict:
                property_set_item = cls.add_property_set_to_tree(
                    property_set, tree_widget
                )
                property_set_dict[property_set] = property_set_item

            property_set_item = property_set_dict[property_set]
            if property_set_item.text(0) != property_set.name:
                property_set_item.setText(0, property_set.name)

            property_dict = cls.get_pset_subelement_dict(property_set_item)

            for som_property in property_set.get_properties(filter=True):
                if som_property not in property_dict:
                    property_item = cls.add_property_to_property_set_tree(
                        som_property, property_set_item
                    )
                    property_dict[som_property] = property_item
                property_item = property_dict[som_property]
                if property_item.text(0) != som_property.name:
                    property_item.setText(0, som_property.name)
        return property_set_dict

    @classmethod
    def delete_old_values_from_pset_tree(
        cls,
        tree_widget: node_ui.PropertySetTree,
        property_set_dict: dict[
            SOMcreator.SOMPropertySet | SOMcreator.SOMProperty, QTreeWidgetItem
        ],
    ):
        selected_node = cls.get_node_from_tree_widget(tree_widget)
        obj = selected_node.aggregation.som_class
        ir = tree_widget.invisibleRootItem()
        for property_set, pset_item in property_set_dict.items():
            if property_set not in obj.get_property_sets(filter=True):
                ir.removeChild(pset_item)
                continue

            property_dict = cls.get_pset_subelement_dict(pset_item)
            for som_property, property_item in property_dict.items():
                if som_property not in property_set.get_properties(filter=True):
                    pset_item.removeChild(property_item)

    @classmethod
    def set_font_metric(cls, font_metrics: Any) -> None:
        cls.get_properties().font_metrics = font_metrics

    @classmethod
    def get_font_metric(cls) -> Any:
        fm = cls.get_properties().font_metrics
        return QFontMetrics(QFont()) if fm is None else fm

    @classmethod
    def set_last_move_direction(cls, move_delta: QPointF) -> None:
        if move_delta is None:
            cls.get_properties().last_move_direction = None
            return
        direction = 0
        if move_delta.x() != 0:
            direction += 1
        if move_delta.y() != 0:
            direction += 2
        cls.get_properties().last_move_direction = direction

    @classmethod
    def get_last_move_direction(cls) -> int:
        """
        0 = No move, 1 = horizontal, 2 = vertical, 3 = both

        :param cls: Description
        :type cls:
        :return: Description
        :rtype: int"""
        return cls.get_properties().last_move_direction

    @classmethod
    def is_move_direction_locked(cls) -> bool:

        return cls.get_properties().is_move_direction_locked

    @classmethod
    def lock_move_direction(cls, lock: bool) -> None:
        if lock:
            logging.debug(f"Lock Move Direction")
        else:
            logging.debug(f"Unlock Move Direction")

        cls.get_properties().is_move_direction_locked = lock
