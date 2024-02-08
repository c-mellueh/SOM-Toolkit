from dataclasses import dataclass, field

import SOMcreator

from som_gui.module.object_filter.ui import ObjectFilterWindow
from PySide6.QtCore import Qt


@dataclass
class ObjectFilterProperties:
    active_use_case_index: int
    active_use_case_name: str
    object_dict: dict
    pset_dict: dict
    attribute_dict: dict
    use_cases: list[SOMcreator.classes.UseCase]
    active_object: SOMcreator.Object = None
    active_check_state: Qt.CheckState = None
    object_filter_window: ObjectFilterWindow = None
    tree_is_clicked: bool = False
    header_data: list[list[str, int, int]] = None
