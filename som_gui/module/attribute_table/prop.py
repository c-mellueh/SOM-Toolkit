from __future__ import annotations
from typing import TypedDict, Callable, TYPE_CHECKING

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
    context_menu_builders = list()  # Functions that are getting called if context menu is requested. Return QAction or None # Each builder gets passed the current table
