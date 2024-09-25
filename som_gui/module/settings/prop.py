from __future__ import annotations
from PySide6.QtWidgets import QWidget
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from . import ui
class SettingsProperties:
    tab_dict: dict[str, dict[str, list[QWidget]]] = dict()  # dict[TabName,dict[ToolboxTabName,Widget]]
    open_functions: list[Callable] = list()
    accept_functions: list[Callable] = list()
    widget: ui.Widget = None
