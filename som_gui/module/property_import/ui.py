from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QTableWidget, QWidget

from som_gui.resources.icons import get_icon, get_settings_icon
from . import trigger


class PropertyImportResultWindow(QWidget):
    def __init__(self):
        from .qt import ui_Widget

        super(PropertyImportResultWindow, self).__init__()
        self.ui = ui_Widget.Ui_PropertyImport()
        self.ui.setupUi(self)
        self.ui.button_settings.setIcon(get_settings_icon())
        self.setWindowIcon(get_icon())

    def closeEvent(self, event):
        trigger.window_closed()
        return super().closeEvent(event)

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


class PropertyTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels(
            [self.tr("Property"), self.tr("Count"), self.tr("Unique")]
        )


class ValueTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear()
        self.setColumnCount(3)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels(
            [self.tr("Accept"), self.tr("Value"), self.tr("Count")]
        )


class ValueCheckBox(QCheckBox):
    def __init__(self, table_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_widget = table_widget
        self.checkStateChanged.connect(lambda: trigger.value_checkstate_changed(self))


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        from .qt import ui_SettingsWidget

        self.widget = ui_SettingsWidget.Ui_SettingsDialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
