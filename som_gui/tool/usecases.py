
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.usecases.prop import UsecasesProperties


class Usecases(som_gui.core.tool.Usecases):
    @classmethod
    def get_properties(cls) -> UsecasesProperties:
        return som_gui.UsecasesProperties
