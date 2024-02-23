from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, ObjectCheckWidget


class ModelcheckProperties:
    active_window: ModelcheckWindow = None
    checkbox_widget: ObjectCheckWidget = None
