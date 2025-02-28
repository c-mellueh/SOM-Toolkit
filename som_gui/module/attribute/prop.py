from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import SOMcreator
    from .ui import AttributeWidget, UnitSettings


class AttributeData(TypedDict):
    getter: Callable
    setter: Callable


class AttributeProperties:
    attribute_data_dict: dict[str, AttributeData] = dict()
    unit_settings_widget: UnitSettings = None


class CompareAttributesProperties:
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    object_dict: dict[SOMcreator.SOMClass, SOMcreator.SOMClass | None] = dict()
    missing_objects: list[list[SOMcreator.SOMClass]] = [None, None]
    object_tree_item_dict = dict()
    object_lists: list[
        tuple[SOMcreator.SOMClass | None, SOMcreator.SOMClass | None]
    ] = list()
    pset_lists: dict[
        SOMcreator.SOMClass, list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]
    ] = dict()
    attributes_lists: dict[
        SOMcreator.PropertySet,
        list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]],
    ] = dict()
    values_lists: dict[SOMcreator.SOMProperty, list[tuple[str, str]]] = dict()
    widget: AttributeWidget = None
