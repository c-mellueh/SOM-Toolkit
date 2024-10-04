from __future__ import annotations
from SOMcreator import Project
from PySide6.QtWidgets import QDialog
from typing import TypedDict, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from . import ui


class ProjectProperties:
    active_project: Project | None = None
    shourtcuts: list = list()
    plugin_save_functions: list[Callable] = list()
    settings_general_widget: ui.SettingsGeneral = None
    settings_path_widget: ui.SettingsPath = None
