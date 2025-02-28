from __future__ import annotations

import SOMcreator
from SOMcreator.importer.som_json import core
from SOMcreator.datastructure.som_json import (
    AGGREGATIONS,
    AggregationDict,
    CONNECTION,
    OBJECT,
    IDENTITY_TEXT,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator import Project


### Import ###
def _get_aggregation(
    proj: SOMcreator.Project,
    aggregation_dict: AggregationDict,
    identifier: str,
):
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, aggregation_dict, identifier
    )

    object_uuid = aggregation_dict[OBJECT]
    obj = SOMcreator.importer.som_json.object_uuid_dict[object_uuid]
    parent_connection = aggregation_dict[CONNECTION]
    identity_text = aggregation_dict.get(IDENTITY_TEXT)
    aggregation = SOMcreator.SOMAggregation(
        obj=obj,
        parent_connection=parent_connection,
        uuid=identifier,
        description=description,
        optional=optional,
        filter_matrix=filter_matrix,
        identity_text=identity_text,
    )
    SOMcreator.importer.som_json.aggregation_dict[aggregation] = (
        parent,
        parent_connection,
    )


def load(proj: SOMcreator.Project, main_dict: dict):
    aggregations_dict: dict[str, AggregationDict] = main_dict.get(AGGREGATIONS)
    core.remove_part_of_dict(AGGREGATIONS)
    aggregations_dict = (
        dict()
        if core.check_dict(aggregations_dict, AGGREGATIONS)
        else aggregations_dict
    )

    for uuid_ident, entity_dict in aggregations_dict.items():
        _get_aggregation(proj, entity_dict, uuid_ident)


def calculate(proj: SOMcreator.Project):
    uuid_dict = proj.get_uuid_dict()
    for aggregation, (
        uuid,
        connection_type,
    ) in SOMcreator.importer.som_json.aggregation_dict.items():
        parent = uuid_dict.get(uuid)
        if parent is None:
            continue
        parent.add_child(aggregation, connection_type)
