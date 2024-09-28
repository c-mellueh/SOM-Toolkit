from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.plugins.prop import PluginsProperties


class Plugins(som_gui.core.tool.Plugins):
    @classmethod
    def get_properties(cls) -> PluginsProperties:
        return som_gui.PluginsProperties
