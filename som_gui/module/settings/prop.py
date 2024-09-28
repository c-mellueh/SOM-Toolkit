from __future__ import annotations
from PySide6.QtWidgets import QWidget, QToolBox
from typing import Callable, TYPE_CHECKING, Type
if TYPE_CHECKING:
    from . import ui
class SettingsProperties:
    tab_dict: dict[str, dict[str, list[Type[QWidget]]]] = dict()  # dict[TabName,dict[ToolboxTabName,Widget]]
    tab_widget_dict: dict[str, tuple[QToolBox, dict[str, QWidget]]] = dict()
    open_functions: list[Callable] = list()
    accept_functions: list[Callable] = list()
    widget: ui.Dialog = None
