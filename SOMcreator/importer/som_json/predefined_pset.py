from __future__ import annotations
from SOMcreator.importer.som_json import core
from SOMcreator.datastructure.som_json import PREDEFINED_PSETS
from SOMcreator.importer.som_json import property_set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import MainDict
    from SOMcreator import SOMProject


def load(project: SOMProject, main_dict: MainDict):
    predef_pset_dict = main_dict.get(PREDEFINED_PSETS)
    core.remove_part_of_dict(PREDEFINED_PSETS)
    predef_pset_dict = (
        dict()
        if core.check_dict(predef_pset_dict, PREDEFINED_PSETS)
        else predef_pset_dict
    )

    for uuid_ident, entity_dict in predef_pset_dict.items():
        property_set.load(project, entity_dict, uuid_ident, None)
