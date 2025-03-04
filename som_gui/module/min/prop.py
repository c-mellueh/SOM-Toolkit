
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, TypedDict

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

import SOMcreator

if TYPE_CHECKING:
    from .ui import ClassInfoWidget

class ClassInfoProperties:
    widget:ClassInfoWidget = None
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