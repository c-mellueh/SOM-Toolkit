from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass, field
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.main_window import Ui_MainWindow


class MenuDict(TypedDict):
    submenu: list[MenuDict]
    actions: list[QAction]
    menu: QMenu
    name: str


class MainWindowProperties:
    menu_dict: MenuDict = {
        "submenu": list(),
        "actions": list(),
        "menu":    None,
        "name":    "menubar",
    }
    active_main_window: Ui_MainWindow | None = None
