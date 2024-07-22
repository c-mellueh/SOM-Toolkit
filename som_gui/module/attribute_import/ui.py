from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTableWidget, QComboBox, QCheckBox
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


class AttributeImportResultWindow(QWidget):
    def __init__(self):
        super(AttributeImportResultWindow, self).__init__()
        self.widget = attribute_import.window.Ui_Form()
        self.widget.setupUi(self)
        self.widget.button_settings.setIcon(get_settings_icon())
        self.setWindowTitle(self.tr("Modellinformationen Einlesen"))
        self.setWindowIcon(get_icon())

class PropertySetTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("PropertySet"), self.tr("Anzahl")])

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_property_set_table()

class IfcTypeComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.ifctype_combobox_paint_event()


class SOMTypeComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.somtype_combobox_paint_event()
class AttributeTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("Attribut"), self.tr("Anzahl"), self.tr("Eindeutig")])

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_attribute_table()


class ValueTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("Übernehmen"), self.tr("Wert"), self.tr("Anzahl")])

    def paintEvent(self, e):
        super().paintEvent(e)
        attribute_import.trigger.paint_value_table()


class ValueCheckBox(QCheckBox):
    def __init__(self, table_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_widget = table_widget
        self.checkStateChanged.connect(lambda: attribute_import.trigger.value_checkstate_changed(self))
class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.widget = attribute_import.settings_window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Einstellungen")
