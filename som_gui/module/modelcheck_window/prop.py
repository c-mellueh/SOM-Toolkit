from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, PsetTree, ClassTree
    from PySide6.QtCore import QThreadPool, QItemSelectionModel
    from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel
    from PySide6.QtGui import QStandardItemModel, QAction
    from som_gui.tool.ifc_importer import IfcImportRunner


class ModelcheckWindowProperties:
    active_window: ModelcheckWindow = None
    check_state_dict: dict[
        SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty, bool
    ] = None
    selected_class: SOMcreator.SOMClass = None
    thread_pool: QThreadPool = None
    export_button: QPushButton = None
    export_line_edit: QLineEdit = None
    run_button: QPushButton = None
    abort_button: QPushButton = None
    ifc_import_widget = None
    status_label: QLabel = None
    ifc_import_runners: list[IfcImportRunner] = list()
    initial_paint = True
    class_tree: ClassTree = None
    class_tree_model: QStandardItemModel|None = None
    class_tree_selection_model: QItemSelectionModel = None
    property_set_tree: PsetTree = None
    pset_tree_model: QStandardItemModel = None
    pset_tree_selection_model: QStandardItemModel = None
    actions: dict[str, QAction] = dict()
    class_label = None
