from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtCore import QThreadPool

if TYPE_CHECKING:
    from . import ui
class MoveProperties:
    widget: ui.MoveWidget = None
    thread_pool: QThreadPool = None
