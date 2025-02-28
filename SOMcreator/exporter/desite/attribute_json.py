from __future__ import annotations

import json
import os
import SOMcreator
from SOMcreator.constants import value_constants
from SOMcreator.util import xml

DATA_TYPE = "data_type"
VALUE_TYPE = "value_Type"
VALUE = "value"


def _iter_attributes(property_set: SOMcreator.SOMPropertySet, pset_dict: dict) -> None:
    for attribute in property_set.get_attributes(filter=True):
        pset_dict[attribute.name] = dict()
        attribute_dict = pset_dict[attribute.name]

        attribute_dict[DATA_TYPE] = xml.transform_data_format(attribute.data_type)
        if not attribute.value:
            attribute_dict[VALUE_TYPE] = value_constants.EXISTS
        else:
            attribute_dict[VALUE_TYPE] = attribute.value_type
        attribute_dict[VALUE] = attribute.value


def export(project: SOMcreator.SOMProject, path: str | os.PathLike) -> None:
    json_dict = dict()
    for obj in sorted(project.get_objects(filter=True), key=lambda x: x.ident_value):
        if not obj.get_property_sets(filter=True):
            continue
        if obj.ident_value is None:
            continue
        json_dict[obj.ident_value] = dict()
        obj_dict = json_dict[obj.ident_value]
        for property_set in obj.get_property_sets(filter=True):
            if not property_set.get_attributes(filter=True):
                continue
            obj_dict[property_set.name] = dict()
            pset_dict = obj_dict[property_set.name]
            _iter_attributes(property_set, pset_dict)
    with open(path, "w") as file:
        json.dump(json_dict, file, indent=1)
