from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import AttributeImportWindow, AttributeImportWidget, SettingsDialog
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from PySide6.QtWidgets import QPushButton, QLabel
    from som_gui.tool.modelcheck import ModelcheckRunner
    from PySide6.QtWidgets import QLabel, QProgressBar
    from sqlite3 import Connection
class AttributeImportProperties:
    active_window: AttributeImportWindow = None
    attribute_import_widget: AttributeImportWidget = None
    ifc_importer: IfcImportWidget = None
    settings_dialog: SettingsDialog = None
    main_pset: str = "Undefined"
    main_attribute: str = "Undefined"
    import_is_aborted = False
    ifc_import_runners = []
    runner = None
    thread_pool = None
    run_button: QPushButton = None
    ifc_button: QPushButton = None
    abort_button: QPushButton = None
    status_label: QLabel = None


class AttributeImportSQLProperties:
    database_path: str = None
    connection: Connection = None
