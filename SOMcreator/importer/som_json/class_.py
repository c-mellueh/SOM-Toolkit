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
from SOMcreator.datastructure.ifc_schema import IFC2X3,IFC4, IFC4_3,class_exists_in_version,predefined_type_exists_in_version,PREDEFINED_SPLITTER

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

    # pre 2.14.1
    if isinstance(ifc_mapping, list):
        ifc_mapping = set(ifc_mapping)

    if not isinstance(ifc_mapping, dict):
        mapping_dict = {IFC2X3:[],IFC4:[],IFC4_3:[]}
        for mapping in ifc_mapping:
            if PREDEFINED_SPLITTER in mapping:
                class_name,predefined_type = mapping.split(PREDEFINED_SPLITTER)
            else:
                class_name,predefined_type = mapping,None
            
            for version in [IFC2X3,IFC4,IFC4_3]:
                if predefined_type is not None:
                    if predefined_type_exists_in_version(class_name,predefined_type,version):
                        mapping_dict[version].append(PREDEFINED_SPLITTER.join(class_name,predefined_type))
                    elif class_exists_in_version(class_name,version):
                        mapping_dict[version].append(class_name)
                else:
                    if class_exists_in_version(class_name,version):
                        mapping_dict[version].append(class_name)
        ifc_mapping = mapping_dict

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
    ident_prop_id = class_dict[IDENT_PROPERTY]
    if ident_prop_id is not None:
        identifier_property = SOMcreator.importer.som_json.property_uuid_dict.get(
            ident_prop_id
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
