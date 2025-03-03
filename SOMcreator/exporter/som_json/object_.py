from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import (
    IFC_MAPPINGS,
    ABBREVIATION,
    PROPERTY_SETS,
    IDENT_ATTRIBUTE,
    OBJECTS,
)
from SOMcreator.exporter.som_json import property_set
import SOMcreator
from SOMcreator.exporter.som_json import core

if TYPE_CHECKING:
    from SOMcreator import SOMProject
    from SOMcreator.datastructure.som_json import ObjectDict, MainDict


### Export ###
def _write_object(element: SOMcreator.SOMClass) -> ObjectDict:
    object_dict: ObjectDict = dict()
    core.write_basics(object_dict, element)

    if isinstance(element.ifc_mapping, set):
        object_dict[IFC_MAPPINGS] = list(element.ifc_mapping)
    else:
        object_dict[IFC_MAPPINGS] = list(element.ifc_mapping)

    psets_dict = dict()
    for pset in element.get_property_sets(filter=False):
        psets_dict[pset.uuid] = property_set.write_entry(pset)

    object_dict[PROPERTY_SETS] = psets_dict
    object_dict[ABBREVIATION] = element.abbreviation

    if isinstance(element.identifier_property, SOMcreator.SOMProperty):
        object_dict[IDENT_ATTRIBUTE] = element.identifier_property.uuid
    else:
        object_dict[IDENT_ATTRIBUTE] = element.identifier_property

    return object_dict


def write(proj: SOMProject, main_dict: MainDict):
    main_dict[OBJECTS] = dict()
    for obj in sorted(proj.get_classes(filter=False), key=lambda o: o.uuid):
        main_dict[OBJECTS][obj.uuid] = _write_object(obj)
