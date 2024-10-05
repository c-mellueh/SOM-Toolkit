from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from . import ui

class FilterWindowProperties:
    widget: ui.FilterWidget = None
    active_object: SOMcreator.Object = None
