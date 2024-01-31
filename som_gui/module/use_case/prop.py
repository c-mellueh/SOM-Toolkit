from dataclasses import dataclass, field

import SOMcreator

from som_gui.module.use_case.ui import UseCaseWindow
from PySide6.QtCore import Qt


@dataclass
class UseCaseProperties:
    active_use_case_index: int
    active_use_case_name: str
    object_dict: dict
    pset_dict: dict
    attribute_dict: dict
    use_cases: list[SOMcreator.classes.UseCase]
    active_object: SOMcreator.Object = None
    active_check_state: Qt.CheckState = None
    use_case_window: UseCaseWindow = None
    tree_is_clicked: bool = False
    header_data: list[list[str, int, int]] = None
