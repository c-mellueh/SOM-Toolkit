from __future__ import annotations

from typing import TYPE_CHECKING

import ifcopenshell

if TYPE_CHECKING:
    from som_gui.tool.modelcheck import ModelcheckRunner
    from PySide6.QtWidgets import QLabel, QProgressBar
    from sqlite3 import Connection


class ModelcheckProperties:
    guids: dict[str, str] = dict()
    database_path: str = None
    main_property_name: str = None
    main_pset_name: str = None
    ifc_name: str = None
    ident_dict: dict = dict()
    data_dict: dict = dict()
    active_element: ifcopenshell.entity_instance = None
    active_element_type: str = None
    status_label: QLabel = None
    progress_bar: QProgressBar = None
    object_checked_count: int = 0
    object_count: int = 0
    abort_modelcheck: bool = False
    group_parent_dict: dict = dict()
    group_dict: dict = dict()
    connection: Connection = None
    file_check_plugins = list()
    entity_check_plugins = list()
