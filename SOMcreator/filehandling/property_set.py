from __future__ import annotations
import SOMcreator
from SOMcreator import classes
from SOMcreator.filehandling import core
from SOMcreator.filehandling.constants import PREDEFINED_PSETS, ATTRIBUTES
from SOMcreator.filehandling import attribute
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.filehandling.typing import PropertySetDict, MainDict
    from SOMcreator import Project


def load(proj: Project, pset_dict: PropertySetDict, identifier: str, obj: classes.Object | None) -> None:
    name, description, optional, parent, filter_matrix = core.get_basics(proj, pset_dict)
    pset = classes.PropertySet(name=name, obj=obj, uuid=identifier, description=description, optional=optional,
                               project=proj, filter_matrix=filter_matrix)
    attributes_dict = pset_dict[ATTRIBUTES]
    for ident, attribute_dict in attributes_dict.items():
        attribute.load(proj, attribute_dict, ident, pset)
    SOMcreator.filehandling.parent_dict[pset] = parent
    SOMcreator.filehandling.property_set_uuid_dict[identifier] = pset

#### Export ####

def write_entry(pset: classes.PropertySet) -> PropertySetDict:
    pset_dict: PropertySetDict = dict()
    core.write_basics(pset_dict, pset)
    attributes_dict = dict()
    for attrib in pset.get_all_attributes():
        new_dict = attribute.write(attrib)
        attributes_dict[attrib.uuid] = new_dict
    pset_dict[ATTRIBUTES] = attributes_dict
    return pset_dict
