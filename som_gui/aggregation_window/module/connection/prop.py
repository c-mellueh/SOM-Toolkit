from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.node.ui import NodeProxy
    from PySide6.QtWidgets import QGraphicsPathItem


class ConnectionProperties:
    draw_node: NodeProxy | None = None
    draw_connection: QGraphicsPathItem | None = None
    draw_started: bool = False
