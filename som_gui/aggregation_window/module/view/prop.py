from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.classes import Aggregation
from PySide6.QtCore import QPointF
if TYPE_CHECKING:
    from .ui import AggregationView, AggregationScene


class ViewProperties:
    aggregation_view: AggregationView = None
    active_scene: AggregationScene = None
    aggregation_dict: dict[str, list[tuple[Aggregation, QPointF]]] = dict()
    scene_dict: dict[str, AggregationScene] = dict()
