from dataclasses import dataclass
from som_gui.module.use_case.ui import UseCaseWindow
from PySide6.QtCore import Qt


@dataclass
class UseCaseProperties:
    active_use_case_index: int
    active_use_case_name: str
    active_check_state: Qt.CheckState = None
    use_case_window: UseCaseWindow = None
    object_tree_is_clicked: bool = False
