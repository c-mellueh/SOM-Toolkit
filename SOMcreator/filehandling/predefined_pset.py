from __future__ import annotations
from SOMcreator.filehandling import core
from SOMcreator.filehandling.constants import PREDEFINED_PSETS
from SOMcreator.filehandling import property_set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator.filehandling.typing import MainDict
    from SOMcreator import Project


def load(project: Project, main_dict: MainDict):
    predef_pset_dict = main_dict.get(PREDEFINED_PSETS)
    core.remove_part_of_dict(PREDEFINED_PSETS)
    predef_pset_dict = dict() if core.check_dict(predef_pset_dict, PREDEFINED_PSETS) else predef_pset_dict

    for uuid_ident, entity_dict in predef_pset_dict.items():
        property_set.load(project, entity_dict, uuid_ident, None)


def write(proj: Project, main_dict: MainDict):
    main_dict[PREDEFINED_PSETS] = dict()
    for predefined_property_set in sorted(proj.get_predefined_psets(), key=lambda x: x.uuid):
        main_dict[PREDEFINED_PSETS][predefined_property_set.uuid] = property_set.write_entry(predefined_property_set)
