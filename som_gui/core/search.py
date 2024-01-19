from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import Search


def refresh_search_window(search_tool: Type[Search]):
    search_tool.refresh_dialog()
