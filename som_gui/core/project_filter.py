from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open_project_filter_window(project_filter_tool: Type[tool.ProjectFilter], project_tool: Type[tool.Project]):
    window = project_filter_tool.create_dialog()
    window.show()
    pass
