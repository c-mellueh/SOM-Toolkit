from dataclasses import dataclass, field
from typing import TypedDict, Callable

import SOMcreator


class ColumnDict(TypedDict):
    display_name: str
    get_function: Callable


class AttributeData(TypedDict):
    getter: Callable
    setter: Callable




@dataclass
class AttributeProperties:
    attribute_table_columns: list[ColumnDict] = field(default_factory=lambda: list())
    attribute_data_dict: dict[str, AttributeData] = field(default_factory=lambda: dict())
    active_attribute: SOMcreator.Attribute = None
