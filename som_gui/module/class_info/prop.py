from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, TypedDict
from PySide6.QtWidgets import QWidget
import SOMcreator

if TYPE_CHECKING:
    from .ui import ClassInfoWidget


class ClasstDataDict(TypedDict):
    name: str
    is_group: bool
    abbreviation: str
    ident_pset_name: str
    ident_property_name: str
    ident_value: str
    ifc_mappings: list[str]


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


class ClassInfoProperties:
    widget: ClassInfoWidget = None
    focus_object: SOMcreator.SOMClass = None
    mode: int = 0  # 0= create 1= Info 2 =Copy
    ifc_mappings: list[str] = list()
    name: str = ""
    plugin_infos: dict[str, Any] = dict()
    is_group: bool = False
    pset_name: str = ""
    attribute_name: str = ""
    ident_value: str = ""
    ifc_lines: list = list()
    class_add_infos_functions = list()
    class_info_plugin_list: list[PluginProperty] = list()
