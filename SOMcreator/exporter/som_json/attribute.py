from __future__ import annotations
import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.exporter.som_json.constants import VALUE, VALUE_TYPE, DATA_TYPE, CHILD_INHERITS_VALUE, REVIT_MAPPING
from SOMcreator.constants.value_constants import OLD_DATATYPE_DICT
from SOMcreator.exporter import som_json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.exporter.som_json.typing import AttributeDict


def load(proj: SOMcreator.Project, attribute_dict: dict, identifier: str,
         property_set: SOMcreator.PropertySet, ) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(proj, attribute_dict, identifier)
    value = attribute_dict[VALUE]
    value_type = attribute_dict[VALUE_TYPE]
    data_type = attribute_dict[DATA_TYPE]

    # compatibility for Datatype import that uses XML-Datatypes such as xs:string
    if data_type in OLD_DATATYPE_DICT:
        data_type = OLD_DATATYPE_DICT[data_type]

    child_inherits_value = attribute_dict[CHILD_INHERITS_VALUE]
    revit_mapping = attribute_dict[REVIT_MAPPING]
    attribute = SOMcreator.Attribute(property_set=property_set, name=name, value=value, value_type=value_type,
                                  data_type=data_type,
                                  child_inherits_values=child_inherits_value, uuid=identifier,
                                  description=description, optional=optional, revit_mapping=revit_mapping,
                                  project=proj, filter_matrix=filter_matrix)
    som_json.parent_dict[attribute] = parent
    SOMcreator.exporter.som_json.attribute_uuid_dict[identifier] = attribute


def write(attribute: SOMcreator.Attribute) -> AttributeDict:
    attribute_dict: AttributeDict = dict()
    core.write_basics(attribute_dict, attribute)
    attribute_dict[DATA_TYPE] = attribute.data_type
    attribute_dict[VALUE_TYPE] = attribute.value_type
    attribute_dict[CHILD_INHERITS_VALUE] = attribute.child_inherits_values
    attribute_dict[REVIT_MAPPING] = attribute.revit_name
    attribute_dict[VALUE] = attribute.get_own_values()
    return attribute_dict
