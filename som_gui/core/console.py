from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def show(console: Type[tool.Console]):
    con = console.create_console()


def close(console: Type[tool.Console]):
    console.close_console()
