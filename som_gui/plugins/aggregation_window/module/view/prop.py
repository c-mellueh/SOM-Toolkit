from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF

from SOMcreator import SOMAggregation

if TYPE_CHECKING:
    from .ui import AggregationView, AggregationScene
    from ..node.ui import NodeProxy
    from ..connection.ui import Connection
    from PySide6.QtGui import QTransform

from dataclasses import dataclass, field


@dataclass
class ViewProperties:
    project_scene_dict = dict()
    aggregation_view: AggregationView = None
    active_scene: AggregationScene = None
    scene_name_list: list[str] = field(default_factory=list)
    scene_list: list[AggregationScene] = field(default_factory=list)
    node_list: list[set[NodeProxy]] = field(default_factory=list)
    import_list: list[list[tuple[SOMAggregation, QPointF]]] = field(
        default_factory=list
    )
    connections_list: list[set[Connection]] = field(default_factory=list)
    scene_settings_list: list[tuple[QTransform, float, float] | None] = field(
        default_factory=list
    )  # (Transform, Horizontal Scroll, Vertical Scroll)
    focus_list: list[bool] = field(
        default_factory=list
    )  # list for scenes which autofocussed at least once
    last_mouse_pos: QPointF = None
    mouse_mode: int = 0
    resize_node: NodeProxy | None = None
    copy_list: list[tuple[SOMAggregation, QPointF]] = field(default_factory=list)
    drawn_scenes: set[AggregationScene] = field(default_factory=set)
