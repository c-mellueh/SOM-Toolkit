from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import AggregationWindow


class WindowProperties:
    aggregation_window: AggregationWindow = None
