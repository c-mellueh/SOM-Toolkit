from __future__ import annotations
import logging

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
import SOMcreator
import ifcopenshell
from datetime import datetime

GROUP = "Gruppe"
ELEMENT = "Element"

SUBGROUPS = "subgroups"
SUBELEMENT = "subelement"

rev_datatype_dict = {
    str:   "IfcText/IfcLabel",
    bool:  "IfcBoolean",
    int:   "IfcInteger",
    float: "IfcReal"
}


def check_file(file: ifcopenshell.file, modelcheck: Type[tool.Modelcheck],
               modelcheck_window: Type[tool.ModelcheckWindow]):

    modelcheck.connect_to_data_base(modelcheck.get_database_path())
    modelcheck.remove_existing_issues(datetime.today())

    modelcheck.build_data_dict(modelcheck_window.get_item_checkstate_dict())
    modelcheck.build_group_structure(file)

    modelcheck.set_object_checked_count(0)
    modelcheck.set_object_count(modelcheck.get_element_count())
    modelcheck.set_progress(0)
    check_groups(file, modelcheck)
    modelcheck.set_progress(0)

    entities = file.by_type("IfcElement")
    modelcheck.set_object_checked_count(0)
    modelcheck.set_object_count(len(entities))
    check_entities(entities, modelcheck)

    entities_without_group_assignment = modelcheck.get_entities_without_group_assertion(file)
    modelcheck.set_object_checked_count(0)
    modelcheck.set_object_count(len(entities_without_group_assignment))
    modelcheck.disconnect_from_data_base()

    modelcheck.set_status("Prüfung abgeschlossen")
    modelcheck.set_progress(100)


def check_groups(file: ifcopenshell.file, modelcheck: Type[tool.Modelcheck]):
    group_count = modelcheck.get_group_count()
    modelcheck.set_status(f"{group_count} Gruppen werden geprüft")
    root_groups = modelcheck.get_root_groups(file)
    for entity in root_groups:
        if modelcheck.is_aborted():
            return
        check_group(entity, 0, modelcheck)


def check_entities(entities, modelcheck: Type[tool.Modelcheck]):
    modelcheck.set_status(f"{len(entities)} Entitäten werden geprüft")
    for entity in entities:
        modelcheck.increment_checked_items()
        if modelcheck.is_aborted():
            return
        check_element(entity, modelcheck)


def check_group(group_entity: ifcopenshell.entity_instance, layer_index, modelcheck: Type[tool.Modelcheck]):
    modelcheck.increment_checked_items()
    if not modelcheck.entity_should_be_tested(group_entity):
        return

    if group_entity.is_a("IfcElement"):
        modelcheck.set_active_element_type(ELEMENT)
        check_correct_parent(group_entity, modelcheck)
        return
    else:
        modelcheck.set_active_element_type(GROUP)

    is_even_layer = layer_index % 2 == 0
    if is_even_layer:
        check_collector_group(group_entity, modelcheck)
    else:
        check_group_entity(group_entity, modelcheck)

    if not modelcheck.get_sub_entities(group_entity):
        modelcheck.empty_group_issue(group_entity)

    for sub_group in modelcheck.get_sub_entities(group_entity):
        if modelcheck.is_aborted():
            return
        check_group(sub_group, layer_index + 1, modelcheck)


def check_group_entity(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck]):
    check_element(entity, modelcheck)
    check_correct_parent(entity, modelcheck)
    if modelcheck.subelements_have_doubling_identifier(entity):
        modelcheck.repetetive_group_issue(entity)


def check_collector_group(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck]):
    modelcheck.db_create_entity(entity, modelcheck.get_ident_value(entity))
    sub_idents = [modelcheck.get_ident_value(sub_group) for sub_group in modelcheck.get_sub_entities(entity)]
    identifier = modelcheck.get_ident_value(entity)
    for sub_ident in sub_idents:
        if sub_ident != identifier:
            modelcheck.subgroup_issue(sub_ident)


def check_correct_parent(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck]):
    """
    Checks if an Entity or Group has an allowed Parent Group
    """
    object_rep = modelcheck.get_object_representation(entity)
    parent_entity: ifcopenshell.entity_instance = modelcheck.get_parent_entity(modelcheck.get_parent_entity(entity))
    allowed_parents = modelcheck.get_allowed_parents(object_rep)
    if parent_entity is None:
        if None not in allowed_parents:
            logging.warning(f"Group {entity.GlobalId} -> no parent group")
        return

    parent_object_rep = modelcheck.get_object_representation(parent_entity)

    if parent_object_rep is None:
        logging.warning(f"Group {entity.GlobalId} -> no parent obj")
        return

    if not modelcheck.is_parent_allowed(entity, parent_entity):
        modelcheck.parent_issue(entity, parent_entity)


def check_element(element: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck]):
    modelcheck.set_active_element(element)

    data_dict = modelcheck.get_data_dict()
    main_pset_name, main_attribute_name = modelcheck.get_main_pset_name(), modelcheck.get_main_attribute_name()
    main_attribute_value = modelcheck.get_ident_value(element)
    main_attribute_value = "" if main_attribute_value is None else main_attribute_value
    modelcheck.db_create_entity(element, main_attribute_value)

    if not modelcheck.is_pset_existing(element, main_pset_name):
        modelcheck.ident_pset_issue(element.GlobalId, main_pset_name)
        return

    elif not modelcheck.is_attribute_existing(element, main_pset_name, main_attribute_name):
        modelcheck.ident_issue(element.GlobalId, main_pset_name, main_attribute_name)
        return

    obj_rep: SOMcreator.Object = modelcheck.get_ident_dict().get(main_attribute_value)

    if obj_rep is None:
        modelcheck.ident_unknown(element.GlobalId, main_pset_name, main_attribute_name,
                                 main_attribute_value)
        return

    if obj_rep not in data_dict:  # Object Type shouldn't be tested
        return

    if not modelcheck.entity_is_in_group(element) and obj_rep.aggregations:
        modelcheck.no_group_issue(element)

    modelcheck.check_for_attributes(element, obj_rep)
