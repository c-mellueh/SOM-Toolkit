from __future__ import annotations
from typing import TypedDict
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QLabel, QApplication

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow
    from som_gui.module.main_window.qt.window import Ui_MainWindow


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
    ui: Ui_MainWindow | None = None
    window: MainWindow = None
    status_bar_label: QLabel = None
    application: QApplication = None
    mapping_window = None
    attribute_import_window = None
    grouping_window = None
