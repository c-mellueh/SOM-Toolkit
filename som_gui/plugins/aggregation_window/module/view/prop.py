from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF

from SOMcreator import SOMAggregation

if TYPE_CHECKING:
    from .ui import AggregationView, AggregationScene
    from ..node.ui import NodeProxy
    from ..connection.ui import Connection
    from PySide6.QtGui import QTransform


class ViewProperties:
    aggregation_view: AggregationView = None
    active_scene: AggregationScene = None
    scene_name_list: list[str] = list()
    scene_list: list[AggregationScene] = list()
    node_list: list[set[NodeProxy]] = list()
    import_list: list[list[tuple[SOMAggregation, QPointF]]] = list()
    connections_list: list[set[Connection]] = list()
    scene_settings_list: list[tuple[QTransform, float, float] | None] = (
        list()
    )  # (Transform, Horizontal Scroll, Vertical Scroll)
    focus_list: list[bool] = list()  # list for scenes which autofocussed at least once
    last_mouse_pos: QPointF = None
    mouse_mode: int = 0
    resize_node: NodeProxy | None = None
    copy_list: list[tuple[SOMAggregation, QPointF]] = list()
    drawn_scenes:set[AggregationScene] = set()