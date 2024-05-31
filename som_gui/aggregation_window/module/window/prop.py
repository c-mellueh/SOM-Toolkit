from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import AggregationWindow, ComboBox


class WindowProperties:
    aggregation_window: AggregationWindow = None
    combo_box: ComboBox = None
