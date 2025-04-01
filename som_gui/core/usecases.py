from __future__ import annotations
from PySide6.QtCore import QCoreApplication
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui import tool

def create_main_menu_actions(
    usecases: Type[tool.Usecases], main_window: Type[tool.MainWindow]
):
    action = main_window.add_action("menuEdit", "UsecaseWindow", usecases.signaller.open_window.emit)
    usecases.set_action("open_window", action)
    usecases.connect_signals()

def retranslate_ui(usecases: Type[tool.Usecases], util: Type[tool.Util]):
    action = usecases.get_action("open_window")
    action.setText(QCoreApplication.translate("UsecaseWindow", "Usecases"))

    window = usecases.get_window()
    if window:
        title = QCoreApplication.translate("UsecaseWindow", "Project Filter")
        window.ui.retranslateUi(window)
        window.setWindowTitle(util.get_window_title(title))