from __future__ import annotations
import SOMcreator
from SOMcreator.importer.som_json import core
from SOMcreator.datastructure.som_json import PROPERTIES
from SOMcreator.importer.som_json import property_
from typing import TYPE_CHECKING
import SOMcreator.importer.som_json

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import PropertySetDict
    from SOMcreator import SOMProject


def load(
    proj: SOMProject,
    pset_dict: PropertySetDict,
    identifier: str,
    som_class: SOMcreator.SOMClass | None,
) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, pset_dict, identifier
    )
    pset = SOMcreator.SOMPropertySet(
        name=name,
        som_class=som_class,
        uuid=identifier,
        description=description,
        optional=optional,
        project=proj,
        filter_matrix=filter_matrix,
    )
    properties_dict = pset_dict[PROPERTIES]
    for ident, property_dict in properties_dict.items():
        property_.load(proj, property_dict, ident, pset)
    SOMcreator.importer.som_json.parent_dict[pset] = parent
    SOMcreator.importer.som_json.property_set_uuid_dict[identifier] = pset
