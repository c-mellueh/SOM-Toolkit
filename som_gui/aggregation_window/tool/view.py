from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.aggregation_window.core.tool
from som_gui.aggregation_window.module.view import ui as ui_view

if TYPE_CHECKING:
    from som_gui.aggregation_window.module.view.prop import ViewProperties


class View(som_gui.aggregation_window.core.tool.View):
    @classmethod
    def get_properties(cls) -> ViewProperties:
        return som_gui.ViewProperties

    @classmethod
    def create_view(cls) -> ui_view.AggregationView:
        view = ui_view.AggregationView()
        cls.get_properties().aggregation_view = view
        return view

    @classmethod
    def create_scene(cls) -> ui_view.AggregationScene:
        scene = ui_view.AggregationScene()
        cls.get_properties().active_scene = scene
        return scene
