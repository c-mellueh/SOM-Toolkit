
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.property_window.prop import PropertyWindowProperties


class PropertyWindow(som_gui.core.tool.PropertyWindow):
    @classmethod
    def get_properties(cls) -> PropertyWindowProperties:
        return som_gui.PropertyWindowProperties
