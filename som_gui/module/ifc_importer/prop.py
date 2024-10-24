from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ifcopenshell import file as ifc_file
    from PySide6.QtCore import QRunnable, QThreadPool


class IfcImportProperties:
    imported_model: ifc_file = None
    runner: QRunnable = None
    thread_pool: QThreadPool = None
