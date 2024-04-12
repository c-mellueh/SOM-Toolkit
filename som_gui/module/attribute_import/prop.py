from typing import TYPE_CHECKING

from .ui import AttributeImportWindow, AttributeImportWidget, SettingsDialog
from som_gui.module.ifc_importer.ui import IfcImportWidget


class AttributeImportProperties:
    active_window: AttributeImportWindow = None
    attribute_import_widget: AttributeImportWidget = None
    ifc_import_widget: IfcImportWidget = None
    settings_dialog: SettingsDialog = None
    main_pset: str = "Undefined"
    main_attribute: str = "Undefined"
    import_is_aborted = False
    ifc_import_runners = []
    runner = None
    thread_pool = None
