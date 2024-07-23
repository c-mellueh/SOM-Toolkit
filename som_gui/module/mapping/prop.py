from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import MappingWindow


class MappingProperties:
    window: MappingWindow = None
    object_check_state_dict: dict[SOMcreator.Object, bool] = dict()
