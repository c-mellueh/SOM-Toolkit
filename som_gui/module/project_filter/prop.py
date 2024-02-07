from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.classes import UseCase, Phase
    from .ui import ProjectFilterDialog


class ProjectFilterProperties:
    project_filter_dialog: ProjectFilterDialog = None
    use_cases: list[UseCase] = list()
    phases: list[Phase] = list()
    filter_matrix: list[list[bool]] = list()
    active_use_case: UseCase = None
    active_project_phase: Phase = None
    delete_use_cases: list[UseCase] = list()
    delete_phases: list[Phase] = list()
    add_use_cases: list[UseCase] = list()
    add_phases: list[Phase] = list()
    rename_dict: dict[UseCase | Phase, str] = dict()
    selected_header: UseCase | Phase = None
