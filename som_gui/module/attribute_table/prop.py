from __future__ import annotations
from typing import Callable, TYPE_CHECKING, TypedDict
import SOMcreator

class AttributeTableProperties:
    attribute_table_columns: list[tuple[str,Callable]] = list() #list of columns list[Tuple[name,Getter]]
    context_menu_builders:list[Callable] = list()
