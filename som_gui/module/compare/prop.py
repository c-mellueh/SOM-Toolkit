from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
    from PySide6.QtWidgets import QHBoxLayout, QLabel
    from .ui import ProjectSelectDialog, CompareDialog, AttributeWidget

class CompareProjectSelectProperties:
    proj_select_dialog: ProjectSelectDialog = None
    layout_proj0: QHBoxLayout = None
    layout_proj1: QHBoxLayout = None
    is_current_proj_input: bool = False
    label_project: QLabel = None
    layout_input: QHBoxLayout = None
    pass




class CompareWindowProperties:
    widgets = list()
    names = list()
    init_functions = list()
    tools = list()
    window: CompareDialog = None
    export_funcs = list()
