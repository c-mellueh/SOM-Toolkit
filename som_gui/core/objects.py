from __future__ import annotations

from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool import Objects, Project
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import QPoint


def refresh_object_tree(object_tool: Type[Objects], project_tool: Type[Project]):
    """
    gets called on Paint Event
    """
    load_objects(object_tool, project_tool)


def load_objects(object_tool: Type[Objects], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter=True)
    object_tree: QTreeWidget = object_tool.get_object_tree()
    object_tool.fill_object_tree(set(root_objects), object_tree.invisibleRootItem())

def item_changed(item: QTreeWidgetItem, object_tool: Type[Objects]):
    object_tool.update_check_state(item)
    pass

def item_selection_changed(object_tool: Type[Objects]):
    selected_items = object_tool.get_selected_items()
    if len(selected_items) == 1:
        obj = object_tool.get_object_from_item(selected_items[0])
        object_tool.set_active_object(obj)


def item_dropped_on(pos: QPoint, object_tool: Type[Objects]):
    selected_items = object_tool.get_selected_items()
    dropped_on_item = object_tool.get_item_from_pos(pos)
    if dropped_on_item is None:
        return
    dropped_on_object = object_tool.get_object_from_item(dropped_on_item)
    if not object_tool.drop_indication_pos_is_on_item():
        dropped_on_object = dropped_on_object.parent
    dropped_objects = [object_tool.get_object_from_item(item) for item in selected_items]
    for obj in dropped_objects:
        if dropped_on_object is None:
            obj.remove_parent()
        else:
            obj.parent = dropped_on_object
