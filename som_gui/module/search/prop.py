from dataclasses import dataclass
from PySide6.QtWidgets import QDialog


@dataclass
class SearchProperties():
    search_window: QDialog = None
    filter_threshold: int = 65
    search_mode = 1  # 1 = Object 2= Attribute
    selected_info = None
