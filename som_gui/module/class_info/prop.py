from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, TypedDict
from PySide6.QtWidgets import QWidget
import SOMcreator

if TYPE_CHECKING:
    from .ui import ClassInfoDialog


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
    dialog: ClassInfoDialog = None
    active_class: SOMcreator.SOMClass = None
    mode: int = 0  # 0= create 1= Info 2 =Copy
    ifc_mappings: list[str] = list()
    class_name: str = ""
    plugin_infos: dict[str, Any] = dict()
    is_group: bool = False
    pset_name: str = ""
    ident_property_name: str = ""
    ident_value: str = ""
    ifc_line_edits: list = list()
    class_add_infos_functions = list()
    class_info_plugin_list: list[PluginProperty] = list()
    description: str = ""
