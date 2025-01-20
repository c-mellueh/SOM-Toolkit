from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TypedDict

import SOMcreator

if TYPE_CHECKING:
    from .ui import AttributeTable


class ColumnDict(TypedDict):
    display_name: str
    get_function: Callable


class AttributeTableProperties:
    attribute_table_columns: list[tuple[str,Callable]] = list() #list of columns list[Tuple[name,Getter]]
    active_table: AttributeTable = None
    context_menu_builders = list()
