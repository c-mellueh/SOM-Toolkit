from __future__ import annotations

import json
import os
import SOMcreator
from SOMcreator.constants import value_constants
from SOMcreator.util import xml

DATA_TYPE = "data_type"
VALUE_TYPE = "value_Type"
VALUE = "value"


def _iter_properties(property_set: SOMcreator.SOMPropertySet, pset_dict: dict) -> None:
    for som_property in property_set.get_properties(filter=True):
        pset_dict[som_property.name] = dict()
        property_dict = pset_dict[som_property.name]

        property_dict[DATA_TYPE] = xml.transform_data_format(som_property.data_type)
        if not som_property.allowed_values:
            property_dict[VALUE_TYPE] = value_constants.EXISTS
        else:
            property_dict[VALUE_TYPE] = som_property.value_type
        property_dict[VALUE] = som_property.allowed_values


def export(project: SOMcreator.SOMProject, path: str | os.PathLike) -> None:
    json_dict = dict()
    for som_class in sorted(project.get_classes(filter=True), key=lambda x: x.ident_value):
        if not som_class.get_property_sets(filter=True):
            continue
        if som_class.ident_value is None:
            continue
        json_dict[som_class.ident_value] = dict()
        class_dict = json_dict[som_class.ident_value]
        for property_set in som_class.get_property_sets(filter=True):
            if not property_set.get_properties(filter=True):
                continue
            class_dict[property_set.name] = dict()
            pset_dict = class_dict[property_set.name]
            _iter_properties(property_set, pset_dict)
    with open(path, "w") as file:
        json.dump(json_dict, file, indent=1)
