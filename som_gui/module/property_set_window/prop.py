from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set_window.ui import PropertySetWindow


class PropertySetWindowProperties:
    property_set_windows: dict[PropertySetWindow, SOMcreator.PropertySet] = dict()
    active_window: PropertySetWindow = None
    active_attribute: SOMcreator.Attribute = None
