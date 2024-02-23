from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import IfcImportWidget
    from ifcopenshell import file as ifc_file


class IfcImportProperties:
    active_importer: IfcImportWidget = None
    imported_model: ifc_file = None
