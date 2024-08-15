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


class CompareAttributesProperties:
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    object_dict: dict[SOMcreator.Object, SOMcreator.Object | None] = dict()
    missing_objects: list[list[SOMcreator.Object]] = [None, None]
    object_tree_item_dict = dict()
    object_lists: list[tuple[SOMcreator.Object | None, SOMcreator.Object | None]] = list()
    pset_lists: dict[SOMcreator.Object, list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]] = dict()
    attributes_lists: dict[SOMcreator.PropertySet, list[tuple[SOMcreator.Attribute, SOMcreator.Attribute]]] = dict()
    values_lists: dict[SOMcreator.Attribute, list[tuple[str, str]]] = dict()
    widget: AttributeWidget = None


class CompareWindowProperties:
    widgets = list()
    names = list()
    init_functions = list()
    tools = list()
    window: CompareDialog = None
    export_funcs = list()
