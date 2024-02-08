from __future__ import annotations
from typing import TYPE_CHECKING
import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set.ui import PredefinedPropertySetWindow

class PredefinedPsetProperties:
    predefined_property_set_window: PredefinedPropertySetWindow = None
    active_predefined_pset: SOMcreator.PropertySet = None
    is_renaming_predefined_pset = False
    is_renaming_property_set = False
