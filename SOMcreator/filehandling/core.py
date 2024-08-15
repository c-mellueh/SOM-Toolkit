from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from SOMcreator import classes
import SOMcreator
from SOMcreator.filehandling.constants import PROJECT_PHASES, USE_CASES, NAME, DESCRIPTION, OPTIONAL, PARENT, \
    FILTER_MATRIX

if TYPE_CHECKING:
    from SOMcreator import Project
    from SOMcreator.filehandling.typing import ProjectDict, StandardDict, ObjectDict, PropertySetDict, AttributeDict, \
        AggregationDict


##### Import #####

def get_filter_lists(project_dict: ProjectDict):
    project_phases = project_dict.get(PROJECT_PHASES)
    use_cases = project_dict.get(USE_CASES)
    phase_list = list()
    use_case_list = list()
    if project_phases is not None and isinstance(project_phases, list):
        for phase in project_phases:
            if isinstance(phase, str):
                phase_list.append(classes.Phase(phase, phase, ""))
            else:
                phase_list.append(classes.Phase(phase["name"], phase.get("long_name"), phase.get("description")))
    else:
        phase_list = [classes.Phase("Stand", "Standard", "Automatisch generiert bitte aktualisieren")]
    if use_cases is not None and isinstance(use_cases, list):
        for use_case in use_cases:
            if isinstance(use_case, str):
                use_case_list.append(classes.UseCase(use_case, use_case, ""))
            else:
                use_case_list.append(
                    classes.UseCase(use_case["name"], use_case.get("long_name"), use_case.get("description")))
    else:
        use_case_list = [classes.UseCase("Stand", "Standard", "Automatisch generiert bitte aktualisieren")]
    return phase_list, use_case_list


def get_basics(proj: SOMcreator.Project, element_dict: StandardDict) -> tuple[str, str, bool, str, list[list[bool]]]:
    def get_value(d: dict, p: str) -> bool:
        return d.get(p) if d.get(p) is not None else True

    name = element_dict[NAME]
    description = element_dict[DESCRIPTION]
    optional = element_dict[OPTIONAL]
    parent = element_dict[PARENT]
    matrix = element_dict.get(FILTER_MATRIX)
    phase_list, use_case_list = SOMcreator.filehandling.phase_list, SOMcreator.filehandling.use_case_list
    matrix_list = list()
    for _ in proj.get_project_phase_list():
        matrix_list.append([True for __ in proj.get_use_case_list()])

    if matrix is None:  # handle deprecated file types
        matrix = list()
        file_phases: list[bool] = element_dict.get(PROJECT_PHASES)
        if isinstance(file_phases, dict):  # deprecated
            output_phases = [get_value(file_phases, phase.name) for phase in proj.get_project_phase_list()]
        elif file_phases is None:
            output_phases = [True for _ in proj.get_project_phase_list()]
        else:
            output_phases = [True for _ in proj.get_project_phase_list()]
            for output_index, existing_phase in enumerate(proj.get_project_phase_list()):
                if existing_phase in phase_list:
                    value = file_phases[phase_list.index(existing_phase)]
                    output_phases[output_index] = value

        file_use_cases: list[bool] = element_dict.get(USE_CASES)
        if file_use_cases is None:
            output_use_cases = [True for _ in proj.get_use_case_list()]
        else:
            output_use_cases = [True for _ in proj.get_use_case_list()]
            for output_index, existing_use_case in enumerate(proj.get_use_case_list()):
                if existing_use_case in use_case_list:
                    value = file_use_cases[use_case_list.index(existing_use_case)]
                    output_use_cases[output_index] = value

        for phase_index, phase in enumerate(output_phases):
            pl = list()
            for use_case_index, use_case in enumerate(output_use_cases):
                pl.append(bool(output_phases[phase_index] and output_use_cases[use_case_index]))
            matrix.append(pl)

    phase_count = len(SOMcreator.filehandling.phase_list)
    use_case_count = len(SOMcreator.filehandling.use_case_list)

    if phase_count > len(matrix):
        for _ in range(phase_count - len(matrix)):
            matrix.append([True for _ in range(use_case_count)])
    elif phase_count < len(matrix):
        matrix = matrix[:phase_count]

    for phase_index, use_case_list in enumerate(matrix):
        if use_case_count > len(use_case_list):
            [use_case_list.append(True) for _ in range(use_case_count - len(use_case_list))]
        elif use_case_count < len(use_case_list):
            use_case_list = use_case_list[:use_case_count]
        matrix[phase_index] = use_case_list
    return name, description, optional, parent, matrix


def check_dict(d: dict | None, d_name: str) -> bool:
    if d is None:
        logging.error(f"loading Error: {d_name} doesn't exist!")
        return True
    return False


def remove_part_of_dict(key):
    """
    Removes part of plugin dict if its saved in Core
    :param key:
    :return:
    """
    SOMcreator.filehandling.plugin_dict.pop(key)


#### Export ######

def write_filter_matrix(element: classes.ClassTypes):
    proj = element.project
    phases = proj.get_project_phase_list()
    use_cases = proj.get_use_case_list()
    matrix = list()
    for phase in phases:
        phase_list = list()
        for use_case in use_cases:
            phase_list.append(element.get_filter_state(phase, use_case))
        matrix.append(phase_list)
    return matrix


def write_basics(entity_dict: ObjectDict | PropertySetDict | AttributeDict | AggregationDict,
                 element: classes.ClassTypes) -> None:
    """function gets called from all Entities"""
    entity_dict[NAME] = element.name
    entity_dict[OPTIONAL] = element.optional
    entity_dict[FILTER_MATRIX] = write_filter_matrix(element)
    parent = None if element.parent is None else element.parent.uuid
    entity_dict[PARENT] = parent
    entity_dict[DESCRIPTION] = element.description
