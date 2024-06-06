from __future__ import annotations
from typing import TYPE_CHECKING, Callable

import SOMcreator

if TYPE_CHECKING:
    from .ui import AggregationWindow, ComboBox
    from som_gui.module.util.prop import MenuDict

class WindowProperties:
    aggregation_window: AggregationWindow = None
    combo_box: ComboBox = None
    menu_dict: MenuDict = {
        "submenu": list(),
        "actions": list(),
        "menu":    None,
        "name":    "menubar",
    }
    menu_list: list[tuple[str, Callable]] = list()  # MenubarPath,Function
    filter_is_activated: bool = False
    allowed_scenes: list = list()  # Scenes that will be displayed after filter is activated
    filter_object: SOMcreator.Object | None = None
