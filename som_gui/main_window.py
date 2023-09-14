from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QTableWidget, QLabel
from SOMcreator import classes

from som_gui.windows.aggregation_view import aggregation_window
from . import icons
from . import settings, __version__
from .filehandling import open_file, save_file, export
from .qt_designs.ui_mainwindow import Ui_MainWindow
from .widgets import property_widget, object_widget
from .windows import predefined_psets_window, propertyset_window, mapping_window, popups, modelcheck_window, \
    grouping_window, attribute_import_window, settings_window, project_phase_window


class MainWindow(QMainWindow):
    def __init__(self, application, open_file_path: str | None):
        def connect_actions():
            # connect Menubar signals

            self.ui.action_file_Open.triggered.connect(lambda: open_file.open_file_clicked(self))
            self.ui.action_file_new.triggered.connect(lambda: popups.new_file_clicked(self))
            self.ui.action_file_Save.triggered.connect(lambda: save_file.save_clicked(self))
            self.ui.action_file_Save_As.triggered.connect(lambda: save_file.save_as_clicked(self))
            # Export

            self.ui.action_export_bs.triggered.connect(lambda: export.export_building_structure(self))
            self.ui.action_export_bookmarks.triggered.connect(lambda: export.export_bookmarks(self))
            self.ui.action_export_boq.triggered.connect(lambda: export.export_bill_of_quantities(self))
            self.ui.action_vestra.triggered.connect(lambda: export.export_vestra_mapping(self))
            self.ui.action_card1.triggered.connect(lambda: export.export_card_1(self))
            self.ui.action_excel.triggered.connect(lambda: export.export_excel(self))
            self.ui.action_mapping_script.triggered.connect(lambda: export.export_mapping_script(self))
            self.ui.action_allplan.triggered.connect(lambda: export.export_allplan_excel(self))
            self.ui.action_abbreviation_json.triggered.connect(lambda: export.export_desite_abbreviation(self))
            self.ui.action_desite_export.triggered.connect(lambda: export.export_desite_rules(self))
            # Windows

            self.ui.action_show_list.triggered.connect(self.open_predefined_pset_window)
            self.ui.action_settings.triggered.connect(self.open_settings_window)
            self.ui.action_modelcheck.triggered.connect(self.open_modelcheck_window)
            self.ui.action_create_groups.triggered.connect(self.open_grouping_window)
            self.ui.action_model_control.triggered.connect(self.open_attribute_import_window)
            self.ui.action_project_phase.triggered.connect(self.open_project_phase_window)
            self.ui.action_show_graphs.triggered.connect(self.open_aggregation_window)
            self.ui.action_mapping.triggered.connect(self.open_mapping_window)

        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app = application

        # variables
        self.active_object: classes.Object | None = None
        self.active_property_set: classes.PropertySet | None = None
        self.project = classes.Project("Project", "")
        self.permanent_status_text = QLabel()

        # Windows
        self.group_window: grouping_window.GroupingWindow | None = None
        self.model_control_window: attribute_import_window.AttributeImport | None = None
        self.project_phase_window: project_phase_window.ProjectPhaseWindow | None = None
        self.graph_window = aggregation_window.AggregationWindow(self)
        self.mapping_window = None
        self.modelcheck_window: modelcheck_window.ModelcheckWindow | None = None
        self.search_ui: popups.ObjectSearchWindow | popups.AttributeSearchWindow | None = None
        self.object_info_widget: object_widget.ObjectInfoWidget | None = None
        self.predefined_pset_window: predefined_psets_window.PropertySetInherWindow | None = None
        self.property_set_window: None | propertyset_window.PropertySetWindow = None

        # init Object- and PropertyWidget
        object_widget.init(self)
        property_widget.init(self)
        connect_actions()
        settings.reset_save_path()
        self.ui.statusbar.addWidget(self.permanent_status_text)
        self.generate_window_title()

        # Icons
        self.setWindowIcon(icons.get_icon())
        self.ui.button_search.setIcon(icons.get_search_icon())

        if open_file_path is not None:
            open_file.import_data(self, open_file_path)

    # Windows

    def open_mapping_window(self):
        self.mapping_window = mapping_window.MappingWindow(self)
        self.mapping_window.show()

    def open_grouping_window(self):
        if self.group_window is None:
            self.group_window = grouping_window.GroupingWindow(self)
        else:
            self.group_window.show()

    def open_modelcheck_window(self):
        if self.modelcheck_window is None:
            self.modelcheck_window = modelcheck_window.ModelcheckWindow(self)
        else:
            self.modelcheck_window.show()

    def open_attribute_import_window(self):
        if self.model_control_window is None:
            self.model_control_window = attribute_import_window.AttributeImport(self)
        else:
            self.model_control_window.show()

    def open_project_phase_window(self):
        if self.project_phase_window is None:
            self.project_phase_window = project_phase_window.ProjectPhaseWindow(self)
        self.project_phase_window.show()

    def open_predefined_pset_window(self):
        if self.predefined_pset_window is None:
            self.predefined_pset_window = predefined_psets_window.PropertySetInherWindow(self)
        self.predefined_pset_window.show()

    def open_settings_window(self):
        settings_window.SettingsDialog(self)

    def open_aggregation_window(self):
        self.graph_window.show()

    @property
    def object_tree(self) -> object_widget.CustomTree:
        return self.ui.tree_object

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
        object_widget.clear_all(self)
        property_widget.clear_all(self)
        self.predefined_pset_window.clear_all()
        self.project.clear()

    def reload(self):
        object_widget.reload(self)
        predefined_psets_window.reload(self)
        property_widget.reload(self)
        self.generate_window_title()

    def generate_window_title(self) -> str:
        text = f"SOM-Toolkit v{__version__}"
        self.setWindowTitle(text)
        self.permanent_status_text.setText(f"{self.project.name} v{self.project.version}")
        return text
