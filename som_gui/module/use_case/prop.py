from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QAction
    from . import ui
    import SOMcreator


class UseCaseProperties:
    actions: dict[str, QAction] = dict()
    window: ui.Widget = None
    mouse_is_pressed = False
    mouse_press_checkstate: bool = None
