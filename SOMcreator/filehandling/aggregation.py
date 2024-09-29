from __future__ import annotations

import logging
import time
from os import remove

import SOMcreator
from SOMcreator import classes
from SOMcreator.filehandling import core
from SOMcreator.filehandling.constants import OBJECT, CONNECTION, AGGREGATIONS, PARENT
from SOMcreator.filehandling.typing import AggregationDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator import Project
    from SOMcreator.filehandling.typing import MainDict


### Import ###
def _get_aggregation(proj: SOMcreator.Project, aggregation_dict: AggregationDict, identifier: str, ):
    name, description, optional, parent, filter_matrix = core.get_basics(proj, aggregation_dict, identifier)

    object_uuid = aggregation_dict[OBJECT]
    obj = SOMcreator.filehandling.object_uuid_dict[object_uuid]
    parent_connection = aggregation_dict[CONNECTION]
    aggregation = classes.Aggregation(obj=obj, parent_connection=parent_connection, uuid=identifier,
                                      description=description, optional=optional, filter_matrix=filter_matrix)
    SOMcreator.filehandling.aggregation_dict[aggregation] = (parent, parent_connection)


def load(proj: classes.Project, main_dict: dict):
    aggregations_dict: dict[str, AggregationDict] = main_dict.get(AGGREGATIONS)
    core.remove_part_of_dict(AGGREGATIONS)
    aggregations_dict = dict() if core.check_dict(aggregations_dict, AGGREGATIONS) else aggregations_dict

    for uuid_ident, entity_dict in aggregations_dict.items():
        _get_aggregation(proj, entity_dict, uuid_ident)


def calculate(proj: SOMcreator.Project):
    uuid_dict = proj.get_uuid_dict()
    for aggregation, (uuid, connection_type) in SOMcreator.filehandling.aggregation_dict.items():
        parent = uuid_dict.get(uuid)
        if parent is None:
            continue
        parent.add_child(aggregation, connection_type)


### Export ###
def _create_entry(element: classes.Aggregation) -> AggregationDict:
    aggregation_dict: AggregationDict = dict()
    core.write_basics(aggregation_dict, element)
    aggregation_dict[OBJECT] = element.object.uuid
    if element.parent is not None:
        aggregation_dict[PARENT] = element.parent.uuid
    else:
        aggregation_dict[PARENT] = str(element.parent)
    aggregation_dict[CONNECTION] = element.parent_connection
    return aggregation_dict


def write(proj: Project, main_dict: MainDict):
    main_dict[AGGREGATIONS] = dict()
    for aggregation in proj.get_all_aggregations():
        main_dict[AGGREGATIONS][aggregation.uuid] = _create_entry(aggregation)
