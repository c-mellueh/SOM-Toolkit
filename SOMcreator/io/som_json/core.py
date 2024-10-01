from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import SOMcreator
from SOMcreator.io.som_json.constants import PROJECT_PHASES, USE_CASES, NAME, DESCRIPTION, OPTIONAL, PARENT, \
    FILTER_MATRIX

if TYPE_CHECKING:
    from SOMcreator import Project
    from SOMcreator.io.som_json.typing import ProjectDict, StandardDict, ObjectDict, PropertySetDict, \
        AttributeDict, \
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
                phase_list.append(SOMcreator.Phase(phase, phase, ""))
            else:
                phase_list.append(SOMcreator.Phase(phase["name"], phase.get("long_name"), phase.get("description")))
    else:
        phase_list = [SOMcreator.Phase("Stand", "Standard", "Automatisch generiert bitte aktualisieren")]
    if use_cases is not None and isinstance(use_cases, list):
        for use_case in use_cases:
            if isinstance(use_case, str):
                use_case_list.append(SOMcreator.UseCase(use_case, use_case, ""))
            else:
                use_case_list.append(
                    SOMcreator.UseCase(use_case["name"], use_case.get("long_name"), use_case.get("description")))
    else:
        use_case_list = [SOMcreator.UseCase("Stand", "Standard", "Automatisch generiert bitte aktualisieren")]
    return phase_list, use_case_list


def load_filter_matrix(proj: SOMcreator.Project, element_dict: StandardDict, guid: str):
    matrix: list[list[bool]] = element_dict.get(FILTER_MATRIX)
    if matrix is None:
        logging.warning(
            f"Achtung! Filtermatrix für Element '{guid}' liegt nicht vor. Eventuell verwenden Sie eine alte Dateiversion. Bitte mit SOM-Toolkit 2.11.3 Öffnen und neu speichern!")
        return proj.create_filter_matrix(True)
    if isinstance(matrix, int):
        return list(SOMcreator.io.som_json.filter_matrixes[matrix])
    if not check_size_eq(matrix, proj.get_filter_matrix()):
        logging.warning(
            f"Achtung! Filtermatrix für  Element '{guid}' hat die falsche Größe! Status wird überall auf True gesetzt!")
        return proj.create_filter_matrix(True)
    return matrix


def get_basics(proj: SOMcreator.Project, element_dict: StandardDict, guid: str) -> tuple[
    str, str, bool, str, list[list[bool]]]:
    name = element_dict[NAME]
    description = element_dict[DESCRIPTION]
    optional = element_dict[OPTIONAL]
    parent = element_dict[PARENT]
    matrix = load_filter_matrix(proj, element_dict, guid)
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
    if key in SOMcreator.io.som_json.plugin_dict:
        SOMcreator.io.som_json.plugin_dict.pop(key)


#### Export ######

def check_size_eq(lst: list[list[bool]], master_list: list[list[bool]]):
    phase_len = len(lst)
    usecase_len = len(lst[0])
    return phase_len == len(master_list) and usecase_len == len(master_list[0])


def write_filter_matrix(element: SOMcreator.ClassTypes):
    proj = element.project
    filter_matrix = element.get_filter_matrix()
    if not check_size_eq(filter_matrix, proj.get_filter_matrix()):
        logging.warning(f"Filter List of {element} doesn't match size of project filter list")
    return SOMcreator.io.som_json.filter_matrixes.index(
        tuple(tuple(use_case_list) for use_case_list in filter_matrix))


def write_basics(entity_dict: ObjectDict | PropertySetDict | AttributeDict | AggregationDict,
                 element: SOMcreator.ClassTypes) -> None:
    """function gets called from all Entities"""
    entity_dict[NAME] = element.name
    entity_dict[OPTIONAL] = element.is_optional(ignore_hirarchy=True)
    entity_dict[FILTER_MATRIX] = write_filter_matrix(element)
    parent = None if element.parent is None else element.parent.uuid
    entity_dict[PARENT] = parent
    entity_dict[DESCRIPTION] = element.description
