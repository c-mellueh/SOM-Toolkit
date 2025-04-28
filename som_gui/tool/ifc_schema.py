
from __future__ import annotations
from typing import TYPE_CHECKING
import logging

import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.ifc_schema.prop import IfcSchemaProperties


class IfcSchema(som_gui.core.tool.IfcSchema):
    @classmethod
    def get_properties(cls) -> IfcSchemaProperties:
        return som_gui.IfcSchemaProperties
