from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set.ui import PredefinedPropertySetWindow
    from PySide6.QtGui import QAction


class PredefinedPsetProperties:
    predefined_property_set_window: PredefinedPropertySetWindow = None
    active_predefined_pset: SOMcreator.PropertySet = None
    is_renaming_predefined_pset = False
    actions: dict[str, QAction] = dict()


class PredefinedPsetCompareProperties:
    widget = None
    predefined_psets: tuple[set[SOMcreator.PropertySet], set[SOMcreator.PropertySet]] = None
    pset_lists: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]] = list()
    value_dict = dict()
