from __future__ import annotations
from typing import TYPE_CHECKING
import tempfile
import os
import re
import sqlite3
import time
import SOMcreator
import tqdm
from SOMcreator import Project
from SOMcreator import constants as som_constants
from ifcopenshell.util import element as ifc_el
import ifcopenshell
from . import issues
from .sql import db_create_entity, remove_existing_issues,create_tables
from .output import create_issues
from ..windows.modelcheck_window import ModelcheckWindow

if TYPE_CHECKING:
    from ..main_window import MainWindow
from datetime import datetime
GROUP = "Gruppe"
ELEMENT = "Element"

def run_modelcheck(main_window:MainWindow):
    project = main_window.project
    dialog = ModelcheckWindow(main_window)
    answer = dialog.exec()
    if not answer:
        return
    ifc_paths = dialog.get_ifc_path()
    export_path = dialog.widget.line_edit_export.text()


    if dialog.data_base_path is None:
        db_path = tempfile.NamedTemporaryFile().name
    else:
        db_path = dialog.data_base_path

    property_set = dialog.widget.line_edit_ident_pset.text()
    attribute = dialog.widget.line_edit_ident_attribute.text()

    main(ifc_paths,main_window.project,db_path,property_set,attribute,export_path,project.name)



def check_file(file_path, proj, ag, bk, db_name, p_name):
    file_name, extension = os.path.splitext(file_path)
    if extension.lower() != ".ifc":
        return

    file = os.path.split(file_path)[1]

    ifc = ifcopenshell.open(file_path)
    check_all_elements(proj, ifc, file, db_name, ag, bk, p_name)


