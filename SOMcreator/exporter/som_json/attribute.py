from __future__ import annotations
import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.datastructure.som_json import VALUE, VALUE_TYPE, DATA_TYPE, CHILD_INHERITS_VALUE, REVIT_MAPPING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import AttributeDict


def write(attribute: SOMcreator.Attribute) -> AttributeDict:
    attribute_dict: AttributeDict = dict()
    core.write_basics(attribute_dict, attribute)
    attribute_dict[DATA_TYPE] = attribute.data_type
    attribute_dict[VALUE_TYPE] = attribute.value_type
    attribute_dict[CHILD_INHERITS_VALUE] = attribute.child_inherits_values
    attribute_dict[REVIT_MAPPING] = attribute.revit_name
    attribute_dict[VALUE] = attribute.get_own_values()
    return attribute_dict
