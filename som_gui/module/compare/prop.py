from __future__ import annotations
from typing import TYPE_CHECKING,Callable

if TYPE_CHECKING:
    import SOMcreator
    from PySide6.QtWidgets import QHBoxLayout, QLabel
    from .ui import ProjectSelectDialog, CompareDialog, AttributeWidget
    from PySide6.QtGui import QAction
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
    name_getter:list[Callable] = list()
    init_functions = list()
    tools = list()
    window: CompareDialog = None
    export_funcs = list()
    actions: dict[str, QAction] = dict()
