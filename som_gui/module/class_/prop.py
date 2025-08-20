from __future__ import annotations
from typing import TypedDict


class ClassDataDict(TypedDict):
    name: str
    is_group: bool
    abbreviation: str
    ident_pset_name: str
    ident_property_name: str
    ident_value: str
    ifc_mappings: list[str]
    parent_uuid: str


class ClassProperties:
    class_add_checks = list()
