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
