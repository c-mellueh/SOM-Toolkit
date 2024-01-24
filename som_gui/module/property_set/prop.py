from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set.ui import PropertySetWindow, PredefinedPropertySetWindow


class PropertySetProperties:
    active_pset = None
    property_set_windows: dict[PropertySetWindow, SOMcreator.PropertySet] = dict()
    predefined_property_set_window: PredefinedPropertySetWindow = None
    active_predefined_pset = None
    is_renaming_predefined_pset = False
