from __future__ import annotations
from dataclasses import dataclass, field
import SOMcreator
from PySide6.QtWidgets import QDialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ObjectInfoWidget


@dataclass
class ObjectInfoWidgetProperties:
    ifc_mappings: list[str] = field(default_factory=lambda: [])
    name: str = ""
    abbreviation: str = ""
    is_group: bool = False
    pset_name: str = ""
    attribute_name: str = ""
    ident_value: str = ""
    ifc_lines: list = field(default_factory=lambda: [])

@dataclass
class ObjectProperties:
    active_object: SOMcreator.Object
    object_info_widget_properties: ObjectInfoWidgetProperties
    object_info_widget: ObjectInfoWidget = None
