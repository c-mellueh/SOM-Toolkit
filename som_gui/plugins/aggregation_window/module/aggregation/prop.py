from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui import ObjectInfoLineEdit
from PySide6.QtGui import QAction


class AggregationProperties:
    object_info_line_edit:ObjectInfoLineEdit = None
    grouping_window = None
    actions: dict[str, QAction] = dict()
