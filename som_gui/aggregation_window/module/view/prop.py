from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.classes import Aggregation
from PySide6.QtCore import QPointF
if TYPE_CHECKING:
    from .ui import AggregationView, AggregationScene
    from ..node.ui import NodeProxy

class ViewProperties:
    aggregation_view: AggregationView = None
    active_scene: AggregationScene = None
    scene_name_list: list[str] = list()
    scene_list: list[AggregationScene] = list()
    aggregation_list: list[list[tuple[Aggregation, QPointF]]] = list()
    node_list: list[list[NodeProxy]] = list()
