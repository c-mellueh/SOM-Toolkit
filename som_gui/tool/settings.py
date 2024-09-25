from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import logging

import som_gui.core.tool
import som_gui
from som_gui.module.settings import ui
if TYPE_CHECKING:
    from som_gui.module.settings.prop import SettingsProperties


class Settings(som_gui.core.tool.Settings):
    @classmethod
    def get_properties(cls) -> SettingsProperties:
        return som_gui.SettingsProperties

    @classmethod
    def add_tab(cls, tab, start_function: Callable, accept_function: Callable):
        cls.get_properties().tab_widgets.append(tab)
        cls.get_properties().open_functions.append(start_function)
        cls.get_properties().accept_functions.append(accept_function)

    @classmethod
    def get_widget(cls) -> ui.Widget:
        return cls.get_properties().widget

    @classmethod
    def set_widget(cls, widget: ui.Widget):
        cls.get_properties().widget = widget

    @classmethod
    def create_widget(cls) -> ui.Widget:
        return ui.Widget()
