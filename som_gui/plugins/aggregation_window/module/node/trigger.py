from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QTreeWidgetItem

from som_gui import tool
from som_gui.plugins.aggregation_window.core import node as core
from ... import tool as aw_tool

if TYPE_CHECKING:
    from . import ui


def connect() -> None:
    pass


def on_new_project() -> None:
    pass


def pset_tree_double_clicked(item: QTreeWidgetItem, _: int) -> None:
    core.pset_tree_double_clicked(item, aw_tool.Node, tool.PropertySetWindow, tool.AttributeTable)


def drag_move(header, dif) -> None:
    core.move_header(header, dif, aw_tool.View, aw_tool.Node)


def header_clicked(header: ui.Header) -> None:
    core.increment_z_of_node(header.node, aw_tool.Node)


def header_double_clicked(header: ui.Header) -> None:
    core.rename_identity_text(header.node, tool.Popups, aw_tool.Window,aw_tool.Node)


def paint_propertyset_tree(tree: ui.PropertySetTree) -> None:
    core.paint_pset_tree(tree, aw_tool.Node)


def paint_node(node: ui.NodeProxy) -> None:
    core.paint_node(node, aw_tool.Node)


def paint_header(header, painter: QPainter) -> None:
    core.paint_header(painter, header, aw_tool.Node)


def paint_circle(circle: ui.Circle) -> None:
    core.paint_circle(circle, aw_tool.Node)


def retranslate_ui():
    pass
