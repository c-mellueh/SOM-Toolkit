from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import SOMcreator
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtGui import QStandardItem
    from PySide6.QtCore import QItemSelectionModel, QModelIndex


def ifc_file_dialog_clicked(line_edit: QLineEdit, settings: Type[tool.Settings], ifc_importer: Type[tool.IfcImporter]):
    ifc_paths = settings.get_ifc_path()
    if isinstance(ifc_paths, list):
        ifc_paths = ifc_paths[0]
    path = ifc_importer.open_file_dialog(line_edit.window(), ifc_paths)
    if not path:
        return
    settings.set_ifc_path(path)
    line_edit.setText(settings.get_seperator().join(path))
