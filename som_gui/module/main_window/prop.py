from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypedDict

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu
import SOMcreator
if TYPE_CHECKING:
    from som_gui.module.main_window.ui import MainWindow
    from som_gui.module.main_window.qt.ui_MainWindow import Ui_MainWindow

class MainWindowProperties:
    ui: Ui_MainWindow | None = None
    window: MainWindow = None
    application: QApplication = None
    active_class:SOMcreator.SOMClass = None
    actions: dict[str, QAction] = dict()
    #Most Modules have an Actions dict. In this dict The Actions of the MainMenubar are stored. and can be called by get/set action w/ their name
    #This is Mostly used for translating the Actions on Language change
