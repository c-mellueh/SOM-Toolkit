from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import SOMcreator
from SOMcreator.datastructure.som_json import (
    NAME,
    DESCRIPTION,
    OPTIONAL,
    PARENT,
    FILTER_MATRIX,
)
from SOMcreator.util.misc import check_size_eq
import SOMcreator.datastructure.base

if TYPE_CHECKING:
    from SOMcreator.datastructure.som_json import (
        ClassDict,
        PropertySetDict,
        PropertyDict,
        AggregationDict,
    )


#### Export ######


def write_filter_matrix(element: SOMcreator.datastructure.base.BaseClass):
    print(element)
    proj = element.project
    filter_matrix = element.get_filter_matrix()
    if not check_size_eq(filter_matrix, proj.get_filter_matrix()):
        logging.warning(
            f"Filter List of {element} doesn't match size of project filter list"
        )
    return SOMcreator.exporter.som_json.filter_matrixes.index(
        tuple(tuple(use_case_list) for use_case_list in filter_matrix)
    )


def write_basics(
    entity_dict: ClassDict | PropertySetDict | PropertyDict | AggregationDict,
    element: SOMcreator.datastructure.base.BaseClass,
) -> None:
    """function gets called from all Entities"""
    entity_dict[NAME] = element.name
    entity_dict[OPTIONAL] = element.is_optional(ignore_hirarchy=True)
    entity_dict[FILTER_MATRIX] = write_filter_matrix(element)
    parent = None if element.parent is None else element.parent.uuid
    entity_dict[PARENT] = parent
    entity_dict[DESCRIPTION] = element.description
