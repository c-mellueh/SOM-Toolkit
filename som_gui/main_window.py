from __future__ import annotations

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QMainWindow, QTableWidget, QApplication
from PySide6.QtCore import Qt
from SOMcreator import classes

import som_gui
from som_gui import tool
from . import icons, settings
from som_gui.module.main_window.window import Ui_MainWindow
from .windows import (
    mapping_window,
    grouping_window,
)
from .windows.attribute_import.gui import AttributeImport

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from som_gui.core import main_window as core
class MainWindow(QMainWindow):
    def __init__(self, application: QApplication):
        super(MainWindow, self).__init__()
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.GlobalColor.white)
        self.setPalette(palette)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app: QApplication = application

        # variables
        self.active_object: classes.Object | None = None
        self.active_property_set: classes.PropertySet | None = None
        self.project = None

        # Windows
        self.group_window: grouping_window.GroupingWindow | None = None
        self.model_control_window: AttributeImport | None = None
        self.mapping_window = None
        settings.reset_save_path()

        # Icons
        self.setWindowIcon(icons.get_icon())
        self.ui.button_search.setIcon(icons.get_search_icon())

    # Windows

    def open_mapping_window(self):
        self.mapping_window = mapping_window.MappingWindow(self)
        self.mapping_window.show()

    def open_grouping_window(self):
        if self.group_window is None:
            self.group_window = grouping_window.GroupingWindow(self)
        else:
            self.group_window.show()

    def open_attribute_import_window(self):
        if self.model_control_window is not None:
            self.model_control_window.close()
        self.model_control_window = AttributeImport(self)


    @property
    def pset_table(self) -> QTableWidget:
        return self.ui.table_pset

    # Open / Close windows
    def closeEvent(self, event):
        result = core.close_event(tool.Project, tool.Settings, tool.Popups)
        if result:
            self.app.closeAllWindows()
            event.accept()
        else:
            event.ignore()


    def paintEvent(self, event):
        super().paintEvent(event)
        som_gui.core.main_window.refresh_main_window(tool.MainWindow, tool.Project)
