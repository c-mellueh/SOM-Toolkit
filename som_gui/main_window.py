from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QTableWidget, QLabel, QApplication
from SOMcreator import classes

import som_gui
from som_gui import tool
from som_gui.windows.aggregation_view import aggregation_window
from . import icons, settings, __version__
from .filehandling import save_file, export
from .qt_designs.ui_mainwindow import Ui_MainWindow
from .windows import (
    predefined_psets_window,
    mapping_window,
    popups,
    grouping_window,
)
from .module.project import ui
from .windows.project_phases import gui as project_phase_window
from .windows.modelcheck import modelcheck_window
from .windows.attribute_import.gui import AttributeImport

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.objects.ui import ObjectTreeWidget

from som_gui.core import main_window as core
class MainWindow(QMainWindow):
    def __init__(self, application: QApplication):

        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app: QApplication = application
        som_gui.MainUi.ui = self.ui
        som_gui.MainUi.window = self
        core.set_main_window(self.ui, tool.MainWindow)

        # variables
        self.active_object: classes.Object | None = None
        self.active_property_set: classes.PropertySet | None = None
        self.project = None
        self.permanent_status_text = QLabel()

        # Windows
        self.group_window: grouping_window.GroupingWindow | None = None
        self.model_control_window: AttributeImport | None = None
        self.project_phase_window: project_phase_window.ProjectPhaseWindow | None = None
        self.graph_window = aggregation_window.AggregationWindow(self)
        self.mapping_window = None
        self.modelcheck_window: modelcheck_window.ModelcheckWindow | None = None
        self.search_ui: popups.SearchWindow | None = None
        self.predefined_pset_window: predefined_psets_window.PropertySetInherWindow | None = (
            None
        )
        settings.reset_save_path()
        self.ui.statusbar.addWidget(self.permanent_status_text)
        self.generate_window_title()

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
        if self.model_control_window is None:
            self.model_control_window = AttributeImport(self)
        else:
            self.model_control_window.show()

    def open_predefined_pset_window(self):
        if self.predefined_pset_window is None:
            self.predefined_pset_window = (
                predefined_psets_window.PropertySetInherWindow(self)
            )
        self.predefined_pset_window.show()

    def open_aggregation_window(self):
        self.graph_window.show()

    @property
    def object_tree(self) -> ObjectTreeWidget:
        return tool.Object.get_object_tree()

    @property
    def pset_table(self) -> QTableWidget:
        return self.ui.table_pset

    # Open / Close windows
    def closeEvent(self, event):
        action = save_file.close_event(self)

        if action:
            self.app.closeAllWindows()
            event.accept()
        else:
            event.ignore()

    # Main
    def clear_all(self):
        self.project.clear()

    def reload(self):
        predefined_psets_window.reload(self)
        self.generate_window_title()

    def generate_window_title(self) -> str:
        text = f"SOM-Toolkit v{__version__}"
        self.setWindowTitle(text)
        if self.project:
            self.permanent_status_text.setText(
                f"{self.project.name} v{self.project.version}"
            )
        return text
