from __future__ import annotations

import json
import os
from ... import classes
from ...constants import json_constants, value_constants
from ...external_software import xml


def _iter_attributes(property_set: classes.PropertySet, pset_dict: dict) -> None:
    for attribute in property_set.attributes:
        pset_dict[attribute.name] = dict()
        attribute_dict = pset_dict[attribute.name]

        attribute_dict[json_constants.DATA_TYPE] = xml.transform_data_format(attribute.data_type)
        if not attribute.value:
            attribute_dict[json_constants.VALUE_TYPE] = value_constants.EXISTS
        else:
            attribute_dict[json_constants.VALUE_TYPE] = attribute.value_type
        attribute_dict[json_constants.VALUE] = attribute.value


def export(project: classes.Project, path: str | os.PathLike) -> None:
    json_dict = dict()
    for obj in sorted(project.objects, key=lambda x: x.ident_value):
        if not obj.property_sets:
            continue
        if obj.ident_value is None:
            continue
        json_dict[obj.ident_value] = dict()
        obj_dict = json_dict[obj.ident_value]
        for property_set in obj.property_sets:
            if not property_set.attributes:
                continue
            obj_dict[property_set.name] = dict()
            pset_dict = obj_dict[property_set.name]
            _iter_attributes(property_set, pset_dict)
    with open(path, "w") as file:
        json.dump(json_dict, file, indent=1)
