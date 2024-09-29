from __future__ import annotations

import logging
import os
import json
import time

import SOMcreator
from .typing import MainDict
from typing import Type, TYPE_CHECKING
from . import constants, core, project, predefined_pset, property_set, obj, aggregation, inheritance
from ..Template import HOME_DIR, MAPPING_TEMPLATE
from ..external_software import xml
import jinja2

if TYPE_CHECKING:
    from SOMcreator.classes import Project, UseCase, Phase
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
    for obj in project.objects:
        klass = obj.ident_attrib.value[0]
        obj_dict = dict()
        for pset in obj.property_sets:
            pset_dict = dict()
            for attribute in pset.attributes:
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
    SOMcreator.filehandling.object_uuid_dict = dict()
    SOMcreator.filehandling.property_set_uuid_dict = dict()
    SOMcreator.filehandling.attribute_uuid_dict = dict()
    SOMcreator.filehandling.filter_matrixes = list()


def open_json(cls: Type[Project], path: str):
    start_time = time.time()

    SOMcreator.filehandling.parent_dict = dict()
    reset_uuid_dicts()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist!")

    with open(path, "r") as file:
        main_dict: MainDict = json.load(file)

    SOMcreator.filehandling.plugin_dict = dict(main_dict)
    SOMcreator.filehandling.filter_matrixes = main_dict.get("FilterMatrixes")
    project_dict = main_dict.get(constants.PROJECT)
    SOMcreator.filehandling.phase_list, SOMcreator.filehandling.use_case_list = core.get_filter_lists(project_dict)

    proj, project_dict = project.load(cls, main_dict)
    predefined_pset.load(proj, main_dict)

    obj.load(proj, main_dict)

    aggregation.load(proj, main_dict)

    inheritance.calculate(proj)
    aggregation.calculate(proj)
    proj.plugin_dict = SOMcreator.filehandling.plugin_dict
    proj.import_dict = main_dict
    end_time = time.time()
    logging.info(f"Export Done. Time: {end_time - start_time}")
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
