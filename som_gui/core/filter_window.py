from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open(filter_window: Type[tool.FilterWindow]):
    widget = filter_window.get()
    if widget is None:
        widget = filter_window.create_widget()
    widget.show()


def update_project_table(filter_window: Type[tool.FilterWindow]):
    logging.debug(f"Paint ProjectTable")
