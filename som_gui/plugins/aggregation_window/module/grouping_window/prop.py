from __future__ import annotations
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ui
    from som_gui.module.ifc_importer.ui import IfcImportWidget


class GroupingWindowProperties():
    grouping_attribute_line_edit: QLineEdit | None = None
    grouping_pset_line_edit: QLineEdit | None = None
    grouping_window: ui.GroupingWindow | None = None
    status_label: QLabel | None = None
    export_button: QPushButton | None = None
    export_line_edit: QLineEdit | None = None
    ifc_importer: IfcImportWidget | None = None
    ifc_button: QPushButton | None = None  # Button for selecting IFC files
    run_button: QPushButton | None = None
    abort_button: QPushButton | None = None
    abort: bool = False
    main_attribute: tuple[str, str] = ("", "")
    grouping_attribute: tuple[str, str] = ("", "")
    export_path: str = ""
    ifc_import_runners = list()
    ifc_name: str = ""
    runner = None
    thread_pool = None
    identity_attribute = "identitaet"
    create_empty_attribues: bool = True
    is_running = False
