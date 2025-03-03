from __future__ import annotations
import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.datastructure.som_json import ATTRIBUTES
from SOMcreator.exporter.som_json import attribute
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import PropertySetDict


#### Export ####


def write_entry(pset: SOMcreator.SOMPropertySet) -> PropertySetDict:
    pset_dict: PropertySetDict = dict()
    core.write_basics(pset_dict, pset)
    attributes_dict = dict()
    for attrib in pset.get_properties(filter=False):
        new_dict = attribute.write(attrib)
        attributes_dict[attrib.uuid] = new_dict
    pset_dict[ATTRIBUTES] = attributes_dict
    return pset_dict
