from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, QPointF

from som_gui.module.project.constants import CLASS_REFERENCE
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QGraphicsRectItem
from PySide6.QtCore import QRectF
from SOMcreator.classes import Aggregation, Object
import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.node import ui as node_ui
from som_gui.aggregation_window.module.node import constants as node_constants

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node.prop import NodeProperties
    from som_gui.aggregation_window.module.view import ui as view_ui


class Node(som_gui.aggregation_window.core.tool.Node):
    @classmethod
    def get_properties(cls) -> NodeProperties:
        return som_gui.NodeProperties

    @classmethod
    def create_tree_widget(cls, obj: Object) -> node_ui.PropertySetTree:
        widget = node_ui.PropertySetTree()
        widget.setHeaderLabel("Name")
        for property_set in obj.property_sets:
            item = QTreeWidgetItem()
            item.setText(0, property_set.name)
            item.setData(0, CLASS_REFERENCE, property_set)

            for attribute in property_set.attributes:
                attribute_item = QTreeWidgetItem()
                attribute_item.setText(0, attribute.name)
                attribute_item.setData(0, CLASS_REFERENCE, attribute)
                item.addChild(attribute_item)
            widget.addTopLevelItem(item)
        return widget

    @classmethod
    def create_node(cls, aggregation: Aggregation):
        node = node_ui.NodeProxy()
        node_widget = node_ui.NodeWidget()
        node.setWidget(node_widget)
        node_widget.setMinimumSize(QSize(250, 150))
        node.widget().layout().insertWidget(0, cls.create_tree_widget(aggregation.object))
        cls.get_properties().aggregation_dict[aggregation] = node
        return node

    @classmethod
    def create_header(cls, node: node_ui.NodeProxy, scene: view_ui.AggregationScene):
        header = node_ui.Header()
        line_width = header.pen().width()  # if ignore Linewidth: box of Node and Header won't match
        x = line_width / 2
        width = node.widget().width() - line_width
        height = node_constants.HEADER_HEIGHT
        header.setRect(QRectF(x, -height, width, height))
        scene.addItem(header)
        header.show()
        cls.get_properties().header_dict[header] = node

    @classmethod
    def create_frame(cls, node: node_ui.NodeProxy, scene: view_ui.AggregationScene):
        frame = node_ui.Frame()
        rect = node.rect()
        rect.setWidth(rect.width() - frame.pen().width() / 2)
        rect.setY(rect.y() - node_constants.HEADER_HEIGHT)
        rect.setHeight(rect.height())
        rect.setX(frame.x() + frame.pen().width() / 2)
        frame.setRect(rect)
        scene.addItem(frame)
        frame.show()
        cls.get_properties().frame_dict[node] = frame

    @classmethod
    def add_node_to_scene(cls, node: node_ui.NodeProxy, scene: view_ui.AggregationScene):
        scene.addItem(node)

    @classmethod
    def get_linked_item(cls, pset_tree_item: QTreeWidgetItem) -> SOMcreator.PropertySet | SOMcreator.Attribute:
        return pset_tree_item.data(0, CLASS_REFERENCE)

    @classmethod
    def get_node_from_header(cls, header):
        return cls.get_properties().header_dict.get(header)

    @classmethod
    def get_frame_from_node(cls, node: node_ui.NodeProxy):
        return cls.get_properties().frame_dict[node]

    @classmethod
    def move_node(cls, node: node_ui.NodeProxy, dif: QPointF):
        node.moveBy(dif.x(), dif.y())
        frame = cls.get_frame_from_node(node)
        frame.moveBy(dif.x(), dif.y())

    @classmethod
    def get_title(cls, node: node_ui.NodeProxy, pset_name: str, attribute_name: str):
        aggregation = cls.get_aggregation_from_node(node)
        if not (pset_name and attribute_name):
            base_text = f"{aggregation.name} ({aggregation.object.abbreviation})"

            if aggregation.is_root:
                title = base_text
            else:
                title = f"{base_text}\nidGruppe: {aggregation.id_group()}"
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
    def get_aggregation_from_node(cls, node: node_ui.NodeProxy):
        ad = cls.get_properties().aggregation_dict
        print(ad)
        reversed = {v: k for k, v in ad.items()}
        return reversed.get(node)

    @classmethod
    def get_title_settings(cls):
        return cls.get_properties().title_pset, cls.get_properties().title_attribute

    @classmethod
    def set_title_settings(cls, pset_name, attribute_name):
        cls.get_properties().title_pset, cls.get_properties().title_attribute = pset_name, attribute_name

    @classmethod
    def reset_title_settings(cls):
        cls.get_properties().title_pset, cls.get_properties().title_attribute = None, None
