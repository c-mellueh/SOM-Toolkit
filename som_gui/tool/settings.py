from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.settings.prop import SettingsProperties


class Settings(som_gui.core.tool.Settings):
    @classmethod
    def get_properties(cls) -> SettingsProperties:
        return som_gui.SettingsProperties
