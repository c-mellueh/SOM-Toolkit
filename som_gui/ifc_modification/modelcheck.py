from __future__ import annotations

import re

import SOMcreator
import ifcopenshell
from SOMcreator import value_constants
from ifcopenshell import entity_instance
from ifcopenshell.util import element as ifc_el

from . import issues
from .sql import db_create_entity
from ..data import constants

GROUP = "Gruppe"
ELEMENT = "Element"

SUBGROUPS = "subgroups"
SUBELEMENT = "subelement"

datatype_dict = {
    value_constants.XS_STRING: str,
    value_constants.XS_BOOL: bool,
    value_constants.XS_INT: int,
    value_constants.XS_DOUBLE: float
}

rev_datatype_dict = {
    str: "IfcText/IfcLabel",
    bool: "IfcBoolean",
    int: "IfcInteger",
    float: "IfcReal"
}


def get_identifier(el: entity_instance, main_pset: str, main_attribute: str) -> str | None:
    return ifc_el.get_pset(el, main_pset, main_attribute)


def check_element(element: ifcopenshell.entity_instance, main_pset: str, main_attribute: str, database_path: str,
                  ifc_name: str, ident_dict: dict[str, SOMcreator.Object], element_type: str, project_name: str,
                  data_dict:dict[SOMcreator.Object,dict[SOMcreator.PropertySet,list[SOMcreator.Attribute]]],
                  is_in_group=True):
    def check_values(value, attribute: SOMcreator.Attribute):
        check_dict = {value_constants.LIST: check_list, value_constants.RANGE: check_range,
                      value_constants.FORMAT: check_format, constants.GER_LIST: check_list,
                      constants.GER_VALUE: check_values, constants.GER_FORMAT: check_format,
                      constants.GER_RANGE: check_range}
        func = check_dict[attribute.value_type]
        func(value, attribute)
        check_datatype(value, attribute)

    def check_datatype(value, attribute):
        data_type = datatype_dict[attribute.data_type]
        if not isinstance(value, data_type):
            issues.datatype_issue(database_path, guid, attribute, element_type, rev_datatype_dict[type(value)])

    def check_format(value, attribute):
        is_ok = False
        for form in attribute.value:
            if re.match(form, value) is not None:
                is_ok = True
        if not is_ok:
            issues.format_issue(database_path, guid, attribute, element_type)

    def check_list(value, attribute):
        if not attribute.value:
            return
        if value not in attribute.value:
            issues.list_issue(database_path, guid, attribute, element_type)

    def check_range(value, attribute):
        is_ok = False
        for possible_range in attribute:
            if min(possible_range) <= value <= max(possible_range):
                is_ok = True
        if not is_ok:
            issues.range_issue(database_path, guid, attribute, element_type)

    def check_for_attributes(pset_dict, obj: SOMcreator.Object):
        for property_set in data_dict[obj]:
            pset_name = property_set.name
            if pset_name not in pset_dict:
                issues.property_set_issue(database_path, element.GlobalId, pset_name, element_type)
                continue

            for attribute in data_dict[obj][property_set]:
                attribute_name = attribute.name
                if attribute.name not in pset_dict[pset_name]:
                    issues.attribute_issue(database_path, element.GlobalId, pset_name, attribute_name, element_type)
                    continue

                value = pset_dict[pset_name][attribute_name]
                if value is None:
                    issues.empty_value_issue(database_path,guid,pset_name,attribute.name,element_type)
                else:
                    check_values(value, attribute)

    guid = element.GlobalId
    psets = ifc_el.get_psets(element)
    ag_pset = psets.get(main_pset)
    if ag_pset is None:
        issues.ident_pset_issue(database_path, guid, main_pset, element_type)
        db_create_entity(database_path, element, project_name, ifc_name, "")
        return

    bauteil_klassifikation = ag_pset.get(main_attribute)
    if bauteil_klassifikation is None:
        issues.ident_issue(database_path, guid, main_pset, main_attribute, element_type)
        db_create_entity(database_path, element, project_name, ifc_name, "")
        return
    obj_rep: SOMcreator.Object = ident_dict.get(bauteil_klassifikation)
    db_create_entity(database_path, element, project_name, ifc_name, bauteil_klassifikation)
    if obj_rep is None:
        issues.ident_unknown(database_path, guid, main_pset, main_attribute, element_type, bauteil_klassifikation)
        return
    if obj_rep not in data_dict:
        return
    if not is_in_group:
        if obj_rep.aggregations:
            issues.no_group_issue(database_path, element)
    check_for_attributes(psets, obj_rep)


def iterate_group_structure(focus_group: ifcopenshell.entity_instance, group_dict: dict, ag: str, bk: str,
                            group_parent_dict: dict):


    relationships = getattr(focus_group, "IsGroupedBy", [])
    for relationship in relationships:
        for sub_element in relationship.RelatedObjects:  # IfcGroup or IfcElement
            sub_element: ifcopenshell.entity_instance
            group_parent_dict[sub_element] = focus_group
            group_dict[sub_element] = dict()
            if sub_element.is_a("IfcGroup"):
                iterate_group_structure(sub_element, group_dict[sub_element], ag, bk, group_parent_dict)


def get_parent_group(group: entity_instance) -> list[entity_instance]:
    parent_assignment: list[entity_instance] = [assignment for assignment in getattr(group, "HasAssignments", []) if
                                                assignment.is_a("IfcRelAssignsToGroup")]
    if not parent_assignment:
        return []
    return [assignment.RelatingGroup for assignment in parent_assignment]
