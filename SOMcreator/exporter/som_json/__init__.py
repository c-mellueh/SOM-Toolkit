from __future__ import annotations

import logging
import os
import json
import time

import SOMcreator
from .constants import FILTER_MATRIXES
from SOMcreator.datastructure.som_json import MainDict
from typing import Type, TYPE_CHECKING
from . import constants, core, project, predefined_pset, property_set, obj, aggregation, inheritance
from SOMcreator.templates import HOME_DIR, MAPPING_TEMPLATE
from SOMcreator.util import xml
import jinja2

if TYPE_CHECKING:
    from SOMcreator import Project, UseCase, Phase
parent_dict = dict()
aggregation_dict = dict()
phase_list: list[Phase] = list()
use_case_list: list[UseCase] = list()
plugin_dict = dict()
object_uuid_dict: dict[str, SOMcreator.Object] = dict()
property_set_uuid_dict: dict[str, SOMcreator.PropertySet] = dict()
attribute_uuid_dict: dict[str, SOMcreator.Attribute] = dict()
filter_matrixes = list()


def create_mapping_script(project: SOMcreator.Project, pset_name: str, path: str):
    attrib_dict = dict()
    obj: SOMcreator.Object
    for obj in project.get_objects(filter=True):
        klass = obj.ident_attrib.value[0]
        obj_dict = dict()
        for pset in obj.get_property_sets(filter=True):
            pset_dict = dict()
            for attribute in pset.get_attributes(filter=True):
                name = attribute.name
                data_format = xml.transform_data_format(attribute.data_type)
                pset_dict[name] = data_format
            obj_dict[pset.name] = pset_dict
        attrib_dict[klass] = obj_dict
    file_loader = jinja2.FileSystemLoader(HOME_DIR)
    env = jinja2.Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True

    template = env.get_template(MAPPING_TEMPLATE)
    code = template.render(attribute_dict=attrib_dict, pset_name=pset_name)
    with open(path, "w") as file:
        file.write(code)
    pass


def reset_uuid_dicts():
    SOMcreator.exporter.som_json.object_uuid_dict = dict()
    SOMcreator.exporter.som_json.property_set_uuid_dict = dict()
    SOMcreator.exporter.som_json.attribute_uuid_dict = dict()
    SOMcreator.exporter.som_json.filter_matrixes = list()


def open_json(cls: Type[Project], path: str):
    start_time = time.time()

    SOMcreator.exporter.som_json.parent_dict = dict()
    reset_uuid_dicts()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist!")

    with open(path, "r") as file:
        main_dict: MainDict = json.load(file)

    SOMcreator.exporter.som_json.plugin_dict = dict(main_dict)
    SOMcreator.exporter.som_json.filter_matrixes = main_dict.get(FILTER_MATRIXES)
    core.remove_part_of_dict(FILTER_MATRIXES)

    logging.debug(f"Filter Matrixes Read")
    project_dict = main_dict.get(constants.PROJECT)
    SOMcreator.exporter.som_json.phase_list, SOMcreator.exporter.som_json.use_case_list = core.get_filter_lists(
        project_dict)
    logging.debug(f"Filter List Read")

    proj, project_dict = project.load(cls, main_dict)
    logging.debug(f"Project Read")

    predefined_pset.load(proj, main_dict)
    logging.debug(f"Predefined Pset Read")

    obj.load(proj, main_dict)
    logging.debug(f"Objects Read")

    aggregation.load(proj, main_dict)
    logging.debug(f"Aggregations Read")

    inheritance.calculate(proj)
    logging.debug(f"Inheritance Calculated")

    aggregation.calculate(proj)
    logging.debug(f"Aggregation Calculated")

    proj.plugin_dict = SOMcreator.exporter.som_json.plugin_dict
    proj.import_dict = main_dict
    end_time = time.time()
    logging.info(f"Import Done. Time: {end_time - start_time}")
    return proj


def export_json(proj: Project, path: str) -> dict:
    start_time = time.time()
    main_dict = create_export_dict(proj)
    with open(path, "w") as file:
        json.dump(project.order_dict(main_dict), file)

    end_time = time.time()
    logging.info(f"Export Done. Time: {end_time - start_time}")
    return main_dict


def create_export_dict(proj: Project):
    main_dict: MainDict = dict()
    project.write(proj, main_dict)
    predefined_pset.write(proj, main_dict)
    obj.write(proj, main_dict)
    aggregation.write(proj, main_dict)
    main_dict.update(proj.plugin_dict)
    return main_dict
