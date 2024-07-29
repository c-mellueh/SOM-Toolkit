from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
    from PySide6.QtWidgets import QHBoxLayout, QLabel
    from .ui import ImportDialog, CompareDialog
COMPARE_SETTING = "compare"

class CompareProperties():
    import_dialog: ImportDialog = None
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    window: CompareDialog = None
    object_dicts = [None, None]
    missing_objects: list[list[SOMcreator.Object]] = [None, None]
    object_tree_item_dict = dict()
    pset_lists: dict[SOMcreator.Object, list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]] = dict()
    attributes_lists: dict[SOMcreator.PropertySet, list[tuple[SOMcreator.Attribute, SOMcreator.Attribute]]] = dict()
    values_lists: dict[SOMcreator.Attribute, list[tuple[str, str]]] = dict()
    layout_proj0: QHBoxLayout = None
    layout_proj1: QHBoxLayout = None
    current_project_as_input: bool = False
    label_project: QLabel = None
    layout_input: QHBoxLayout = None
