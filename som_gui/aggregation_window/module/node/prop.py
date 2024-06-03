from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import NodeProxy, Header, Frame
    from SOMcreator.classes import Aggregation


class NodeProperties:
    title_pset: str | None = None
    title_attribute: str | None = None
    z_level: int = 1
