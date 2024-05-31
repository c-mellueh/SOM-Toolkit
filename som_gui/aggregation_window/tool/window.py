from __future__ import annotations
from typing import TYPE_CHECKING

import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.window import ui as ui_window
import som_gui

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.window.prop import WindowProperties


class Window(som_gui.aggregation_window.core.tool.Window):
    @classmethod
    def get_properties(cls) -> WindowProperties:
        return som_gui.WindowProperties

    @classmethod
    def create_window(cls) -> ui_window.AggregationWindow:
        window = ui_window.AggregationWindow()
        cls.get_properties().aggregation_window = window
        return window
