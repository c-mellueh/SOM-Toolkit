from __future__ import annotations
from typing import TYPE_CHECKING
from .bsdd import export as export_bsdd

if TYPE_CHECKING:
    import SOMcreator


def build_full_data_dict(
    proj: SOMcreator.SOMProject,
) -> dict[
    SOMcreator.SOMClass, dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]]
]:
    d = dict()
    for som_class in proj.get_classes(filter=True):
        d[som_class] = dict()
        for pset in som_class.get_property_sets(filter=True):
            d[som_class][pset] = list()
            for attribute in pset.get_properties(filter=True):
                d[som_class][pset].append(attribute)
    return d
