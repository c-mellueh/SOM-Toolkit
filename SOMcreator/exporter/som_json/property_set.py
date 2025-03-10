from __future__ import annotations
import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.datastructure.som_json import PROPERTIES
from SOMcreator.exporter.som_json import property_
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import PropertySetDict


#### Export ####


def write_entry(pset: SOMcreator.SOMPropertySet) -> PropertySetDict:
    pset_dict: PropertySetDict = dict()
    core.write_basics(pset_dict, pset)
    property_dict = dict()
    for som_property in pset.get_properties(filter=False):
        new_dict = property_.write(som_property)
        property_dict[som_property.uuid] = new_dict
    pset_dict[PROPERTIES] = property_dict
    return pset_dict
