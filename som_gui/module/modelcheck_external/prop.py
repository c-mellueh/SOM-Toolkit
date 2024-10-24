from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ModelcheckExternalWindow
    from PySide6.QtGui import QAction


class ModelcheckExternalProperties():
    window: ModelcheckExternalWindow = None
    actions: dict[str, QAction] = dict()
