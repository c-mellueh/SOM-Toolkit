from __future__ import annotations
from .constants import VERSION_TYPE
class IfcSchemaProperties:
    active_versions:set[VERSION_TYPE] = set()
    parent_dict:dict[str,dict[str,list[str]]] = dict()
    pset_class_dict:dict[str,dict[str,list[str]]] = dict()
