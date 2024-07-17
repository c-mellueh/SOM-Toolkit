from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTableWidget
from som_gui.module import attribute_import
from ...icons import get_icon, get_settings_icon

STANDARD_CHECK_STATE = False
ALL = "Alles"
GROUP = "Gruppe"
ELEMENT = "Element"
TYPE = "Type"
PROPERTYSETS = "PropertySets"


class AttributeImportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setWindowTitle(self.tr("Modellinformationen Einlesen"))
        self.setWindowIcon(get_icon())


class AttributeImportWidget(QWidget):
    def __init__(self):
        super(AttributeImportWidget, self).__init__()
        self.widget = attribute_import.window.Ui_Form()
        self.widget.setupUi(self)
        self.widget.button_settings.setIcon(get_settings_icon())
        self.widget.button_accept.hide()
        self.setWindowTitle(self.tr("Modellinformationen Einlesen"))
        self.setWindowIcon(get_icon())

class PropertySetTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_property_set_table()


class AttributeTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_attribute_table()


class ValueTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_value_table()


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.widget = attribute_import.settings_window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Einstellungen")
