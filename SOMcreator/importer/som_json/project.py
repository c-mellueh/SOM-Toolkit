from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

import SOMcreator
import SOMcreator.importer.som_json
from SOMcreator.datastructure.som_json import (
    ACTIVE_PHASES,
    ACTIVE_USECASES,
    AGGREGATION_PROPERTY,
    AGGREGATION_PSET,
    AUTHOR,
    CURRENT_PR0JECT_PHASE,
    CURRENT_USE_CASE,
    DESCRIPTION,
    FILTER_MATRIX,
    MainDict,
    NAME,
    PROJECT,
    ProjectDict,
    VERSION,
)
from . import core

if TYPE_CHECKING:
    from SOMcreator import SOMProject


def _load_filter_matrix(
    project_dict: ProjectDict,
    use_case_list: list[SOMcreator.UseCase],
    phase_list: list[SOMcreator.Phase],
):
    old_filter_matrix: list[list[bool]] = project_dict.get(FILTER_MATRIX)
    filter_matrix = list()
    for _ in phase_list:
        filter_matrix.append([True for __ in use_case_list])

    if old_filter_matrix is None:
        return filter_matrix

    for old_phase, new_phase in zip(old_filter_matrix, filter_matrix):
        for index, old_value in enumerate(old_phase):
            new_phase[index] = old_value

    return filter_matrix


def _load_single_filter(
    current_state: str | int | None,
    value_list: list,
) -> tuple:
    # deprecated usecases were defined by name not int
    current_filter = None
    if isinstance(current_state, str):
        filter_dict = {value.name: value for value in value_list}
        current_filter = filter_dict.get(current_state)
    elif isinstance(current_state, int):
        current_filter = value_list[current_state]
    elif isinstance(current_state, SOMcreator.UseCase | SOMcreator.Phase):
        current_filter = current_state
    if current_filter is None:
        current_filter = value_list[0]

    return current_filter, value_list


def _load_usecases(
    project_dict: ProjectDict,
) -> tuple[list[int], list[SOMcreator.UseCase]]:
    active_usecases: list[int] = project_dict.get(ACTIVE_USECASES)
    use_case_list = SOMcreator.importer.som_json.use_case_list

    if active_usecases is not None:
        return active_usecases, use_case_list

    # deprecated import only single Usecase
    current_use_case = project_dict.get(CURRENT_USE_CASE)
    usecase, phase_list = _load_single_filter(current_use_case, use_case_list)
    return [phase_list.index(usecase)], use_case_list


def _load_phases(project_dict: ProjectDict) -> tuple[list[int], list[SOMcreator.Phase]]:
    active_phases: list[int] = project_dict.get(ACTIVE_PHASES)
    phase_list = SOMcreator.importer.som_json.phase_list

    if active_phases is not None:
        return active_phases, phase_list

    # deprecated import only single Phase

    current_project_phase = project_dict.get(CURRENT_PR0JECT_PHASE)
    phase, phase_list = _load_single_filter(current_project_phase, phase_list)
    return [phase_list.index(phase)], phase_list


def load(cls: Type[SOMProject], main_dict: MainDict) -> tuple[SOMProject, ProjectDict]:
    project_dict: ProjectDict = main_dict.get(PROJECT)
    core.remove_part_of_dict(PROJECT)

    name: str = project_dict.get(NAME)
    author = project_dict.get(AUTHOR)
    version = project_dict.get(VERSION)
    description = project_dict.get(DESCRIPTION) or ""
    aggregation_pset_name = project_dict.get(AGGREGATION_PSET)
    aggregation_property = project_dict.get(AGGREGATION_PROPERTY)

    active_use_cases, use_case_list = _load_usecases(project_dict)
    active_phases, phase_list = _load_phases(project_dict)
    filter_matrix = _load_filter_matrix(project_dict, use_case_list, phase_list)

    proj = cls(name, author, phase_list, use_case_list, filter_matrix)
    proj.version = version
    proj.description = description
    if aggregation_pset_name is not None:
        proj.aggregation_pset = aggregation_pset_name
    if aggregation_property is not None:
        proj.aggregation_property = aggregation_property

    proj.active_usecases = active_use_cases
    proj.active_phases = active_phases

    return proj, project_dict
