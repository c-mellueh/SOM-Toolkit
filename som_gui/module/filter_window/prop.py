from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import SOMcreator

if TYPE_CHECKING:
    from . import ui
    from som_gui.module.property_.ui import PropertyWidget


class FilterWindowProperties:
    settings_widget: ui.SettingsWidget = None
    actions: dict[str, QAction] = dict()
    
class FilterCompareProperties:
    widget: PropertyWidget = None
    usecase_list = list()
    use_case_indexes = list()
    phase_list = list()
    phase_indexes = list()
    projects = [None, None]
    match_list = []
