from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import (
    IFC_MAPPINGS,
    ABBREVIATION,
    PROPERTY_SETS,
    IDENT_PROPERTY,
    CLASSES,
)
from SOMcreator.importer.som_json import property_set
import SOMcreator
from SOMcreator.importer.som_json import core
import SOMcreator.importer.som_json

if TYPE_CHECKING:
    from SOMcreator import SOMProject
    from SOMcreator.datastructure.som_json import ClassDict, MainDict


### Import ###


def _load_class(
    proj: SOMcreator.SOMProject, class_dict: ClassDict, identifier: str
) -> SOMcreator.SOMClass:
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, class_dict, identifier
    )
    ifc_mapping = class_dict[IFC_MAPPINGS]
    if isinstance(ifc_mapping, list):
        ifc_mapping = set(ifc_mapping)

    abbreviation = class_dict.get(ABBREVIATION)

    som_class = SOMcreator.SOMClass(
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
    property_sets_dict = class_dict[PROPERTY_SETS]
    for ident, pset_dict in property_sets_dict.items():
        property_set.load(proj, pset_dict, ident, som_class)
    ident_attrib_id = class_dict[IDENT_PROPERTY]
    if ident_attrib_id is not None:
        identifier_property = SOMcreator.importer.som_json.property_uuid_dict.get(
            ident_attrib_id
        )
        som_class.identifier_property = identifier_property
    SOMcreator.importer.som_json.parent_dict[som_class] = parent
    SOMcreator.importer.som_json.class_uuid_dict[identifier] = som_class
    return som_class


def load(proj: SOMProject, main_dict: MainDict):
    classes_dict: dict[str, ClassDict] = main_dict.get(CLASSES)
    core.remove_part_of_dict(CLASSES)

    classes_dict = dict() if core.check_dict(classes_dict, CLASSES) else classes_dict

    for uuid_ident, entity_dict in classes_dict.items():
        _load_class(proj, entity_dict, uuid_ident)
