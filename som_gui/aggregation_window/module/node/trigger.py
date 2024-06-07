from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QTreeWidgetItem
from som_gui.aggregation_window.core import node as core
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool
from PySide6.QtGui import QPainter

if TYPE_CHECKING:
    from . import ui


def connect() -> None:
    pass


def on_new_project() -> None:
    pass


def pset_tree_double_clicked(item: QTreeWidgetItem, _: int) -> None:
    core.pset_tree_double_clicked(item, aw_tool.Node, tool.PropertySetWindow, tool.Attribute, tool.AttributeTable)


def drag_move(header, dif) -> None:
    core.header_drag_move(header, dif, aw_tool.View, aw_tool.Node)


def header_clicked(header: ui.Header) -> None:
    core.node_clicked(header.node, aw_tool.Node)


def paint_propertyset_tree(tree: ui.PropertySetTree) -> None:
    core.paint_pset_tree(tree, aw_tool.Node)


def paint_node(node: ui.NodeProxy) -> None:
    core.paint_node(node, aw_tool.Node)


def paint_header(header, painter: QPainter) -> None:
    core.paint_header(painter, header, aw_tool.Node)


def paint_circle(circle: ui.Circle) -> None:
    core.paint_circle(circle, aw_tool.Node)
