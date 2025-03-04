from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, TypedDict

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

import SOMcreator

if TYPE_CHECKING:
    from .ui import ClassInfoWidget


class ContextMenuDict(TypedDict):
    name_getter: Callable
    function: Callable
    on_single_select: bool
    on_multi_select: bool
    action: QAction


class ObjectInfoWidgetProperties:
    focus_object: SOMcreator.SOMClass = None
    mode: int = 0  # 1= Info 2 =Copy
    ifc_mappings: list[str] = list()
    name: str = ""
    plugin_infos: dict[str, Any] = dict()
    is_group: bool = False
    pset_name: str = ""
    attribute_name: str = ""
    ident_value: str = ""
    ifc_lines: list = list()


class ClassProperties:
    active_class: SOMcreator.SOMClass = None
    object_info_widget_properties: ObjectInfoWidgetProperties = None
    context_menu_list: list[ContextMenuDict] = list()
    object_info_widget: ClassInfoWidget = None
    first_paint = True
    column_List: list[tuple[Callable, Callable, Callable]] = list()
    class_activate_functions = list()
    class_add_infos_functions = list()
    class_info_plugin_list: list[PluginProperty] = list()
    class_add_checks = list()


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
