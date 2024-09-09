from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.bsdd.prop import BsddProperties
import som_gui.core.tool
import som_gui
from som_gui.module.bsdd import ui

class Bsdd(som_gui.core.tool.Bsdd):

    @classmethod
    def get_properties(cls) -> BsddProperties:
        return som_gui.BsddProperties

    @classmethod
    def get_window(cls) -> ui.Widget:
        if not cls.get_properties().widget:
            cls.get_properties().widget = ui.Widget()
        return cls.get_properties().widget
