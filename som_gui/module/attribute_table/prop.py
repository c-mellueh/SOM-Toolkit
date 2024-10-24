from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TypedDict

import SOMcreator

if TYPE_CHECKING:
    from .ui import AttributeTable


class ColumnDict(TypedDict):
    display_name: str
    get_function: Callable


class AttributeTableProperties:
    attribute_table_columns: list[ColumnDict] = list()
    active_attribute: SOMcreator.Attribute = None
    active_table: AttributeTable = None
    context_menu_builders = list()
