from __future__ import annotations
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ui
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from som_gui.tool.ifc_importer import IfcImportRunner
    from PySide6.QtGui import QAction
class GroupingWindowProperties:
    grouping_window: ui.GroupingWindow | None = None
    export_button: QPushButton | None = None
    export_line_edit: QLineEdit | None = None
    ifc_importer: IfcImportWidget | None = None
    abort: bool = False
    main_attribute: tuple[str, str] = ("", "")
    grouping_attribute: tuple[str, str] = ("", "")
    export_path: str = ""
    ifc_import_runners: list[IfcImportRunner] = list()
    ifc_name: str = ""
    runner = None
    thread_pool = None
    identity_attribute = "identitaet"
    create_empty_attribues: bool = True
    is_running = False
    actions: dict[str, QAction] = dict()
