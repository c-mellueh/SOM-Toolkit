
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.class_.prop import ClassProperties


class Class(som_gui.core.tool.Class):
    @classmethod
    def get_properties(cls) -> ClassProperties:
        return som_gui.ClassProperties
