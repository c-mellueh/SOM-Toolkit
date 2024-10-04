from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.filter_window.prop import FilterWindowProperties


class FilterWindow(som_gui.core.tool.FilterWindow):
    @classmethod
    def get_properties(cls) -> FilterWindowProperties:
        return som_gui.FilterWindowProperties
