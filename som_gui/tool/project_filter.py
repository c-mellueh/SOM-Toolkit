from __future__ import annotations
import som_gui.core.tool
from som_gui.module import project_filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.project_filter.prop import ProjectFilterProperties


class ProjectFilter(som_gui.core.tool.ProjectFilter):

    @classmethod
    def get_properties(cls) -> ProjectFilterProperties:
        return som_gui.ProjectFilterProperties

    @classmethod
    def create_dialog(cls):
        dialog = cls.get_properties().project_filter_dialog

        if not dialog:
            dialog = project_filter.ui.ProjectFilterDialog()
        cls.get_properties().project_filter_dialog = dialog
        return dialog
