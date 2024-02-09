from __future__ import annotations
from typing import TypedDict, Callable


class AttributeData(TypedDict):
    getter: Callable
    setter: Callable


class AttributeProperties:
    attribute_data_dict: dict[str, AttributeData] = dict()
