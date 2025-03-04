from __future__ import annotations
from typing import  Callable, TypedDict
from PySide6.QtGui import QAction
import SOMcreator


class ContextMenuDict(TypedDict):
    name_getter: Callable
    function: Callable
    on_single_select: bool
    on_multi_select: bool
    action: QAction

class ClassProperties:
    active_class: SOMcreator.SOMClass = None
    context_menu_list: list[ContextMenuDict] = list()
    first_paint = True
    column_List: list[tuple[Callable, Callable, Callable]] = list()
    class_activate_functions = list()
    class_add_checks = list()
