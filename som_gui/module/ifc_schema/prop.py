from __future__ import annotations
from .constants import VERSION_TYPE


class IfcSchemaProperties:
    active_versions: set[VERSION_TYPE] = {"IFC4_3"}
