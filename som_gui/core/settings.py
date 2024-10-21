from __future__ import annotations

import logging

from som_gui import tool
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import QCoreApplication
if TYPE_CHECKING:
    from som_gui import tool


def create_main_menu_actions(settings: Type[tool.Settings], main_window: Type[tool.MainWindow]) -> None:
    from som_gui.module.settings import trigger
    action = main_window.add_action2("menuEdit", "Settings", trigger.open_window)
    settings.set_action("open_window", action)


def retranslate_ui(settings: Type[tool.Settings], ):
    open_window_action = settings.get_action("open_window")
    open_window_action.setText(QCoreApplication.translate("Settings", "Settings"))
    if settings.get_widget():
        settings.get_widget().retranslate_ui()

def open_window(settings: Type[tool.Settings]):
    logging.info(f"Opening Settings Window")
    dialog = settings.create_dialog()
    retranslate_ui(settings)
    if dialog.exec():
        for func in settings.get_accept_functions():
            func()
    settings.close()
