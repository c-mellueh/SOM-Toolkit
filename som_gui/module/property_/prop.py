from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TypedDict, Union, Sequence

if TYPE_CHECKING:
    import SOMcreator
    from .ui import PropertyWidget
    from som_gui.module.units.ui import UnitSettings

    PP = SOMcreator.SOMClass | SOMcreator.SOMProperty | SOMcreator.SOMPropertySet


class PropertyData(TypedDict):
    getter: Callable
    setter: Callable


class PropertyProperties:
    property_data_dict: dict[str, PropertyData] = dict()
    unit_settings_widget: UnitSettings | None = None


class ComparePropertyProperties:
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    class_dict: dict[SOMcreator.SOMClass, SOMcreator.SOMClass | None] = dict()
    missing_classes: list[list[SOMcreator.SOMClass]] | list[None] = [None, None]
    class_tree_item_dict = dict()
    class_lists: list[tuple[SOMcreator.SOMClass | None, SOMcreator.SOMClass | None]] = (
        list()
    )
    pset_lists: dict[
        SOMcreator.SOMClass,
        list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]],
    ] = dict()
    properties_lists: dict[
        SOMcreator.SOMPropertySet,
        list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]],
    ] = dict()
    values_lists: dict[PP, Sequence[tuple[PP | None, PP | None]]] = dict()
    widget: PropertyWidget | None = None
