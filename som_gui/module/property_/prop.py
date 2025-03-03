from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TypedDict,Union,Sequence

if TYPE_CHECKING:
    import SOMcreator
    from .ui import PropertyWidget, UnitSettings

    PP = SOMcreator.SOMClass|SOMcreator.SOMProperty| SOMcreator.SOMPropertySet
class PropertyData(TypedDict):
    getter: Callable
    setter: Callable


class PropertyProperties:
    attribute_data_dict: dict[str, PropertyData] = dict()
    unit_settings_widget: UnitSettings|None = None


class ComparePropertyProperties:
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    object_dict: dict[SOMcreator.SOMClass, SOMcreator.SOMClass | None] = dict()
    missing_objects: list[list[SOMcreator.SOMClass]]|list[None] = [None, None]
    object_tree_item_dict = dict()
    object_lists: list[
        tuple[SOMcreator.SOMClass | None, SOMcreator.SOMClass | None]
    ] = list()
    pset_lists: dict[
        SOMcreator.SOMClass,
        list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]],
    ] = dict()
    properties_lists: dict[
        SOMcreator.SOMPropertySet,
        list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]],
    ] = dict()
    values_lists: dict[PP, Sequence[tuple[PP|None, PP|None]]] = dict()
    widget: PropertyWidget|None = None

