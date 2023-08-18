from __future__ import annotations

import logging
import logging.config
import os
import sys
import json

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QCompleter, QDialog, QTableWidget, QInputDialog, QLineEdit,QFileDialog,QLabel
from SOMcreator import classes, desite,vestra,card1,filehandling,allplan
from SOMcreator import excel as som_excel
from . import icons
from . import logs
from .filehandling import open_file, save_file, export
from .qt_designs import ui_project_settings
from .qt_designs.ui_mainwindow import Ui_MainWindow
from .widgets import  property_widget, object_widget
from som_gui.windows.aggregation_view import aggregation_window
from .windows import predefined_psets_window, propertyset_window, mapping_window, popups, modelcheck_window, grouping_window, model_control_window
from . import settings, __version__
def get_icon():
    icon_path = os.path.join(icons.ICON_PATH, icons.ICON_DICT["icon"])
    return QtGui.QIcon(icon_path)


def start_log() -> None:
    if os.path.exists(logs.LOG_PATH):
        os.remove(logs.LOG_PATH)
    logging.config.fileConfig(logs.CONF_PATH, defaults={'logfilename': logs.LOG_PATH.replace("\\", "/")})


class MainWindow(QMainWindow):
    def __init__(self, app):
        def connect():
            # connect Menubar signals
            self.ui.action_file_Open.triggered.connect(self.open_file_clicked)
            self.ui.action_file_new.triggered.connect(self.new_file_clicked)
            self.ui.action_file_Save.triggered.connect(self.save_clicked)
            self.ui.action_file_Save_As.triggered.connect(self.save_as_clicked)
            self.ui.action_desite_export.triggered.connect(self.export_desite_rules)
            self.ui.action_show_list.triggered.connect(self.open_pset_list)
            self.ui.action_settings.triggered.connect(self.open_settings)
            self.ui.action_export_bs.triggered.connect(self.export_bs)
            self.ui.action_export_bookmarks.triggered.connect(self.export_bookmarks)
            self.ui.action_export_boq.triggered.connect(self.export_boq)
            self.ui.action_show_graphs.triggered.connect(self.open_graph)
            self.ui.action_mapping.triggered.connect(self.open_mapping_window)
            self.ui.action_vestra.triggered.connect(self.export_vestra_mapping)
            self.ui.action_card1.triggered.connect(self.card_1)
            self.ui.action_excel.triggered.connect(self.excel_export)
            self.ui.action_mapping_script.triggered.connect(self.create_mapping_script)
            self.ui.action_allplan.triggered.connect(self.export_allplan_excel)
            self.ui.action_abbreviation_json.triggered.connect(self.desite_abbreviation)
            self.ui.table_pset.itemChanged.connect(self.item_changed)
            self.ui.button_search.clicked.connect(self.search_object)
            self.ui.action_modelcheck.triggered.connect(self.run_modelcheck)
            self.ui.action_create_groups.triggered.connect(self.run_groups)
            self.ui.action_model_control.triggered.connect(self.run_model_control)
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app = app
        self.ui.button_search.setIcon(icons.get_search_icon())

        self.parent_property_window = predefined_psets_window.open_pset_list(self)
        self.parent_property_window.hide()
        self.pset_window: None | propertyset_window.PropertySetWindow = None
        self.obj_line_edit_list = [self.ui.line_edit_object_name,
                                   self.ui.lineEdit_ident_value,
                                   self.ui.lineEdit_ident_attribute,
                                   self.ui.lineEdit_ident_pSet,
                                   self.ui.line_edit_abbreviation]

        # variables
        self.icon = get_icon()
        self.search_ui:popups.ObjectSearchWindow|popups.AttributeSearchWindow|None = None
        self.object_info_widget:object_widget.ObjectInfoWidget|None = None

        self.setWindowIcon(self.icon)
        self._export_path = None
        self.active_object: classes.Object | None = None
        self.graph_window = aggregation_window.AggregationWindow(self)
        self.mapping_window = None
        self.modelcheck_window: modelcheck_window.ModelcheckWindow|None = None
        self.group_window: grouping_window.GroupingWindow|None = None
        self.model_control_window: model_control_window.ModelControlWindow|None = None
        self.project = classes.Project("Project", "")

        # init object and ProertyWidget
        object_widget.init(self)
        property_widget.init(self)
        connect()
        settings.reset_save_path()

        self.permanent_status_text = QLabel()
        self.ui.statusbar.addWidget(self.permanent_status_text)
        self.generate_window_title()

    def generate_window_title(self) -> str:
        text = f"SOM-Toolkit v{__version__}"
        self.setWindowTitle(text)
        self.permanent_status_text.setText(f"{self.project.name} v{self.project.version}")
        return text

    def run_groups(self):
        if self.group_window is None:
            self.group_window = grouping_window.GroupingWindow(self)
        else:
            self.group_window.show()

    def run_modelcheck(self):
        if self.modelcheck_window is None:
            self.modelcheck_window = modelcheck_window.ModelcheckWindow(self)
        else:
            self.modelcheck_window.show()

    def run_model_control(self):
        if self.model_control_window is None:
            self.model_control_window = model_control_window.ModelControlWindow(self)

    @property
    def object_tree(self) -> object_widget.CustomTree:
        return self.ui.tree_object

    @property
    def pset_table(self) -> QTableWidget:
        return self.ui.table_pset

    @property
    def save_path(self) -> str:
        return self._save_path

    @save_path.setter
    def save_path(self, value: str) -> None:
        self._save_path = value
        self._export_path = value

    @property
    def export_path(self):
        return self._export_path

    @export_path.setter
    def export_path(self, value):
        self._save_path = value
        self._export_path = value

    # Open / Close windows
    def closeEvent(self, event):
        action = save_file.close_event(self)

        if action:
            app.closeAllWindows()
            event.accept()
        else:
            event.ignore()

    def open_mapping_window(self):
        # if self.mapping_window is None:
        self.mapping_window = mapping_window.MappingWindow(self)
        self.mapping_window.show()

    def open_pset_list(self):
        if self.parent_property_window is not None:
            self.parent_property_window.show()

    # Desite
    def export_desite_rules(self):
        path = export.get_path(self, "qa.xml")
        if path:
            self.export_path = path
            desite.export_modelcheck(self.project, path)



    # filehandling

    # Click Events
    def item_changed(self, item: object_widget.CustomObjectTreeItem | propertyset_window.CustomCheckItem | propertyset_window.CustomTableItem):
        item.update()

    def save_clicked(self):
        save_file.save_clicked(self)

    def save_as_clicked(self):
        save_file.save_as_clicked(self)

    def new_file_clicked(self):
        new_file = popups.msg_unsaved()
        if new_file:
            project_name = QInputDialog.getText(self, "New Project", "new Project Name:", QLineEdit.Normal, "")
            if project_name[1]:
                self.clear_all()
                self.setWindowTitle(self.project.name)
                self.project.name = project_name[0]

    def open_file_clicked(self):
        open_file.open_file_clicked(self)
        self.generate_window_title()

    def merge_new_file(self):
        open_file.merge_new_file(self)

    def open_pset_menu(self, position):
        property_widget.open_menu(self, position)

    # Main
    def clear_all(self):
        object_widget.clear_all(self)
        property_widget.clear_all(self)
        self.parent_property_window.clear_all()
        self.project.clear()

    # ObjectWidget
    def search_object(self):
        object_widget.search_object(self)



    def fill_tree(self) -> None:
        root_item = self.object_tree.invisibleRootItem()
        item_dict: dict[classes.Object, object_widget.CustomObjectTreeItem] = \
            { obj: self.add_object_to_tree(obj, root_item) for obj in classes.Object} #add all Objects to Tree without Order

        for obj in classes.Object:
            tree_item = item_dict[obj]
            if obj.parent is not None:
                parent_item = item_dict[obj.parent]
                root = tree_item.treeWidget().invisibleRootItem()
                item = root.takeChild(root.indexOfChild(tree_item))
                parent_item.addChild(item)
        self.ui.tree_object.resizeColumnToContents(0)

        object_widget.resize_tree(self)

    def info(self):
        object_widget.info(self)

    def reload_objects(self):
        object_widget.reload(self)

    def rc_collapse(self):
        object_widget.rc_collapse(self.ui.tree_object)

    def rc_expand(self):
        object_widget.rc_expand(self.ui.tree_object)


    def update_completer(self):
        completer = QCompleter(property_widget.predefined_pset_list(self), self)
        self.ui.lineEdit_ident_pSet.setCompleter(completer)
        self.ui.lineEdit_pSet_name.setCompleter(completer)

    def object_clicked(self, item):
        object_widget.single_click(self, item)

    def set_ident_line_enable(self, value: bool):
        object_widget.set_ident_line_enable(self, value)


    def clear_object_input(self):
        object_widget.clear_object_input(self)

    def add_object(self):
        object_widget.add_object(self)

    def add_object_to_tree(self, obj: classes.Object, parent=None):
        val =  object_widget.add_object_to_tree(self, obj, parent)
        self.ui.tree_object.resizeColumnToContents(0)
        return val

    # PropertyWidget
    def attribute_double_clicked(self, item):
        property_widget.attribute_double_click(self, item)

    def delete_pset(self):
        property_widget.delete_selection(self)

    def rename_pset(self):
        property_widget.rename(self)

    def text_changed(self, text):
        property_widget.text_changed(self, text)

    def set_right_window_enable(self, value: bool):
        property_widget.set_enable(self, value)

    def list_object_clicked(self, item):
        property_widget.left_click(self, item)

    def list_object_double_clicked(self, item):
        property_widget.double_click(self, item)

    def open_pset_window(self, property_set: classes.PropertySet, active_object, window_title=None) -> None:
        property_widget.open_pset_window(self, property_set, active_object, window_title)

    def add_pset(self):
        property_widget.create_new_pset(self)

    def selected_object(self):
        return object_widget.selected_object(self)

    def export_bs(self):
        path = export.get_path(self, "bs.xml")
        if path:
            desite.export_bs(self.project, path)

    def reload(self):
        self.reload_objects()
        predefined_psets_window.reload(self)
        self.reload_pset_widget()

    def reload_pset_widget(self):
        property_widget.reload(self)

    def open_settings(self):
        dialog = QDialog()
        widget = ui_project_settings.Ui_Dialog()
        widget.setupUi(dialog)
        dialog.setWindowIcon(icons.get_icon())
        dialog.setWindowTitle(f"SOM-Toolkit Version {__version__}")
        widget.lineEdit_project_name.setText(self.project.name)
        widget.lineEdit_author.setText(self.project.author)
        widget.lineEdit_version.setText(self.project.version)

        if dialog.exec():
            self.project.name = widget.lineEdit_project_name.text()
            self.project.author = widget.lineEdit_author.text()
            self.project.version = widget.lineEdit_version.text()
            self.generate_window_title()

    def export_bookmarks(self):
        path = export.get_folder(self)
        if path:
            desite.export_bookmarks(self.project,path)

    def open_graph(self):
        self.graph_window.show()

    ## EXPORT

    def export_boq(self):
        path = export.get_path(self, "csv")
        words = list({pset.name for pset in classes.PropertySet})  # every Pset name only once

        ok, pset_name = popups.req_boq_pset(self, words)
        if path and ok:
            desite.export_boq(path, pset_name)

    def export_vestra_mapping(self) -> None:
        file_text = "Excel Files (*.xlsx);;"
        if self._export_path is None:
            self._export_path = str(os.getcwd() + "/")
        excel_path, answer = QFileDialog.getOpenFileName(self, "Template Excel", self._export_path, file_text)
        if answer:
            export_folder = QFileDialog.getExistingDirectory(self, "Export Folder", self._export_path)
            if export_folder:
                vestra.create_mapping(excel_path, export_folder, self.project)

    def card_1(self) -> None:
        file_text = "Excel Files (*.xlsx);;"
        if self._export_path is None:
            self._export_path = str(os.getcwd() + "/")

        src, answer = QFileDialog.getOpenFileName(self, "Template Excel", self._export_path, file_text)
        if not answer:
            return
        dest = QFileDialog.getSaveFileName(self, "CARD1 Excel", self._export_path, file_text)[0]

        if dest:
            card1.create_mapping(src, dest, self.project)

    def excel_export(self):
        if self._export_path is None:
            self._export_path = str(os.getcwd() + "/")
        dest = QFileDialog.getSaveFileName(self, "SOM Excel", self._export_path, "Excel Files (*.xlsx);;")[0]
        if not dest:
            return
        mapping_dict = {"aus": "Ausbau", "lst": "LST"}  # TODO: implement GUI method to create extra mapping dict

        som_excel.export(self.project, dest, mapping_dict)

    def create_mapping_script(self):
        name, answer = popups.req_export_pset_name(self)

        if not answer:
            return

        file_text = "JavaScript (*.js);;"
        if self._export_path is None:
            self._export_path = str(os.getcwd() + "/")

        path = QFileDialog.getSaveFileName(self, "Safe Mapping Script", self._export_path, file_text)[0]
        if not path:
            return

        project = self.project
        filehandling.create_mapping_script(project, name, path)

    def export_allplan_excel(self) -> None:
        file_text = "Excel Files (*.xlsx);;"
        if self._export_path is None:
            self._export_path = str(os.getcwd() + "/")
        name, answer = popups.req_export_pset_name(self)
        if not answer:
            return
        path = QFileDialog.getSaveFileName(self, "Safe Attribute Excel", self._export_path, file_text)[0]

        if path:
            allplan.create_mapping(self.project, path, name)



    def desite_abbreviation(self) -> None:
        abbrev = {obj.abbreviation: [obj.ident_value, obj.name] for obj in
                  self.project.objects}
        file_text = "JSON (*.json);;"
        path = QFileDialog.getSaveFileName(self, "Abbreviations File", self._export_path, file_text)[0]
        if path is not None:
            with open(path, "w") as file:
                json.dump(abbrev, file, indent=2)

def main():
    start_log()
    global app
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()
    window.resize(1200, 550)

    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()
