from __future__ import annotations
import SOMcreator
from SOMcreator.io.som_json import core
from SOMcreator.io.som_json.constants import ATTRIBUTES
from SOMcreator.io.som_json import attribute
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.io.som_json.typing import PropertySetDict
    from SOMcreator import Project


def load(proj: Project, pset_dict: PropertySetDict, identifier: str, obj: SOMcreator.Object | None) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(proj, pset_dict, identifier)
    pset = SOMcreator.PropertySet(name=name, obj=obj, uuid=identifier, description=description, optional=optional,
                               project=proj, filter_matrix=filter_matrix)
    attributes_dict = pset_dict[ATTRIBUTES]
    for ident, attribute_dict in attributes_dict.items():
        attribute.load(proj, attribute_dict, ident, pset)
    SOMcreator.io.som_json.parent_dict[pset] = parent
    SOMcreator.io.som_json.property_set_uuid_dict[identifier] = pset

#### Export ####

def write_entry(pset: SOMcreator.PropertySet) -> PropertySetDict:
    pset_dict: PropertySetDict = dict()
    core.write_basics(pset_dict, pset)
    attributes_dict = dict()
    for attrib in pset.get_attributes(filter=False):
        new_dict = attribute.write(attrib)
        attributes_dict[attrib.uuid] = new_dict
    pset_dict[ATTRIBUTES] = attributes_dict
    return pset_dict
