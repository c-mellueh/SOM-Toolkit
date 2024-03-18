from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from .ui import ModelcheckWindow, ObjectCheckWidget


class ModelcheckProperties:
    active_window: ModelcheckWindow = None
    checkbox_widget: ObjectCheckWidget = None
    check_state_dict: dict[SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute, bool] = None
    selected_object: SOMcreator.Object = None
