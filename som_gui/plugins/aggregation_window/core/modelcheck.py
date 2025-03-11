from __future__ import annotations

import logging
from typing import Type, TYPE_CHECKING


import ifcopenshell
from PySide6.QtCore import QCoreApplication

import SOMcreator
from som_gui import tool
from som_gui.core.modelcheck import ELEMENT, GROUP
from som_gui.plugins.aggregation_window import tool as aw_tool

if TYPE_CHECKING:
    from som_gui.tool.modelcheck import ModelcheckRunner


def add_modelcheck_plugin(
    modelcheck: Type[tool.Modelcheck], modelcheck_plugin: Type[aw_tool.Modelcheck]
):
    modelcheck.add_file_check_plugin(
        lambda runner: check_file(runner, modelcheck, modelcheck_plugin)
    )
    modelcheck.add_entity_check_plugin(
        lambda e: check_entities(e, modelcheck, modelcheck_plugin)
    )


def check_file(
    runner: ModelcheckRunner,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    file = runner.file
    modelcheck.set_class_checked_count(0)
    modelcheck.set_class_count(len(modelcheck_plugin.get_all_groups(file)))
    modelcheck.set_progress(runner, 0)
    modelcheck_plugin.build_group_structure(file)

    group_count = modelcheck_plugin.get_group_count()
    status = QCoreApplication.translate(
        "Aggregation", "{} Groups will be checked"
    ).format(group_count)
    modelcheck.set_status(runner, status)
    root_groups = modelcheck_plugin.get_root_groups(file)
    for entity in root_groups:
        if modelcheck.is_aborted():
            return
        check_group(runner, entity, 0, modelcheck, modelcheck_plugin)


def check_entities(
    entity,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    main_property_value = modelcheck.get_ident_value(entity)
    main_property_value = "" if main_property_value is None else main_property_value
    obj_rep: SOMcreator.SOMClass = modelcheck.get_ident_dict().get(main_property_value)
    if not modelcheck_plugin.entity_is_in_group(entity) and obj_rep.aggregations:
        modelcheck_plugin.no_group_issue(entity)


def check_group(
    runner: ModelcheckRunner,
    group_entity: ifcopenshell.entity_instance,
    layer_index,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    modelcheck.increment_checked_items(runner)
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
        check_group(runner, sub_group, layer_index + 1, modelcheck, modelcheck_plugin)


def check_group_entity(
    entity: ifcopenshell.entity_instance,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    from som_gui.core.modelcheck import check_element

    check_element(entity, modelcheck)
    check_correct_parent(entity, modelcheck, modelcheck_plugin)
    if modelcheck_plugin.subelements_have_doubling_identifier(entity):
        modelcheck_plugin.repetetive_group_issue(entity)


def check_collector_group(
    entity: ifcopenshell.entity_instance,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    modelcheck.db_create_entity(entity, modelcheck.get_ident_value(entity))
    sub_idents = [
        modelcheck.get_ident_value(sub_group)
        for sub_group in modelcheck_plugin.get_sub_entities(entity)
    ]
    identifier = modelcheck.get_ident_value(entity)
    for sub_ident in sub_idents:
        if sub_ident != identifier:
            modelcheck_plugin.subgroup_issue(sub_ident)


def check_correct_parent(
    entity: ifcopenshell.entity_instance,
    modelcheck: Type[tool.Modelcheck],
    modelcheck_plugin: Type[aw_tool.Modelcheck],
):
    """
    Checks if an Entity or Group has an allowed Parent Group
    """
    class_rep = modelcheck.get_class_representation(entity)
    parent_entity: ifcopenshell.entity_instance = modelcheck_plugin.get_parent_entity(
        modelcheck_plugin.get_parent_entity(entity)
    )
    allowed_parents = modelcheck_plugin.get_allowed_parents(class_rep)
    if parent_entity is None:
        if None not in allowed_parents:
            logging.warning(f"Group {entity.GlobalId} -> no parent group")
        return

    parent_class_rep = modelcheck.get_class_representation(parent_entity)

    if parent_class_rep is None:
        logging.warning(f"Group {entity.GlobalId} -> no parent obj")
        return

    if not modelcheck_plugin.is_parent_allowed(entity, parent_entity):
        modelcheck_plugin.parent_issue(entity, parent_entity)
