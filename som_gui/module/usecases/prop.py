from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtGui import QAction
    from . import ui
    import SOMcreator
class UsecasesProperties:
    actions:dict[str,QAction] = dict()
    window:ui.Widget = None