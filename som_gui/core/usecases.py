from __future__ import annotations

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui import tool

def create_main_menu_actions(
    usecases: Type[tool.Usecases], main_window: Type[tool.MainWindow]
):
    action = main_window.add_action("menuEdit", "UsecaseWindow", usecases.signaller.open_window.emit)
    usecases.set_action("open_window", action)
    usecases.connect_signals()

