from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import MappingWindow, ObjectTreeWidget, PropertySetTreeWidget
    from PySide6.QtWidgets import QTreeWidget
    from PySide6.QtGui import QAction


class MappingProperties:
    window: MappingWindow = None
    check_state_dict: dict[SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute, bool] = dict()
    object_tree: ObjectTreeWidget = None
    pset_tree: PropertySetTreeWidget = None
    ifc_export_dict: dict[str, (list[SOMcreator.Attribute], set[str])] = dict()
    actions: dict[str, QAction] = dict()
