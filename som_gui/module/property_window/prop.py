from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass
from PySide6.QtWidgets import QWidget
from . import ui
import SOMcreator

@dataclass
class PluginProperty:
    key: str
    layout_name: str
    widget: QWidget
    index: int
    value_getter: Callable
    value_setter: Callable
    widget_value_setter: Callable
    value_test: Callable


class PropertyWindowProperties:
    plugin_widget_list: list[PluginProperty] = list()
    windows:dict[SOMcreator.SOMProperty,ui.PropertyWindow] = dict()
    context_menu_builders = list()