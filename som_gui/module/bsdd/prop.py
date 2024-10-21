from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QAction
if TYPE_CHECKING:
    from .ui import Widget, DictionaryWidget
    from SOMcreator.exporter.bsdd import Dictionary

class BsddProperties:
    widget: Widget = None
    dictionary_widget: DictionaryWidget = None
    tab_list: list[tuple[str, QWidget]] = list()
    dictionary: Dictionary = None
    actions: dict[str, QAction] = dict()
