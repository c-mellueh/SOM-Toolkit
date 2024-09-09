from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open_window(bsdd: Type[tool.Bsdd]):
    window = bsdd.get_window()
    window.show()
