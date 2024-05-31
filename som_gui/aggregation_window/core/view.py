from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.aggregation_window import tool as aw_tool
    from som_gui import tool


def import_positions(view: Type[aw_tool.View], project: Type[tool.Project]):
    proj = project.get()
    plugin_dict = proj.import_dict
    view.create_scene_dict(proj, plugin_dict)
