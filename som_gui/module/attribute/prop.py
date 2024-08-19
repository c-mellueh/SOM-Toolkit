from __future__ import annotations
from typing import TypedDict, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
    from .ui import AttributeWidget
class AttributeData(TypedDict):
    getter: Callable
    setter: Callable


class AttributeProperties:
    attribute_data_dict: dict[str, AttributeData] = dict()


class CompareAttributesProperties:
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    object_dict: dict[SOMcreator.Object, SOMcreator.Object | None] = dict()
    missing_objects: list[list[SOMcreator.Object]] = [None, None]
    object_tree_item_dict = dict()
    object_lists: list[tuple[SOMcreator.Object | None, SOMcreator.Object | None]] = list()
    pset_lists: dict[SOMcreator.Object, list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]] = dict()
    attributes_lists: dict[SOMcreator.PropertySet, list[tuple[SOMcreator.Attribute, SOMcreator.Attribute]]] = dict()
    values_lists: dict[SOMcreator.Attribute, list[tuple[str, str]]] = dict()
    widget: AttributeWidget = None
