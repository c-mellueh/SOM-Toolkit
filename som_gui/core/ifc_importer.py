from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import SOMcreator
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.util.constants import PATH_SEPERATOR
if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QLineEdit

IFC_PATH = "ifc_path"


def ifc_file_dialog_clicked(line_edit: QLineEdit, appdata: Type[tool.Appdata], ifc_importer: Type[tool.IfcImporter]):
    ifc_paths = appdata.get_path(IFC_PATH)
    if isinstance(ifc_paths, list):
        ifc_paths = ifc_paths[0]
    path = ifc_importer.open_file_dialog(line_edit.window(), ifc_paths)
    if not path:
        return
    appdata.set_path(IFC_PATH, path)

    line_edit.setText(PATH_SEPERATOR.join(path))
