from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ClassInfoLineEdit
from PySide6.QtGui import QAction


class AggregationProperties:
    class_info_line_edit: ClassInfoLineEdit = None
    grouping_window = None
    actions: dict[str, QAction] = dict()
    class_info_indexes = list()
    save_function_index = None
