from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, ObjectCheckWidget
    from PySide6.QtCore import QThreadPool
    from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel


class ModelcheckWindowProperties:
    active_window: ModelcheckWindow = None
    checkbox_widget: ObjectCheckWidget = None
    check_state_dict: dict[SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute, bool] = None
    enabled_dict: dict[SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute, bool] = None
    selected_object: SOMcreator.Object = None
    thread_pool: QThreadPool = None
    export_button: QPushButton = None
    export_line_edit: QLineEdit = None
    run_button: QPushButton = None
    abort_button: QPushButton = None
    ifc_import_widget = None
    status_label: QLabel = None
    ifc_import_runners = list()
    initial_paint = True
