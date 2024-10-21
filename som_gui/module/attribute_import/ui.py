from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTableWidget, QComboBox, QCheckBox
from ...icons import get_icon, get_settings_icon
from . import trigger
from som_gui import __version__ as version
from som_gui import tool

class AttributeImportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setWindowTitle(self.tr(f"Modellinformationen Einlesen | {tool.Util.get_status_text()}"))
        self.setWindowIcon(get_icon())


class AttributeImportResultWindow(QWidget):
    def __init__(self):
        from .qt import ui_Widget
        super(AttributeImportResultWindow, self).__init__()
        self.widget = ui_Widget.Ui_Form()
        self.widget.setupUi(self)
        self.widget.button_settings.setIcon(get_settings_icon())
        self.setWindowTitle(self.tr(f"Modellinformationen Einlesen | {tool.Util.get_status_text()}"))
        self.setWindowIcon(get_icon())


class PropertySetTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("PropertySet"), self.tr("Anzahl")])


class IfcTypeComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        super().paintEvent(e)


class SOMTypeComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AttributeTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("Attribut"), self.tr("Anzahl"), self.tr("Eindeutig")])


class ValueTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("Übernehmen"), self.tr("Wert"), self.tr("Anzahl")])


class ValueCheckBox(QCheckBox):
    def __init__(self, table_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_widget = table_widget
        self.checkStateChanged.connect(lambda: trigger.value_checkstate_changed(self))


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        from .qt import ui_SettingsWidget
        self.widget = ui_SettingsWidget.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(f"Einstellungen v{version}  | {tool.Util.get_status_text()}")
