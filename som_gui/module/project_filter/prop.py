from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ProjectFilterDialog


class ProjectFilterProperties:
    project_filter_dialog: ProjectFilterDialog = None
