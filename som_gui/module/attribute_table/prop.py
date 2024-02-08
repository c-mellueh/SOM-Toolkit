from __future__ import annotations
from typing import TypedDict, Callable, TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import AttributeTable


class ColumnDict(TypedDict):
    display_name: str
    get_function: Callable


class AttributeData(TypedDict):
    getter: Callable
    setter: Callable


class AttributeTableProperties:
    attribute_table_columns: list[ColumnDict] = list()
    attribute_data_dict: dict[str, AttributeData] = list()
    active_attribute: SOMcreator.Attribute = None
    active_table: AttributeTable = None
