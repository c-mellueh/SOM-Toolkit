from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set.ui import PredefinedPropertySetWindow
    from PySide6.QtGui import QAction


class PredefinedPsetProperties:
    predefined_property_set_window: PredefinedPropertySetWindow = None
    active_predefined_pset: SOMcreator.SOMPropertySet = None
    is_renaming_predefined_pset = False
    actions: dict[str, QAction] = dict()


class PredefinedPsetCompareProperties:
    widget = None
    predefined_psets: tuple[
        set[SOMcreator.SOMPropertySet], set[SOMcreator.SOMPropertySet]
    ] = None
    pset_lists: list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]] = (
        list()
    )
    value_dict = dict()
