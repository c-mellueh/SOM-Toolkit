from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget
from som_gui.aggregation_window.core import node as core
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool
from PySide6.QtGui import QPainter

if TYPE_CHECKING:
    from . import ui

def connect():
    pass


def on_new_project():
    pass


def pset_tree_double_clicked(item: QTreeWidgetItem, _: int):
    core.pset_tree_double_clicked(item, aw_tool.Node, tool.PropertySetWindow, tool.Attribute, tool.AttributeTable)


def drag_move(header, dif):
    core.header_drag_move(header, dif, aw_tool.Node)


def paint_header(header, painter: QPainter):
    core.paint_header(painter, header, aw_tool.Node)


def header_clicked(header: ui.Header):
    core.node_clicked(header.node, aw_tool.Node)


def paint_propertyset_tree(tree: QTreeWidget):
    core.paint_pset_tree(tree, aw_tool.Node)
