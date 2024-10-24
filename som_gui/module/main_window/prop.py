from __future__ import annotations
from typing import TypedDict
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QLabel, QApplication

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow
    from som_gui.module.main_window.qt.ui_MainWindow import Ui_MainWindow


class MenuDict(TypedDict):
    submenu: list[MenuDict]
    actions: list[QAction]
    menu: QMenu
    name: str


class MainWindowProperties:
    ui: Ui_MainWindow | None = None
    window: MainWindow = None
    application: QApplication = None
    mapping_window = None
    grouping_window = None
    actions: dict[str, QAction] = dict()
