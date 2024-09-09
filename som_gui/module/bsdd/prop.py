from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from PySide6.QtWidgets import QWidget
if TYPE_CHECKING:
    from .ui import Widget, DictionaryWidget
    from SOMcreator.bsdd import Dictionary

class BsddProperties:
    widget: Widget = None
    dictionary_widget: DictionaryWidget = None
    tab_list: list[tuple[str, QWidget]] = list()
    dictionary: Dictionary = None
