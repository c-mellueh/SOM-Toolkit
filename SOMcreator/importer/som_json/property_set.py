from __future__ import annotations
import SOMcreator
from SOMcreator.importer.som_json import core
from SOMcreator.datastructure.som_json import ATTRIBUTES
from SOMcreator.importer.som_json import attribute
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import PropertySetDict
    from SOMcreator import SOMProject


def load(
    proj: SOMProject,
    pset_dict: PropertySetDict,
    identifier: str,
    obj: SOMcreator.SOMClass | None,
) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, pset_dict, identifier
    )
    pset = SOMcreator.SOMPropertySet(
        name=name,
        obj=obj,
        uuid=identifier,
        description=description,
        optional=optional,
        project=proj,
        filter_matrix=filter_matrix,
    )
    attributes_dict = pset_dict[ATTRIBUTES]
    for ident, attribute_dict in attributes_dict.items():
        attribute.load(proj, attribute_dict, ident, pset)
    SOMcreator.importer.som_json.parent_dict[pset] = parent
    SOMcreator.importer.som_json.property_set_uuid_dict[identifier] = pset
