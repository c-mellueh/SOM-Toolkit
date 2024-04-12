from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
from som_gui.module.attribute_import import ui, trigger
from som_gui import tool
from PySide6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from som_gui.module.attribute_import.prop import AttributeImportProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget
class AttributeImport(som_gui.core.tool.AttributeImport):
    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_attribute_widget() is not None

    @classmethod
    def get_attribute_widget(cls) -> ui.AttributeImportWidget:
        return cls.get_properties().attribute_import_widget

    @classmethod
    def get_window(cls):
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls) -> ui.AttributeImportWindow:
        prop = cls.get_properties()
        prop.active_window = ui.AttributeImportWindow()
        return prop.active_window

    @classmethod
    def create_import_widget(cls) -> ui.AttributeImportWidget:
        prop = cls.get_properties()
        prop.attribute_import_widget = ui.AttributeImportWidget()
        return prop.attribute_import_widget

    @classmethod
    def set_ifc_importer_widget(cls, widget: IfcImportWidget):
        cls.get_properties().ifc_import_widget = widget

    @classmethod
    def get_ifc_import_widget(cls):
        return cls.get_properties().ifc_import_widget

    @classmethod
    def get_buttons(cls):
        window = cls.get_attribute_widget()
        ifc_importer = cls.get_ifc_import_widget()

        run_button = ifc_importer.widget.button_run
        abort_button = ifc_importer.widget.button_close

        accept_button = window.widget.button_accept
        close_button = window.widget.button_abort
        return [run_button, abort_button, accept_button, close_button]

    @classmethod
    def connect_buttons(cls, button_list: list[QPushButton]):
        trigger.connect_buttons(*button_list)
