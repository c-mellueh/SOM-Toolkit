from __future__ import annotations
from PySide6.QtWidgets import QWidget, QDialog, QTableWidget, QComboBox, QCheckBox
from som_gui.ressources.icons import get_icon, get_settings_icon
from . import trigger
from som_gui import __version__ as version
from som_gui import tool
from PySide6.QtCore import QCoreApplication



class AttributeImportResultWindow(QWidget):
    def __init__(self):
        from .qt import ui_Widget
        super(AttributeImportResultWindow, self).__init__()
        self.ui = ui_Widget.Ui_AttributeImport()
        self.ui.setupUi(self)
        self.ui.button_settings.setIcon(get_settings_icon())
        title = QCoreApplication.translate("AttributeImport", "Import Values")
        self.setWindowTitle(f"{title} | {tool.Util.get_status_text()}")
        self.setWindowIcon(get_icon())


class PropertySetTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("PropertySet"), self.tr("Count")])


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
        self.setHorizontalHeaderLabels([self.tr("Attribute"), self.tr("Count"), self.tr("Unique")])


class ValueTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels([self.tr("Accept"), self.tr("Value"), self.tr("Count")])


class ValueCheckBox(QCheckBox):
    def __init__(self, table_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_widget = table_widget
        self.checkStateChanged.connect(lambda: trigger.value_checkstate_changed(self))


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        from .qt import ui_SettingsWidget
        self.widget = ui_SettingsWidget.Ui_AttributeImport()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        title = QCoreApplication.translate("AttributeImport", "Settings v")
        self.setWindowTitle(f"{title}{version} | {tool.Util.get_status_text()}")
