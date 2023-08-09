from __future__ import annotations

import re

import SOMcreator
import ifcopenshell
from SOMcreator import constants as som_constants
from ifcopenshell import entity_instance
from ifcopenshell.util import element as ifc_el

from . import issues
from .sql import db_create_entity


GROUP = "Gruppe"
ELEMENT = "Element"

SUBGROUPS = "subgroups"
SUBELEMENT = "subelement"

def get_identifier(el: entity_instance, main_pset: str, main_attribute: str) -> str | None:
    return ifc_el.get_pset(el, main_pset, main_attribute)


def check_element(element, ag, bk, db_name, file_name, ident_dict, element_type, project_name):
    def check_values(value, attribute: SOMcreator.Attribute):
        check_dict = {som_constants.LIST: check_list, som_constants.RANGE: check_range,
                      som_constants.FORMAT: check_format}
        func = check_dict[attribute.value_type]
        func(value, attribute)

    def check_format(value, attribute):
        is_ok = False
        for form in attribute.value:
            if re.match(form, value) is not None:
                is_ok = True
        if not is_ok:
            issues.format_issue(db_name, guid, attribute, element_type)

    def check_list(value, attribute):
        if not attribute.value:
            return
        if value not in attribute.value:
            issues.list_issue(db_name, guid, attribute, element_type)

    def check_range(value, attribute):
        is_ok = False
        for possible_range in attribute:
            if min(possible_range) <= value <= max(possible_range):
                is_ok = True
        if not is_ok:
            issues.range_issue(db_name, guid, attribute, element_type)

    def check_for_attributes(pset_dict, obj: SOMcreator.Object):
        guid = element.GlobalId
        for property_set in obj.property_sets:
            pset_name = property_set.name
            if pset_name not in pset_dict:
                issues.property_set_issue(db_name, guid, pset_name, element_type)
                continue

            for attribute in property_set.attributes:
                attribute_name = attribute.name
                if attribute.name not in pset_dict[pset_name]:
                    issues.attribute_issue(db_name, guid, pset_name, attribute_name, element_type)
                    continue

                value = pset_dict[pset_name][attribute_name]
                check_values(value, attribute)

    guid = element.GlobalId
    psets = ifc_el.get_psets(element)
    ag_pset = psets.get(ag)
    if ag_pset is None:
        issues.ident_pset_issue(db_name, guid, ag, element_type)
        db_create_entity(db_name, element, project_name, file_name, "")
        return

    bauteil_klassifikation = ag_pset.get(bk)
    if bauteil_klassifikation is None:
        issues.ident_issue(db_name, guid, ag, bk, element_type)
        db_create_entity(db_name, element, project_name, file_name, "")
        return
    obj_rep = ident_dict.get(bauteil_klassifikation)
    db_create_entity(db_name, element, project_name, file_name, bauteil_klassifikation)
    if obj_rep is None:
        issues.ident_unknown(db_name, guid, ag, bk, element_type, bauteil_klassifikation)
        return

    check_for_attributes(psets, obj_rep)


def build_group_structure(focus_group: ifcopenshell.entity_instance, group_dict: dict, ag: str, bk: str, group_parent_dict:dict):

    relationships = getattr(focus_group, "IsGroupedBy", [])
    for relationship in relationships:
        for sub_element in relationship.RelatedObjects:  # IfcGroup or IfcElement
            sub_element: ifcopenshell.entity_instance
            group_parent_dict[sub_element] = focus_group
            group_dict[sub_element] = dict()
            if sub_element.is_a("IfcGroup"):
                build_group_structure(sub_element, group_dict[sub_element], ag, bk,group_parent_dict)


def get_parent_group(group: entity_instance) -> list[entity_instance]:
    parent_assignment: list[entity_instance] = [assignment for assignment in getattr(group, "HasAssignments", []) if
                                                assignment.is_a("IfcRelAssignsToGroup")]
    if not parent_assignment:
        return []
    return [assignment.RelatingGroup for assignment in parent_assignment]
