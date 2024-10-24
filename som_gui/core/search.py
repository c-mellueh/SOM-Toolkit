from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def refresh_search_window(search_tool: Type[tool.Search]):
    widget = search_tool.get_dialog()
    threshold = search_tool.get_search_properties().filter_threshold
    search_tool.refresh_dialog(widget, threshold)


def retranslate_ui(search: Type[tool.Search]):
    widget = search.get_dialog()
    if not widget:
        return
    widget.ui.retranslateUi(widget)
    refresh_search_window(search)
    search.retranslate_title(widget, search.get_search_mode())