def main(file_paths, proj:Project, db_path, ag, bk, issue_path, p_name):
    create_tables(db_path)

    if not isinstance(file_paths, list):
        if not isinstance(file_paths, str):
            return
        if not os.path.isfile(file_paths):
            return
        check_file(file_paths, proj, ag, bk, db_path, p_name)
        return

    for path in file_paths:
        if os.path.isdir(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                check_file(file_path, proj, ag, bk, db_path, p_name)
        else:
            check_file(path, proj, ag, bk, db_path, p_name)

    create_issues(db_path, issue_path)


def check_format(cursor, value, attribute, guid, element_type):
    is_ok = False
    for form in attribute.value:
        if re.match(form, value) is not None:
            is_ok = True
    if not is_ok:
        issues.format_issue(cursor, guid, attribute, element_type)


def check_list(cursor, value, attribute, guid, element_type):
    if not attribute.value:
        return
    if value not in attribute.value:
        issues.list_issue(cursor, guid, attribute, element_type)


def check_range(cursor, value, attribute, guid, element_type):
    is_ok = False
    for possible_range in attribute:
        if min(possible_range) <= value <= max(possible_range):
            is_ok = True
    if not is_ok:
        issues.range_issue(cursor, guid, attribute, element_type)


def check_values(cursor, value, attribute: SOMcreator.Attribute, guid, element_type):
    check_dict = {som_constants.LIST: check_list, som_constants.RANGE: check_range,
                  som_constants.FORMAT: check_format}
    func = check_dict[attribute.value_type]
    func(cursor, value, attribute, guid, element_type)


def check_for_attributes(cursor, element, pset_dict, obj: SOMcreator.Object, element_type):
    guid = element.GlobalId
    for property_set in obj.property_sets:
        pset_name = property_set.name
        if pset_name not in pset_dict:
            issues.property_set_issue(cursor, guid, pset_name, element_type)
            continue

        for attribute in property_set.attributes:
            attribute_name = attribute.name
            if attribute.name not in pset_dict[pset_name]:
                issues.attribute_issue(cursor, guid, pset_name, attribute_name, element_type)
                continue

            value = pset_dict[pset_name][attribute_name]
            check_values(cursor, value, attribute, guid, element_type)


def gruppe_zu_pruefen(cursor, el, ag, bk,create_issue = True):
    """create Issue: Wenn überprüft wird ob die Struktur "Element-Subelement-Element" mit 3x identischen Typ ist soll keine Fehlermeldung ausgegeben werden, weil die Gruppen Rekursiv geprüft werden"""

    bauteilklass = ifc_el.get_pset(el, ag, bk)  #ob.w
    if bauteilklass is None:
        if create_issue:
            issues.ident_issue(cursor, el.GlobalId, bk, ag, GROUP)
        return False

    sub_bks = set()
    for relationship in getattr(el, "HasAssignments", []):
        if not relationship.is_a('IfcRelAssignsToGroup'):
            continue

        parent = relationship.RelatingGroup #is assigned to Group
        parent_bk = ifc_el.get_pset(parent, ag, bk) #ob.w
        if parent_bk != bauteilklass:
            continue

        if gruppe_zu_pruefen(cursor,parent,ag,bk,False):
            return False
        return True

    if not create_issue:
        return False

    for relationship in getattr(el, "IsGroupedBy", []):
        for sub in relationship.RelatedObjects:
            sub_bk = ifc_el.get_pset(sub, ag, bk)
            sub_bks.add(sub_bk)

    if {bauteilklass} != sub_bks:
        issues.subgroup_issue(cursor, el.GlobalId)

    return False


def check_group(group, sub_group, ag, bk, ident_dict):
    bauteilklasse_gruppe = ifc_el.get_pset(group, ag, bk)
    bauteilklasse_sub_gruppe = ifc_el.get_pset(sub_group, ag, bk)

    parent_obj = ident_dict.get(bauteilklasse_gruppe)
    child_obj = ident_dict.get(bauteilklasse_sub_gruppe)

    if child_obj is None:
        return False

    child_aggregations = child_obj.aggregation_representations

    for parent_aggregation in parent_obj.aggregation_representations:
        if parent_aggregation.children.intersection(child_aggregations):
            return True
    return False


def check_element(element, ag, bk, cursor, file_name, ident_dict, element_type, project_name):
    guid = element.GlobalId
    psets = ifc_el.get_psets(element)
    ag_pset = psets.get(ag)
    group_assignment = [assignment for assignment in getattr(element, "HasAssignments", []) if
                        assignment.is_a("IfcRelAssignsToGroup")]
    if not group_assignment:
        issues.no_group_issue(cursor, element)

    if ag_pset is None:
        issues.ident_pset_issue(cursor, guid, ag, element_type)
        db_create_entity(element, cursor, project_name, file_name, "")
        return

    bauteil_klassifikation = ag_pset.get(bk)
    if bauteil_klassifikation is None:
        issues.ident_issue(cursor, guid, ag, bk, element_type)
        db_create_entity(element, cursor, project_name, file_name, "")
        return
    obj_rep = ident_dict.get(bauteil_klassifikation)
    db_create_entity(element, cursor, project_name, file_name, bauteil_klassifikation)
    if obj_rep is None:
        issues.ident_unknown(cursor, guid, ag, bk, element_type, bauteil_klassifikation)
        return

    check_for_attributes(cursor, element, psets, obj_rep, element_type)


def check_all_elements(proj: Project, ifc, file_name, db_name, ag, bk, project_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    remove_existing_issues(cursor, project_name, datetime.today(), file_name)

    ident_dict = {obj.ident_value: obj for obj in proj.objects}
    for element in tqdm.tqdm(ifc.by_type("IfcElement"), desc=f"[{ELEMENT}] {file_name}"):
        check_element(element, ag, bk, cursor, file_name, ident_dict, ELEMENT, project_name)

    for element in tqdm.tqdm(ifc.by_type("IfcGroup"), desc=f"[{GROUP}] {file_name}"):
        relationships = getattr(element, "IsGroupedBy", [])
        if gruppe_zu_pruefen(cursor, element, ag, bk):
            check_element(element, ag, bk, cursor, file_name, ident_dict, GROUP, project_name)
            if not relationships:
                issues.empty_group_issue(cursor, element)

            for relationship in relationships:
                for sub_element in relationship.RelatedObjects:
                    allowed = check_group(element, sub_element, ag, bk, ident_dict)
                    if not allowed:
                        issues.child_issue(cursor, element, sub_element,ag,bk)

    time.sleep(0.1)
    conn.commit()
    conn.close()

