from __future__ import annotations
from PySide6.QtWidgets import QWidget
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from . import ui
class SettingsProperties:
    tab_widgets: list[QWidget] = list()
    tab_section_index: list[int] = list()
    open_functions: list[Callable] = list()
    accept_functions: list[Callable] = list()
    sections: list[str] = list()
    widget: ui.Widget = None
