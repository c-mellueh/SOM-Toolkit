from __future__ import annotations
from typing import TYPE_CHECKING, Type

from .constants import *
from SOMcreator.datastructure.som_json import ProjectDict, FilterDict, MainDict
import SOMcreator
from . import core
from collections import OrderedDict

if TYPE_CHECKING:
    from SOMcreator import Project


def _load_filter_matrix(project_dict: ProjectDict, use_case_list: list[SOMcreator.UseCase],
                        phase_list: list[SOMcreator.Phase]):
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


def _load_single_filter(current_state: str | int | None,
                        value_list: list[SOMcreator.UseCase] | list[SOMcreator.Phase]):
    # deprecated usecases were defined by name not int
    if isinstance(current_state, str):
        current_state = {value.name: value for value in value_list}.get(current_state)
    elif isinstance(current_state, int):
        current_state = value_list[current_state]
    if current_state is None:
        current_state = value_list[0]

    return current_state, value_list


def _load_usecases(project_dict: ProjectDict) -> tuple[list[int], list[SOMcreator.UseCase]]:
    active_usecases: list[int] = project_dict.get(ACTIVE_USECASES)
    use_case_list = SOMcreator.io.som_json.use_case_list

    if active_usecases is not None:
        return active_usecases, use_case_list

    #deprecated import only single Usecase
    current_use_case = project_dict.get(CURRENT_USE_CASE)
    usecase, phase_list = _load_single_filter(current_use_case, use_case_list)
    return [phase_list.index(usecase)], use_case_list


def _load_phases(project_dict: ProjectDict) -> tuple[list[int], list[SOMcreator.Phase]]:
    active_phases: list[int] = project_dict.get(ACTIVE_PHASES)
    phase_list = SOMcreator.io.som_json.phase_list

    if active_phases is not None:
        return active_phases, phase_list

    #deprecated import only single Phase

    current_project_phase = project_dict.get(CURRENT_PR0JECT_PHASE)
    phase, phase_list = _load_single_filter(current_project_phase, phase_list)
    return [phase_list.index(phase)], phase_list

def load(cls: Type[Project], main_dict: MainDict) -> tuple[Project, dict]:
    project_dict: ProjectDict = main_dict.get(PROJECT)
    core.remove_part_of_dict(PROJECT)

    name = project_dict.get(NAME)
    author = project_dict.get(AUTHOR)
    version = project_dict.get(VERSION)

    aggregation_pset_name = project_dict.get(AGGREGATION_PSET)
    aggregation_attribute = project_dict.get(AGGREGATION_ATTRIBUTE)

    active_use_cases, use_case_list = _load_usecases(project_dict)
    active_phases, phase_list = _load_phases(project_dict)
    filter_matrix = _load_filter_matrix(project_dict, use_case_list, phase_list)

    proj = cls(name, author, phase_list, use_case_list, filter_matrix)
    proj.version = version
    if aggregation_pset_name is not None:
        proj.aggregation_pset = aggregation_pset_name
    if aggregation_attribute is not None:
        proj.aggregation_attribute = aggregation_attribute

    proj.active_usecases = active_use_cases
    proj.active_phases = active_phases

    return proj, project_dict


def write(project: Project, main_dict: MainDict) -> None:
    main_dict[FILTER_MATRIXES] = create_existing_filter_states(project)
    SOMcreator.io.som_json.filter_matrixes = main_dict[FILTER_MATRIXES]
    main_dict[PROJECT] = dict()
    project_dict: ProjectDict = main_dict[PROJECT]
    project_dict[NAME] = project.name
    project_dict[AUTHOR] = project.author
    project_dict[VERSION] = project.version
    project_dict[AGGREGATION_ATTRIBUTE] = project.aggregation_attribute
    project_dict[AGGREGATION_PSET] = project.aggregation_pset
    project_dict[
        ACTIVE_PHASES] = project.active_phases  # project_dict[CURRENT_PR0JECT_PHASE] = project.get_project_phase_list().index(project.current_project_phase)
    project_dict[
        ACTIVE_USECASES] = project.active_usecases  #    project_dict[CURRENT_USE_CASE] = project.get_use_case_list().index(project.current_use_case)
    project_dict[PROJECT_PHASES] = _write_filter_dict(project.get_phases())
    project_dict[USE_CASES] = _write_filter_dict(project.get_usecases())
    project_dict[FILTER_MATRIX] = project.get_filter_matrix()


def order_dict(main_dict: MainDict):
    order = [PROJECT, PREDEFINED_PSETS, OBJECTS, AGGREGATIONS, FILTER_MATRIXES]
    ordered_data = [(name, main_dict.get(name)) for name in order]
    for key, data in main_dict.items():
        if key not in order:
            ordered_data.append((key, data))
    return OrderedDict(ordered_data)


def _write_filter_dict(filter_list: list[SOMcreator.Phase] | list[SOMcreator.UseCase]) -> list[FilterDict]:
    fl = list()
    for fil in filter_list:
        fl.append({
            "name":        fil.name,
            "long_name":   fil.long_name,
            "description": fil.description
        })
    return fl


def create_existing_filter_states(proj: Project):
    filter_matrixes = set()
    for entity in proj.get_hirarchy_items(filter=False):
        hashable = tuple(tuple(use_case_list) for use_case_list in entity.get_filter_matrix())
        filter_matrixes.add(hashable)
    return list(filter_matrixes)
