from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import AggregationView, AggregationScene


class ViewProperties:
    aggregation_view: AggregationView = None
    active_scene: AggregationScene = None
