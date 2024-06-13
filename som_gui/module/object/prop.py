from __future__ import annotations
from dataclasses import dataclass, field
from PySide6.QtGui import QAction
import SOMcreator
from PySide6.QtWidgets import QDialog
from typing import TYPE_CHECKING, TypedDict, Callable

if TYPE_CHECKING:
    from .ui import ObjectInfoWidget


class ContextMenuDict(TypedDict):
    display_name: str
    function: Callable
    on_single_select: bool
    on_multi_select: bool
    action: QAction

@dataclass
class ObjectInfoWidgetProperties:
    focus_object: SOMcreator.Object = None
    mode: int = 0  # 1= Info 2 =Copy
    ifc_mappings: list[str] = field(default_factory=lambda: [])
    name: str = ""
    abbreviation: str = ""
    is_group: bool = False
    pset_name: str = ""
    attribute_name: str = ""
    ident_value: str = ""
    ifc_lines: list = field(default_factory=lambda: [])

class ObjectProperties:
    active_object: SOMcreator.Object
    object_info_widget_properties: ObjectInfoWidgetProperties
    context_menu_list: list[ContextMenuDict] = list()
    object_info_widget: ObjectInfoWidget = None
    first_paint = True
    column_List: list[tuple[str, Callable]] = list()
    object_activate_functions = list()
