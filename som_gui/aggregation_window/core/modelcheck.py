from __future__ import annotations
from typing import Type
from som_gui import tool
from som_gui.aggregation_window import tool as aw_tool
import ifcopenshell
from som_gui.core.modelcheck import ELEMENT, GROUP
import logging
import SOMcreator


def add_modelcheck_plugin(modelcheck: Type[tool.Modelcheck], modelcheck_plugin: Type[aw_tool.Modelcheck]):
    modelcheck.add_file_check_plugin(lambda file: check_file(file, modelcheck, modelcheck_plugin))
    modelcheck.add_entity_check_plugin(lambda e: check_entities(e, modelcheck, modelcheck_plugin))


def check_file(file: ifcopenshell.file, modelcheck: Type[tool.Modelcheck],
               modelcheck_plugin: Type[aw_tool.Modelcheck]):
    modelcheck.set_object_checked_count(0)
    modelcheck.set_object_count(len(modelcheck_plugin.get_all_groups(file)))
    modelcheck.set_progress(0)
    modelcheck_plugin.build_group_structure(file)

    group_count = modelcheck_plugin.get_group_count()
    modelcheck.set_status(f"{group_count} Gruppen werden geprüft")
    root_groups = modelcheck_plugin.get_root_groups(file)
    for entity in root_groups:
        if modelcheck.is_aborted():
            return
        check_group(entity, 0, modelcheck, modelcheck_plugin)


def check_entities(entity, modelcheck: Type[tool.Modelcheck], modelcheck_plugin: Type[aw_tool.Modelcheck]):
    main_attribute_value = modelcheck.get_ident_value(entity)
    main_attribute_value = "" if main_attribute_value is None else main_attribute_value
    obj_rep: SOMcreator.Object = modelcheck.get_ident_dict().get(main_attribute_value)
    if not modelcheck_plugin.entity_is_in_group(entity) and obj_rep.aggregations:
        modelcheck_plugin.no_group_issue(entity)


def check_group(group_entity: ifcopenshell.entity_instance, layer_index, modelcheck: Type[tool.Modelcheck],
                modelcheck_plugin: Type[aw_tool.Modelcheck]):
    modelcheck.increment_checked_items()
    if not modelcheck.entity_should_be_tested(group_entity):
        return

    if group_entity.is_a("IfcElement"):
        modelcheck.set_active_element_type(ELEMENT)
        check_correct_parent(group_entity, modelcheck, modelcheck_plugin)
        return
    else:
        modelcheck.set_active_element_type(GROUP)

    is_even_layer = layer_index % 2 == 0
    if is_even_layer:
        check_collector_group(group_entity, modelcheck, modelcheck_plugin)
    else:
        check_group_entity(group_entity, modelcheck, modelcheck_plugin)

    sub_groups = modelcheck_plugin.get_sub_entities(group_entity)
    if not sub_groups:
        modelcheck_plugin.empty_group_issue(group_entity)

    for sub_group in sub_groups:
        if modelcheck.is_aborted():
            return
        check_group(sub_group, layer_index + 1, modelcheck, modelcheck_plugin)


def check_group_entity(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck],
                       modelcheck_plugin: Type[aw_tool.Modelcheck]):
    from som_gui.core.modelcheck import check_element
    check_element(entity, modelcheck)
    check_correct_parent(entity, modelcheck, modelcheck_plugin)
    if modelcheck_plugin.subelements_have_doubling_identifier(entity):
        modelcheck_plugin.repetetive_group_issue(entity)


def check_collector_group(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck],
                          modelcheck_plugin: Type[aw_tool.Modelcheck]):
    modelcheck.db_create_entity(entity, modelcheck.get_ident_value(entity))
    sub_idents = [modelcheck.get_ident_value(sub_group) for sub_group in modelcheck_plugin.get_sub_entities(entity)]
    identifier = modelcheck.get_ident_value(entity)
    for sub_ident in sub_idents:
        if sub_ident != identifier:
            modelcheck_plugin.subgroup_issue(sub_ident)


def check_correct_parent(entity: ifcopenshell.entity_instance, modelcheck: Type[tool.Modelcheck],
                         modelcheck_plugin: Type[aw_tool.Modelcheck]):
    """
    Checks if an Entity or Group has an allowed Parent Group
    """
    object_rep = modelcheck.get_object_representation(entity)
    parent_entity: ifcopenshell.entity_instance = modelcheck_plugin.get_parent_entity(
        modelcheck_plugin.get_parent_entity(entity))
    allowed_parents = modelcheck_plugin.get_allowed_parents(object_rep)
    if parent_entity is None:
        if None not in allowed_parents:
            logging.warning(f"Group {entity.GlobalId} -> no parent group")
        return

    parent_object_rep = modelcheck.get_object_representation(parent_entity)

    if parent_object_rep is None:
        logging.warning(f"Group {entity.GlobalId} -> no parent obj")
        return

    if not modelcheck_plugin.is_parent_allowed(entity, parent_entity):
        modelcheck_plugin.parent_issue(entity, parent_entity)
