from __future__ import annotations
from typing import TYPE_CHECKING, Type

from SOMcreator.datastructure.som_json import (
    DESCRIPTION,
    FILTER_MATRIXES,
    FILTER_MATRIX,
    ACTIVE_USECASES,
    ACTIVE_PHASES,
    CURRENT_PR0JECT_PHASE,
    CURRENT_USE_CASE,
    PROJECT,
    NAME,
    AUTHOR,
    VERSION,
    AGGREGATION_PSET,
    AGGREGATION_PROPERTY,
    PROJECT_PHASES,
    USE_CASES,
    PREDEFINED_PSETS,
    CLASSES,
    AGGREGATIONS,
)
from SOMcreator.datastructure.som_json import ProjectDict, FilterDict, MainDict
import SOMcreator
from . import core
from collections import OrderedDict

if TYPE_CHECKING:
    from SOMcreator import SOMProject


def write(project: SOMProject, main_dict: MainDict) -> None:
    main_dict[FILTER_MATRIXES] = create_existing_filter_states(project)
    SOMcreator.exporter.som_json.filter_matrixes = main_dict[FILTER_MATRIXES]
    main_dict[PROJECT] = dict()
    project_dict: ProjectDict = main_dict[PROJECT]
    project_dict[NAME] = project.name
    project_dict[AUTHOR] = project.author
    project_dict[VERSION] = project.version
    project_dict[DESCRIPTION] = project.description
    project_dict[AGGREGATION_PROPERTY] = project.aggregation_property
    project_dict[AGGREGATION_PSET] = project.aggregation_pset
    project_dict[ACTIVE_PHASES] = (
        project.active_phases
    )  # project_dict[CURRENT_PR0JECT_PHASE] = project.get_project_phase_list().index(project.current_project_phase)
    project_dict[ACTIVE_USECASES] = (
        project.active_usecases
    )  #    project_dict[CURRENT_USE_CASE] = project.get_use_case_list().index(project.current_use_case)
    project_dict[PROJECT_PHASES] = _write_filter_dict(project.get_phases())
    project_dict[USE_CASES] = _write_filter_dict(project.get_usecases())
    project_dict[FILTER_MATRIX] = project.get_filter_matrix()


def order_dict(main_dict: MainDict):
    order = [PROJECT, PREDEFINED_PSETS, CLASSES, AGGREGATIONS, FILTER_MATRIXES]
    ordered_data = [(name, main_dict.get(name)) for name in order]
    for key, data in main_dict.items():
        if key not in order:
            ordered_data.append((key, data))
    return OrderedDict(ordered_data)


def _write_filter_dict(
    filter_list: list[SOMcreator.Phase] | list[SOMcreator.UseCase],
) -> list[FilterDict]:
    fl = list()
    for fil in filter_list:
        fl.append(
            {
                "name": fil.name,
                "long_name": fil.long_name,
                "description": fil.description,
            }
        )
    return fl


def create_existing_filter_states(proj: SOMProject):
    filter_matrixes = set()
    for entity in proj.get_items(filter=False):
        hashable = tuple(
            tuple(use_case_list) for use_case_list in entity.get_filter_matrix()
        )
        filter_matrixes.add(hashable)
    return list(filter_matrixes)
