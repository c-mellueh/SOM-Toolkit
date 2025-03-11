from __future__ import annotations

import logging
import os
import json
import time
import SOMcreator.importer.som_json
import SOMcreator
import SOMcreator.datastructure.som_json
from SOMcreator.datastructure.som_json import FILTER_MATRIXES, MainDict
from typing import Type, TYPE_CHECKING
from . import (
    core,
    project,
    predefined_pset,
    property_set,
    obj,
    aggregation,
    inheritance,
)

if TYPE_CHECKING:
    from SOMcreator import SOMProject, UseCase, Phase
parent_dict = dict()
aggregation_dict: dict[SOMcreator.SOMAggregation, tuple[str | None, int]] = dict()
phase_list: list[Phase] = list()
use_case_list: list[UseCase] = list()
plugin_dict = dict()
class_uuid_dict: dict[str, SOMcreator.SOMClass] = dict()
property_set_uuid_dict: dict[str, SOMcreator.SOMPropertySet] = dict()
property_uuid_dict: dict[str, SOMcreator.SOMProperty] = dict()
filter_matrixes = list()


def reset_uuid_dicts():
    SOMcreator.importer.som_json.class_uuid_dict = dict()
    SOMcreator.importer.som_json.property_set_uuid_dict = dict()
    SOMcreator.importer.som_json.property_uuid_dict = dict()
    SOMcreator.importer.som_json.filter_matrixes = list()


def open_json(cls: Type[SOMProject], path: str | os.PathLike):
    start_time = time.time()

    SOMcreator.importer.som_json.parent_dict = dict()
    reset_uuid_dicts()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist!")

    with open(path, "r") as file:
        main_dict: MainDict = json.load(file)

    SOMcreator.importer.som_json.plugin_dict = dict(main_dict)
    SOMcreator.importer.som_json.filter_matrixes = main_dict.get(FILTER_MATRIXES)
    core.remove_part_of_dict(FILTER_MATRIXES)

    logging.debug(f"Filter Matrixes Read")
    project_dict = main_dict.get(SOMcreator.datastructure.som_json.PROJECT)
    (
        SOMcreator.importer.som_json.phase_list,
        SOMcreator.importer.som_json.use_case_list,
    ) = core.get_filter_lists(project_dict)
    logging.debug(f"Filter List Read")

    proj, project_dict = project.load(cls, main_dict)
    logging.debug(f"Project Read")

    predefined_pset.load(proj, main_dict)
    logging.debug(f"Predefined Pset Read")

    obj.load(proj, main_dict)
    logging.debug(f"Classes Read")

    aggregation.load(proj, main_dict)
    logging.debug(f"Aggregations Read")

    inheritance.calculate(proj)
    logging.debug(f"Inheritance Calculated")

    aggregation.calculate(proj)
    logging.debug(f"Aggregation Calculated")

    proj.plugin_dict = SOMcreator.importer.som_json.plugin_dict
    proj.import_dict = main_dict
    end_time = time.time()
    logging.info(f"Import Done. Time: {end_time - start_time}")
    return proj
