from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import NodeProxy
    from SOMcreator.classes import Aggregation


class NodeProperties:
    aggregation_dict: dict[Aggregation, NodeProxy] = dict()
