from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.property_set_window.ui import (
        PropertySetWindow,
        SplitterSettings,
        UnitSettings,
    )


class PropertySetWindowProperties:
    property_set_windows: dict[PropertySetWindow, SOMcreator.SOMPropertySet] = dict()
    active_window: PropertySetWindow = None
    active_property: SOMcreator.SOMProperty = None
    splitter_settings: SplitterSettings = None
    unit_settings: UnitSettings = None
    context_menu_builders = list()