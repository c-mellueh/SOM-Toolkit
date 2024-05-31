from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize

from som_gui.module.project.constants import CLASS_REFERENCE
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem
from SOMcreator.classes import Aggregation, Object
import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.node import ui as node_ui

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
        return node

    @classmethod
    def add_node_to_scene(cls, node: node_ui.NodeProxy, scene: view_ui.AggregationScene):
        scene.addItem(node)
