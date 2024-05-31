from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window.tool import Window, View


def create_window(window: Window, view: View):
    window = window.create_window()
