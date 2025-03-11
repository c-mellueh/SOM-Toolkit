from __future__ import annotations
import logging
import SOMcreator
import SOMcreator.importer.som_json
from SOMcreator.importer.som_json import core
from SOMcreator.datastructure.som_json import (
    AGGREGATIONS,
    AggregationDict,
    CONNECTION,
    CLASS,
    IDENTITY_TEXT,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator import SOMProject
    from SOMcreator.datastructure.som_json import MainDict


### Import ###
def _get_aggregation(
    proj: SOMcreator.SOMProject,
    aggregation_dict: AggregationDict,
    identifier: str,
):
    name, description, optional, parent, filter_matrix = core.get_basics(
        proj, aggregation_dict, identifier
    )

    class_uuid: str = aggregation_dict[CLASS]
    som_class = SOMcreator.importer.som_json.class_uuid_dict[class_uuid]
    parent_connection = aggregation_dict[CONNECTION]
    identity_text = aggregation_dict.get(IDENTITY_TEXT)
    aggregation = SOMcreator.SOMAggregation(
        som_class=som_class,
        parent_connection=parent_connection,
        uuid=identifier,
        description=description,
        optional=optional,
        filter_matrix=filter_matrix,
        identity_text=identity_text,
    )
    proj.add_item(aggregation, overwrite_filter_matrix=False)
    SOMcreator.importer.som_json.aggregation_dict[aggregation] = (
        parent,
        parent_connection,
    )


def load(proj: SOMcreator.SOMProject, main_dict: MainDict):
    aggregations_dict: dict[str, AggregationDict] = main_dict.get(AGGREGATIONS)
    core.remove_part_of_dict(AGGREGATIONS)
    aggregations_dict = (
        dict()
        if core.check_dict(aggregations_dict, AGGREGATIONS)
        else aggregations_dict
    )

    for uuid_ident, entity_dict in aggregations_dict.items():
        _get_aggregation(proj, entity_dict, uuid_ident)


def calculate(proj: SOMcreator.SOMProject):
    uuid_dict = proj.get_uuid_dict()
    for aggregation, (
        uuid,
        connection_type,
    ) in SOMcreator.importer.som_json.aggregation_dict.items():
        if uuid is None:
            continue
        parent = uuid_dict.get(uuid)
        if parent is None or not isinstance(parent, SOMcreator.SOMAggregation):
            logging.warning(
                f"Aggregation '{aggregation.name}'parent with uuid '{uuid}' not found"
            )
            continue
        parent.add_child(aggregation, connection_type)
