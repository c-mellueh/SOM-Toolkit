from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import (
    IFC_MAPPINGS,
    ABBREVIATION,
    PROPERTY_SETS,
    IDENT_PROPERTY,
    CLASSES,
)
from SOMcreator.exporter.som_json import property_set
import SOMcreator
from SOMcreator.exporter.som_json import core

if TYPE_CHECKING:
    from SOMcreator import SOMProject
    from SOMcreator.datastructure.som_json import ClassDict, MainDict


### Export ###
def _write_class(element: SOMcreator.SOMClass) -> ClassDict:
    class_dict: ClassDict = dict()
    core.write_basics(class_dict, element)

    class_dict[IFC_MAPPINGS] = element.ifc_mapping

    psets_dict = dict()
    for pset in element.get_property_sets(filter=False):
        psets_dict[pset.uuid] = property_set.write_entry(pset)

    class_dict[PROPERTY_SETS] = psets_dict
    class_dict[ABBREVIATION] = element.abbreviation

    if isinstance(element.identifier_property, SOMcreator.SOMProperty):
        class_dict[IDENT_PROPERTY] = element.identifier_property.uuid
    else:
        class_dict[IDENT_PROPERTY] = element.identifier_property

    return class_dict


def write(proj: SOMProject, main_dict: MainDict):
    main_dict[CLASSES] = dict()
    for som_class in sorted(proj.get_classes(filter=False), key=lambda o: o.uuid):
        main_dict[CLASSES][som_class.uuid] = _write_class(som_class)
