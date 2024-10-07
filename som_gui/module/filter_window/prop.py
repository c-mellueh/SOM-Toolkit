from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtCore import Qt
import SOMcreator

if TYPE_CHECKING:
    from . import ui

class FilterWindowProperties:
    widget: ui.FilterWidget = None
    active_object: SOMcreator.Object = None
    tree_is_clicked = False
    active_check_state: Qt.CheckState = None
