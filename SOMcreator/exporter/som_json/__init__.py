from __future__ import annotations

import logging
import os
import json
import time

import SOMcreator
from SOMcreator.datastructure.som_json import MainDict
from typing import TYPE_CHECKING
from . import class_, core, project, predefined_pset, property_set, aggregation
from SOMcreator.templates import HOME_DIR, MAPPING_TEMPLATE
from SOMcreator.util import xml
import jinja2

if TYPE_CHECKING:
    from SOMcreator import SOMProject, UseCase, Phase
parent_dict = dict()
aggregation_dict = dict()
phase_list: list[Phase] = list()
use_case_list: list[UseCase] = list()
plugin_dict = dict()
class_uuid_dict: dict[str, SOMcreator.SOMClass] = dict()
property_set_uuid_dict: dict[str, SOMcreator.SOMPropertySet] = dict()
property_uuid_dict: dict[str, SOMcreator.SOMProperty] = dict()
filter_matrixes = list()


def create_mapping_script(project: SOMcreator.SOMProject, pset_name: str, path: str):
    property_dict = dict()
    som_class: SOMcreator.SOMClass
    for som_class in project.get_classes(filter=True):
        klass = som_class.identifier_property.allowed_values[0]
        class_dict = dict()
        for pset in som_class.get_property_sets(filter=True):
            pset_dict = dict()
            for som_property in pset.get_properties(filter=True):
                name = som_property.name
                data_format = xml.transform_data_format(som_property.data_type)
                pset_dict[name] = data_format
            class_dict[pset.name] = pset_dict
        property_dict[klass] = class_dict
    file_loader = jinja2.FileSystemLoader(HOME_DIR)
    env = jinja2.Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True

    template = env.get_template(MAPPING_TEMPLATE)
    code = template.render(attribute_dict=property_dict, pset_name=pset_name)
    with open(path, "w") as file:
        file.write(code)
    pass


def reset_uuid_dicts():
    SOMcreator.exporter.som_json.class_uuid_dict = dict()
    SOMcreator.exporter.som_json.property_set_uuid_dict = dict()
    SOMcreator.exporter.som_json.property_uuid_dict = dict()
    SOMcreator.exporter.som_json.filter_matrixes = list()


def export_json(proj: SOMProject, path: str | os.PathLike) -> dict:
    start_time = time.time()
    main_dict = create_export_dict(proj)
    with open(path, "w") as file:
        json.dump(project.order_dict(main_dict), file)

    end_time = time.time()
    logging.info(f"Export Done. Time: {end_time - start_time}")
    return main_dict


def create_export_dict(proj: SOMProject):
    main_dict: MainDict = dict()
    project.write(proj, main_dict)
    predefined_pset.write(proj, main_dict)
    class_.write(proj, main_dict)
    aggregation.write(proj, main_dict)
    main_dict.update(proj.plugin_dict)
    return main_dict
