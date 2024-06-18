from __future__ import annotations
from dataclasses import dataclass, field
from PySide6.QtGui import QAction
import SOMcreator
from PySide6.QtWidgets import QDialog, QWidget
from typing import TYPE_CHECKING, TypedDict, Callable, Any

if TYPE_CHECKING:
    from .ui import ObjectInfoWidget


class ContextMenuDict(TypedDict):
    display_name: str
    function: Callable
    on_single_select: bool
    on_multi_select: bool
    action: QAction

class ObjectInfoWidgetProperties:
    focus_object: SOMcreator.Object = None
    mode: int = 0  # 1= Info 2 =Copy
    ifc_mappings: list[str] = list()
    name: str = ""
    plugin_infos: dict[str, Any] = dict()
    is_group: bool = False
    pset_name: str = ""
    attribute_name: str = ""
    ident_value: str = ""
    ifc_lines: list = list()

class ObjectProperties:
    active_object: SOMcreator.Object
    object_info_widget_properties: ObjectInfoWidgetProperties
    context_menu_list: list[ContextMenuDict] = list()
    object_info_widget: ObjectInfoWidget = None
    first_paint = True
    column_List: list[tuple[str, Callable]] = list()
    object_activate_functions = list()
    object_add_infos_functions = list()
    object_info_plugin_list: list[PluginProperty] = list()
    object_add_checks = list()

@dataclass
class PluginProperty:
    key: str
    layout_name: str
    widget: QWidget
    index: int
    init_value_getter: Callable
    widget_value_getter: Callable
    widget_value_setter: Callable
    value_test: Callable
    value_setter: Callable
