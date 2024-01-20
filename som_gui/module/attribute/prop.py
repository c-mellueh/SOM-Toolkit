from dataclasses import dataclass, field
from typing import TypedDict, Callable


class ColumnDict(TypedDict):
    display_name: str
    get_function: Callable


@dataclass
class AttributeProperties:
    attribute_table_columns: list[ColumnDict] = field(default_factory=lambda: list())
