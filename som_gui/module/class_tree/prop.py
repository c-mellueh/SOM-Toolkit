from __future__ import annotations
from typing import Callable, TypedDict,TYPE_CHECKING
from PySide6.QtGui import QAction
import SOMcreator

if TYPE_CHECKING:
    from . import ui

class ContextMenuDict(TypedDict):
    name_getter: Callable
    function: Callable
    on_single_select: bool
    on_multi_select: bool
    action: QAction


class ClassTreeProperties:
    existing_trees = set()
    active_class: dict[ui.ClassTreeWidget,SOMcreator.SOMClass] = dict()
    context_menu_list:  dict[ui.ClassTreeWidget,list[ContextMenuDict]] = dict()
    first_paint:  dict[ui.ClassTreeWidget,True] = dict()
    column_List: dict[ui.ClassTreeWidget,list[tuple[Callable, Callable, Callable]]] = dict()

