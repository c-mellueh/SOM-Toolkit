from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import (
    IFC_MAPPINGS,
    ABBREVIATION,
    PROPERTY_SETS,
    IDENT_ATTRIBUTE,
    OBJECTS,
)
from SOMcreator.importer.som_json import property_set
import SOMcreator
from SOMcreator.importer.som_json import core

if TYPE_CHECKING:
    from SOMcreator import SOMProject
    from SOMcreator.datastructure.som_json import ObjectDict, MainDict


### Import ###


def _load_object(
    proj: SOMcreator.SOMProject, object_dict: ObjectDict, identifier: str
) -> SOMcreator.SOMClass:
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, object_dict, identifier
    )
    ifc_mapping = object_dict[IFC_MAPPINGS]
    if isinstance(ifc_mapping, list):
        ifc_mapping = set(ifc_mapping)

    abbreviation = object_dict.get(ABBREVIATION)

    obj = SOMcreator.SOMClass(
        name=name,
        identifier_property=None,
        uuid=identifier,
        ifc_mapping=ifc_mapping,
        description=description,
        optional=optional,
        abbreviation=abbreviation,
        project=proj,
        filter_matrix=filter_matrix,
    )
    property_sets_dict = object_dict[PROPERTY_SETS]
    for ident, pset_dict in property_sets_dict.items():
        property_set.load(proj, pset_dict, ident, obj)
    ident_attrib_id = object_dict[IDENT_ATTRIBUTE]
    if ident_attrib_id is not None:
        ident_attrib = SOMcreator.importer.som_json.attribute_uuid_dict.get(
            ident_attrib_id
        )
        obj.identifier_property = ident_attrib
    SOMcreator.importer.som_json.parent_dict[obj] = parent
    SOMcreator.importer.som_json.object_uuid_dict[identifier] = obj


def load(proj: SOMProject, main_dict: dict):
    objects_dict: dict[str, ObjectDict] = main_dict.get(OBJECTS)
    core.remove_part_of_dict(OBJECTS)

    objects_dict = dict() if core.check_dict(objects_dict, OBJECTS) else objects_dict

    for uuid_ident, entity_dict in objects_dict.items():
        _load_object(proj, entity_dict, uuid_ident)
