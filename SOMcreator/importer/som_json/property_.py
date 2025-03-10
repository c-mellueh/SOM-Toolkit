from __future__ import annotations
import SOMcreator
from SOMcreator.importer.som_json import core
from SOMcreator.constants.value_constants import OLD_DATATYPE_DICT
from SOMcreator.importer import som_json
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import (
    CHILD_INHERITS_VALUE,
    DATA_TYPE,
    REVIT_MAPPING,
    VALUE,
    VALUE_TYPE,
    PropertyDict,
)


def load(
    proj: SOMcreator.SOMProject,
    property_dict: PropertyDict,
    identifier: str,
    property_set: SOMcreator.SOMPropertySet,
) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, property_dict, identifier
    )
    value = property_dict[VALUE]
    value_type = property_dict[VALUE_TYPE]
    data_type = property_dict[DATA_TYPE]

    # compatibility for Datatype import that uses XML-Datatypes such as xs:string
    if data_type in OLD_DATATYPE_DICT:
        data_type = OLD_DATATYPE_DICT[data_type]

    child_inherits_value = property_dict[CHILD_INHERITS_VALUE]
    revit_mapping = property_dict[REVIT_MAPPING]
    som_property = SOMcreator.SOMProperty(
        property_set=property_set,
        name=name,
        allowed_values=value,
        value_type=value_type,
        data_type=data_type,
        child_inherits_values=child_inherits_value,
        uuid=identifier,
        description=description,
        optional=optional,
        revit_mapping=revit_mapping,
        project=proj,
        filter_matrix=filter_matrix,
    )
    som_json.parent_dict[som_property] = parent
    som_json.property_uuid_dict[identifier] = som_property
