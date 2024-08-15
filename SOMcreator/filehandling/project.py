from __future__ import annotations
from typing import TYPE_CHECKING, Type

from .constants import PROJECT, NAME, AUTHOR, VERSION, AGGREGATION_PSET, AGGREGATION_ATTRIBUTE, CURRENT_PR0JECT_PHASE, \
    CURRENT_USE_CASE, FILTER_MATRIX, PROJECT_PHASES, USE_CASES
from .typing import ProjectDict, FilterDict, MainDict
import SOMcreator
from SOMcreator import classes
from SOMcreator.filehandling import core

if TYPE_CHECKING:
    from SOMcreator import Project


def _load_filter_matrix(project_dict: ProjectDict, use_case_list: list[classes.UseCase],
                        phase_list: list[classes.Phase]):
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


def _load_filter(current_state: str | int | None,
                 value_list: list[classes.UseCase] | list[classes.Phase]):
    if isinstance(current_state, str):
        current_state = {value.name: value for value in value_list}.get(current_state)
    elif isinstance(current_state, int):
        current_state = value_list[current_state]
    if current_state is None:
        current_state = value_list[0]

    return current_state, value_list


def _load_usecases(project_dict: ProjectDict) -> tuple[classes.UseCase, list[classes.UseCase]]:
    current_use_case = project_dict.get(CURRENT_USE_CASE)
    use_case_list = SOMcreator.filehandling.use_case_list
    return _load_filter(current_use_case, use_case_list)


def _load_phases(project_dict: ProjectDict) -> tuple[classes.Phase, list[classes.Phase]]:
    current_project_phase = project_dict.get(CURRENT_PR0JECT_PHASE)
    phase_list = SOMcreator.filehandling.phase_list
    return _load_filter(current_project_phase, phase_list)


def load(cls: Type[Project], main_dict: MainDict) -> tuple[Project, dict]:
    project_dict: ProjectDict = main_dict.get(PROJECT)
    core.remove_part_of_dict(PROJECT)

    name = project_dict.get(NAME)
    author = project_dict.get(AUTHOR)
    version = project_dict.get(VERSION)

    aggregation_pset_name = project_dict.get(AGGREGATION_PSET)
    aggregation_attribute = project_dict.get(AGGREGATION_ATTRIBUTE)

    current_use_case, use_case_list = _load_usecases(project_dict)
    current_phase, phase_list = _load_phases(project_dict)
    filter_matrix = _load_filter_matrix(project_dict, use_case_list, phase_list)

    proj = cls(name, author, phase_list, use_case_list, filter_matrix)
    proj.version = version
    if aggregation_pset_name is not None:
        proj.aggregation_pset = aggregation_pset_name
    if aggregation_attribute is not None:
        proj.aggregation_attribute = aggregation_attribute

    proj.current_use_case = current_use_case
    proj.current_project_phase = current_phase

    return proj, project_dict


def write(project, main_dict: MainDict) -> None:
    main_dict[PROJECT] = dict()
    project_dict: ProjectDict = main_dict[PROJECT]
    project_dict[NAME] = project.name
    project_dict[AUTHOR] = project.author
    project_dict[VERSION] = project.version
    project_dict[AGGREGATION_ATTRIBUTE] = project.aggregation_attribute
    project_dict[AGGREGATION_PSET] = project.aggregation_pset
    project_dict[CURRENT_PR0JECT_PHASE] = project.get_project_phase_list().index(project.current_project_phase)
    project_dict[CURRENT_USE_CASE] = project.get_use_case_list().index(project.current_use_case)
    project_dict[PROJECT_PHASES] = _write_filter_dict(project.get_project_phase_list())
    project_dict[USE_CASES] = _write_filter_dict(project.get_use_case_list())
    project_dict[FILTER_MATRIX] = project.get_filter_matrix()


def _write_filter_dict(filter_list: list[classes.Phase] | list[classes.UseCase]) -> list[FilterDict]:
    fl = list()
    for fil in filter_list:
        fl.append({
            "name":        fil.name,
            "long_name":   fil.long_name,
            "description": fil.description
        })
    return fl
