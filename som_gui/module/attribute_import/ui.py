from __future__ import annotations
from PySide6.QtWidgets import QWidget, QDialog

from ...icons import get_icon, get_settings_icon

from . import window, settings_window

STANDARD_CHECK_STATE = False
ALL = "Alles"
GROUP = "Gruppe"
ELEMENT = "Element"
TYPE = "Type"
PROPERTYSETS = "PropertySets"


class AttributeImport(QWidget):
    def __init__(self):
        super(AttributeImport, self).__init__()
        self.widget = window.Ui_Form()
        self.widget.setupUi(self)
        self.show()
        self.setWindowTitle("Modellinformationen Einlesen")
        self.setWindowIcon(get_icon())
        self.widget.button_settings.setIcon(get_settings_icon())


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.widget = settings_window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Einstellungen")
