from __future__ import annotations

from typing import Callable, TYPE_CHECKING, Optional

from PySide6.QtWidgets import QLineEdit

import SOMcreator
from dataclasses import dataclass,field
if TYPE_CHECKING:
    from .ui import AggregationWindow, ComboBox
    from som_gui.module.util.prop import MenuDict
    from PySide6.QtGui import QAction
    from ..grouping_window.ui import GroupingWindow


@dataclass
class WindowProperties:
    aggregation_window: Optional[AggregationWindow] = None
    combo_box: Optional[ComboBox] = None
    menu_dict: dict[str, Optional[list]] = field(default_factory=lambda: {
        "submenu": [],
        "actions": [],
        "menu": None,
        "name": "menubar",
    })
    menu_list: list[tuple[str, Callable]] = field(default_factory=list)  # MenubarPath, Function
    filter_is_activated: bool = False
    allowed_scenes: list = field(default_factory=list)  # Scenes that will be displayed after filter is activated
    filter_class: Optional[SOMcreator.SOMClass] = None
    class_info_line_edit: Optional[QLineEdit] = None
    grouping_window: Optional[GroupingWindow] = None
    actions: dict[str, QAction] = field(default_factory=dict)
