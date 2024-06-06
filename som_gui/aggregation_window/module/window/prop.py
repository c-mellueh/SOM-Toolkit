from __future__ import annotations
from typing import TYPE_CHECKING

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
