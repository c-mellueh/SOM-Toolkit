from __future__ import annotations

import logging

from som_gui import tool
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open_window(settings: Type[tool.Settings]):
    logging.info(f"Opening Settings Window")
    if not settings.get_widget():
        widget = settings.create_widget()
        settings.set_widget(widget)

    widget = settings.get_widget()
    widget.show()
