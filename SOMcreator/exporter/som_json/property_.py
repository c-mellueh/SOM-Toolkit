from __future__ import annotations
import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.datastructure.som_json import (
    VALUE,
    VALUE_TYPE,
    DATA_TYPE,
    CHILD_INHERITS_VALUE,
    REVIT_MAPPING,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import PropertyDict


def write(som_property: SOMcreator.SOMProperty) -> PropertyDict:
    property_dict: PropertyDict = dict()
    core.write_basics(property_dict, som_property)
    property_dict[DATA_TYPE] = som_property.data_type
    property_dict[VALUE_TYPE] = som_property.value_type
    property_dict[CHILD_INHERITS_VALUE] = som_property.child_inherits_values
    property_dict[REVIT_MAPPING] = som_property.revit_name
    property_dict[VALUE] = som_property.get_own_values()
    return property_dict
