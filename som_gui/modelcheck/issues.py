from ifcopenshell import entity_instance
from ifcopenshell.util import element as ifc_el

from . import sql

IDENT_PROPERTY_SET_ISSUE = 1
IDENT_ATTRIBUTE_ISSUE = 2
IDENT_ATTRIBUTE_UNKNOWN = 3
GUID_ISSUE = 4
PROPERTY_SET_ISSUE = 5
ATTRIBUTE_EXIST_ISSUE = 6
ATTRIBUTE_VALUE_ISSUES = 7
PARENT_ISSUE = 8
SUBGROUP_ISSUE = 9  # Gruppe besitzt verschiedene Untergruppen
EMPTY_GROUP_ISSUE = 10
NO_GROUP_ISSUE = 11
REPETETIVE_GROUP_ISSUE = 12


def format_issue(cursor, guid, attribute, element_type):
    description = f"{element_type} besitzt nicht das richtige Format für {attribute.property_set.name}:{attribute.name}"
    issue_nr = ATTRIBUTE_VALUE_ISSUES
    sql.add_issues(cursor, guid, description, issue_nr, attribute)


def list_issue(cursor, guid, attribute, element_type):
    description = f"{element_type} besitzt nicht den richtigen Wert für {attribute.property_set.name}:{attribute.name}"
    issue_nr = ATTRIBUTE_VALUE_ISSUES
    sql.add_issues(cursor, guid, description, issue_nr, attribute)


def range_issue(cursor, guid, attribute, element_type):
    description = f"""{element_type}  {attribute.property_set.name}:{attribute.name} 
                  ist nicht in den vorgegebenen Wertebereichen"""
    issue_nr = ATTRIBUTE_VALUE_ISSUES
    sql.add_issues(cursor, guid, description, issue_nr, attribute)


def property_set_issue(cursor, guid, pset_name, element_type):
    description = f"{element_type} besitzt nicht das PropertySet {pset_name}"
    issue_nr = PROPERTY_SET_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None, pset_name=pset_name)


def attribute_issue(cursor, guid, pset_name, attribute_name, element_type):
    description = f"{element_type} besitzt nicht das Attribute {pset_name}:{attribute_name}"
    issue_nr = ATTRIBUTE_EXIST_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None, pset_name=pset_name,
                   attribute_name=attribute_name)


def ident_issue(cursor, guid, pset_name, attribute_name, element_type):
    description = f"{element_type} besitzt nicht das Zuweisungsattribut {pset_name}:{attribute_name}"
    issue_nr = IDENT_ATTRIBUTE_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None, pset_name=pset_name,
                   attribute_name=attribute_name)


def ident_pset_issue(cursor, guid, pset_name, element_type):
    description = f"{element_type}  besitzt nicht das PropertySet {pset_name}"
    issue_nr = IDENT_PROPERTY_SET_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None, pset_name=pset_name)


def ident_unknown(cursor, guid, pset_name, attribute_name, element_type, value):
    description = f"""{element_type} Zuweisungsattribut {pset_name}:{attribute_name}={value} 
                  konnte nicht in SOM gefunden werden"""
    issue_nr = IDENT_ATTRIBUTE_UNKNOWN
    sql.add_issues(cursor, guid, description, issue_nr, None, pset_name=pset_name,
                   attribute_name=attribute_name)


def guid_issue(cursor, guid, file1, file2):
    description = f'GUID kommt in Datei "{file1}" und "{file2}" vor'
    issue_nr = GUID_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None)


# GROUP ISSUES

def subgroup_issue(cursor, guid,child_ident):
    description = f"Gruppensammler besitzt falsche Untergruppe ({child_ident} nicht erlaubt)"
    issue_nr = SUBGROUP_ISSUE
    sql.add_issues(cursor, guid, description, issue_nr, None)


def empty_group_issue(cursor, element):
    description = f"Gruppe besitzt keine Subelemente "
    issue_nr = EMPTY_GROUP_ISSUE
    sql.add_issues(cursor, element.GlobalId, description, issue_nr, None)


def parent_issue(cursor, element:entity_instance, parent_element:entity_instance, ag, bk):
    ident_value = ifc_el.get_pset(parent_element, ag, bk)
    description = f"Gruppe besitzt die falsche Elternklasse ({ident_value} nicht erlaubt)"
    issue_nr = PARENT_ISSUE
    sql.add_issues(cursor, element.GlobalId, description, issue_nr, None)


def no_group_issue(cursor, element):
    description = f"Element hat keine Gruppenzuweisung"
    issue_nr = NO_GROUP_ISSUE
    sql.add_issues(cursor, element.GlobalId, description, issue_nr, None)


def repetetive_group_issue(cursor,element):
    description = f"Gruppe besitzt mehrere Subelemente mit der selben Bauteilklassifikation"
    issue_nr = REPETETIVE_GROUP_ISSUE
    sql.add_issues(cursor, element.GlobalId, description, issue_nr, None)