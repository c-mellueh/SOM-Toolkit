from PySide6.QtWidgets import QTreeWidgetItem
from som_gui.aggregation_window.core import node as core
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool
def connect():
    pass


def on_new_project():
    pass


def pset_tree_double_clicked(item: QTreeWidgetItem, _: int):
    core.pset_tree_double_clicked(item, aw_tool.Node, tool.PropertySetWindow, tool.Attribute, tool.AttributeTable)
