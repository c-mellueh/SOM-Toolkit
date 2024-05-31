from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import NodeProxy, Header, Frame
    from SOMcreator.classes import Aggregation


class NodeProperties:
    aggregation_dict: dict[Aggregation, NodeProxy] = dict()
    header_dict: dict[Header, NodeProxy] = dict()
    frame_dict: dict[NodeProxy, Frame] = dict()
