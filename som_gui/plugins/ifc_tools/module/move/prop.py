from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from . import ui
class MoveProperties:
    widget: ui.MoveWidget = None
    thread_pool: QThreadPool = None
    actions: dict[str, QAction] = dict()
