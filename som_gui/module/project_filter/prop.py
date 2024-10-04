from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator import UseCase, Phase
    from .ui import ProjectFilterDialog


class ProjectFilterProperties:
    project_filter_dialog: ProjectFilterDialog = None
    use_cases: list[UseCase] = list()
    phases: list[Phase] = list()
    filter_matrix: list[list[bool]] = list()
    add_phases: list[Phase] = list()
    selected_header: UseCase | Phase = None
