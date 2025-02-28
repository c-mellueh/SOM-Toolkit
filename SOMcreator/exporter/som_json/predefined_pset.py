from __future__ import annotations
from SOMcreator.datastructure.som_json import PREDEFINED_PSETS
from SOMcreator.exporter.som_json import property_set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import MainDict
    from SOMcreator import SOMProject


def write(proj: SOMProject, main_dict: MainDict):
    main_dict[PREDEFINED_PSETS] = dict()
    for predefined_property_set in sorted(
        proj.get_predefined_psets(filter=False), key=lambda x: x.uuid
    ):
        main_dict[PREDEFINED_PSETS][predefined_property_set.uuid] = (
            property_set.write_entry(predefined_property_set)
        )
