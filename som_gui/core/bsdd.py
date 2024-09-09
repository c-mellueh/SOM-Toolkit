from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open_window(bsdd: Type[tool.Bsdd]):
    window = bsdd.get_window()
    if not window:
        window = bsdd.create_window()
    window.show()
