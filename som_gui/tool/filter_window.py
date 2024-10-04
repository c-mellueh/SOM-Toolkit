from __future__ import annotations

from idlelib.autocomplete import completion_kwds
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.filter_window.prop import FilterWindowProperties
from som_gui.module.filter_window import ui, trigger
class FilterWindow(som_gui.core.tool.FilterWindow):
    @classmethod
    def get_properties(cls) -> FilterWindowProperties:
        return som_gui.FilterWindowProperties

    @classmethod
    def get_project_table(cls) -> ui.ProjectTable:
        return cls.get().ui.project_table

    @classmethod
    def get_object_tree(cls):
        return cls.get().ui.object_tree

    @classmethod
    def get_pset_tree(cls):
        return cls.get().ui.pset_tree

    @classmethod
    def create_widget(cls) -> ui.FilterWidget:
        cls.get_properties().widget = ui.FilterWidget()

        # Connect Project Table Triggers
        project_table = cls.get_project_table()
        project_table.horizontalHeader().customContextMenuRequested.connect(trigger.pt_horizontal_context_requested)
        project_table.verticalHeader().customContextMenuRequested.connect(trigger.pt_vertical_context_requested)
        project_table.itemClicked.connect(trigger.pt_item_clicked)
        return cls.get_properties().widget

    @classmethod
    def get(cls) -> ui.FilterWidget | None:
        return cls.get_properties().widget
