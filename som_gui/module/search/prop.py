from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui import SearchDialog
from dataclasses import dataclass

from PySide6.QtWidgets import QDialog


class SearchProperties:
    search_dialogues: set[QDialog] = set()
    filter_threshold: int = 65
    search_mode = 1  # 1 = Object 2= Property
    selected_info = None
