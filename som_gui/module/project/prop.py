from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from SOMcreator import Project

if TYPE_CHECKING:
    from . import ui
    from PySide6.QtGui import QAction


class ProjectProperties:
    active_project: Project | None = None
    shourtcuts: list = list()
    plugin_save_functions: list[Callable] = list()
    settings_general_widget: ui.SettingsGeneral = None
    settings_path_widget: ui.SettingsPath = None
    actions: dict[str, QAction] = dict()
