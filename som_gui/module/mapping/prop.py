from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import MappingWindow, ClassTreeWidget, PropertySetTreeWidget
    from PySide6.QtWidgets import QTreeWidget
    from PySide6.QtGui import QAction


class MappingProperties:
    window: MappingWindow = None
    check_state_dict: dict[
        SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty, bool
    ] = dict()
    class_tree: ClassTreeWidget = None
    pset_tree: PropertySetTreeWidget = None
    ifc_export_dict: dict[str, (list[SOMcreator.SOMProperty], set[str])] = dict()
    actions: dict[str, QAction] = dict()
