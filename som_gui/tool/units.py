
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.units.prop import UnitsProperties


class Units(som_gui.core.tool.Units):
    @classmethod
    def get_properties(cls) -> UnitsProperties:
        return som_gui.UnitsProperties
