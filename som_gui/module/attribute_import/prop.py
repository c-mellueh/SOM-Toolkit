from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import AttributeImportWindow, AttributeImportResultWindow, SettingsDialog
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from PySide6.QtWidgets import QComboBox, QPushButton, QLabel, QCheckBox
    from PySide6.QtWidgets import QLabel, QProgressBar
    from sqlite3 import Connection

class AttributeImportProperties:
    ifc_import_window: AttributeImportWindow = None
    attribute_import_window: AttributeImportResultWindow = None
    ifc_importer: IfcImportWidget = None

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
    progress_bar: QProgressBar = None
    ifc_path: str = None
    ifc_combobox: QComboBox = None
    som_combobox: QComboBox = None
    all_keyword: str = "Alles"
    is_updating_locked: bool = False
    update_lock_reason: str = ""
    all_checkbox: QCheckBox = None

class AttributeImportSQLProperties:
    database_path: str = None
    connection: Connection = None
    settings_dialog: SettingsDialog = None
    show_existing_values: bool = False
    show_regex_values: bool = False
    show_range_values: bool = False
    color_values: bool = False
    show_boolean_values: bool = False
    active_usecases: list[SOMcreator.UseCase] = list()
    active_phases: list[SOMcreator.Phase] = list()
    activate_object_filter = True
