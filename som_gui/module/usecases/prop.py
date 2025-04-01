from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtGui import QAction
class UsecasesProperties:
    actions:dict[str,QAction] = dict()
    window = None
