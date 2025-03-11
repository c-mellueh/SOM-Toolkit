from __future__ import annotations

import SOMcreator
from SOMcreator.exporter.som_json import core
from SOMcreator.datastructure.som_json import (
    CLASS,
    CONNECTION,
    AGGREGATIONS,
    PARENT,
    IDENTITY_TEXT,
    AggregationDict,
    MainDict,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SOMcreator import SOMProject


### Export ###
def _create_entry(element: SOMcreator.SOMAggregation) -> AggregationDict:
    aggregation_dict: AggregationDict = dict()
    core.write_basics(aggregation_dict, element)
    aggregation_dict[CLASS] = element.som_class.uuid
    if element.parent is not None:
        aggregation_dict[PARENT] = element.parent.uuid
    else:
        aggregation_dict[PARENT] = str(element.parent)
    aggregation_dict[CONNECTION] = element.parent_connection
    if element.get_identity_text():
        aggregation_dict[IDENTITY_TEXT] = element.get_identity_text()
    return aggregation_dict


def write(proj: SOMProject, main_dict: MainDict):
    main_dict[AGGREGATIONS] = dict()
    for aggregation in proj.get_aggregations(filter=False):
        main_dict[AGGREGATIONS][aggregation.uuid] = _create_entry(aggregation)
