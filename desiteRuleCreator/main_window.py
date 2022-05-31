import os
import sys

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from . import constants,filehandling,object_widget,property_widget,desite_export,classes,script_widget,property_list_widget
from .QtDesigns.ui_mainwindow import Ui_MainWindow
from .classes import Object, PropertySet


def get_icon():
    here = os.path.dirname(__file__)
    icon_name = constants.ICON_PATH
    icon_path = os.path.join(here, icon_name)
    return QtGui.QIcon(icon_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.property_list_widget = None
        self.property_list_widget:property_list_widget.PropertySetInherWindow =self.open_pset_list()
        self.property_list_widget.hide()

        # variables
        self.icon = get_icon()
        self.setWindowIcon(self.icon)
        self._save_path = None
        self._export_path = None
        self.active_object = None
        self.project = classes.Project("")

        # init object and ProertyWidget
        object_widget.init(self)
        property_widget.init(self)
        script_widget.init(self)

        # connect Menubar signals
        self.ui.action_file_Open.triggered.connect(self.openFile_dialog)
        self.ui.action_file_new.triggered.connect(self.new_file)
        self.ui.action_file_Save.triggered.connect(self.save_clicked)
        self.ui.action_file_Save_As.triggered.connect(self.save_as_clicked)
        self.ui.action_desite_Export.triggered.connect(self.export_desite_rules)
        self.ui.action_show_list.triggered.connect(self.open_pset_list)

        self.ui.code_edit.textChanged.connect(self.update_script)

        # debug: preload file
        #self.openFile(path="E:/Cloud/OneDrive/Arbeit/DB_Werkstudent/Projekte/Karlsruhe_Durmersheim/Modelchecking/Regeln/Datenstruktur/22_04_18.xml")
        #self.openFile("desiteRuleCreator/saves/22_04_18.xml")
        self.ui.tree.resizeColumnToContents(0)
        self.save_path = None



    @property
    def save_path(self):
        return self._save_path

    @save_path.setter
    def save_path(self,value):
        self._save_path = value
        self._export_path = value

    @property
    def export_path(self):
        return self._export_path

    @export_path.setter
    def export_path(self,value):
        self._save_path = value
        self._export_path = value

    def update_script(self):
        script_widget.update_script(self)

    def export_desite_rules(self):
        desite_export.save_rules(self)

    def closeEvent(self, event):
        filehandling.close_event(self, event)

    # Filehandling
    def save_clicked(self):
        filehandling.save_clicked(self)

    def open_pset_list(self):
        if self.property_list_widget is not None:
            self.property_list_widget.setHidden(False)
        else:
            self.property_list_widget = property_list_widget.open_pset_list(self)

        return self.property_list_widget

    def save(self, path):
        filehandling.save(self, path)

    def save_as_clicked(self):
        filehandling.save_as_clicked(self)

    def new_file(self):
        filehandling.new_file(self)

    def openFile_dialog(self, path=False):
        filehandling.openFile_dialog(self, path)

    def merge_new_file(self):
        filehandling.merge_new_file(self)

    def openFile(self, path=False):

        if path is False:
            cur_path =os.getcwd()+"/"
            path = QFileDialog.getOpenFileName(self, "Open XML", str(cur_path), "xml Files (*.xml *.DRCxml)")[0]


        if path:
            filehandling.importData(self, path)

    # Main
    def clear_all(self):
        object_widget.clear_all(self)
        property_widget.clear_all(self)

    # ObjectWidget
    def right_click(self, position: QtCore.QPoint):
        object_widget.right_click(self, position)

    def rc_collapse(self):
        object_widget.rc_collapse(self.tree)

    def rc_expand(self):
        object_widget.rc_expand(self.tree)

    def rc_group(self):
        object_widget.rc_group_items(self)

    def object_clicked(self,item):
        object_widget.single_click(self)

    def update_completer(self):
        property_widget.update_completer(self)

    def object_double_clicked(self, item):
        object_widget.double_click(self, item)

    def setIdentLineEnable(self, value: bool):
        object_widget.setIdentLineEnable(self, value)

    def delete_selected_scripts(self):
        script_widget.delete_objects(self)

    def script_list_clicked(self,item):
        script_widget.clicked(self,item)

    def clearObjectInput(self):
        object_widget.clear_object_input(self)

    def addObject(self):
        object_widget.addObject(self)

    def addObjectToTree(self, obj: Object, parent=None):
        return object_widget.addObjectToTree(self, obj, parent)

    def deleteObject(self):
        object_widget.deleteObject(self)

    def updateObject(self):
        object_widget.updateObject(self)

    # PropertyWidget
    def delete_pset(self):
        property_widget.delete(self)

    def rename_pset(self):
        property_widget.rename(self)

    def text_changed(self, text):
        property_widget.text_changed(self, text)

    def set_right_window_enable(self, value: bool):
        property_widget.set_enable(self, value)
        script_widget.set_enable(self,value)

    def listObjectClicked(self, item):
        property_widget.left_click(self, item)

    def listObjectDoubleClicked(self, item):
        property_widget.double_click(self, item)

    def openPsetWindow(self, propertySet: PropertySet,active_object,windowTitle = None):
        return property_widget.openPsetWindow(self,propertySet,active_object,windowTitle)

    def addPset(self):
        property_widget.addPset(self)

    def add_script(self):
        script_widget.add_script(self)

    def selected_object(self):
        return object_widget.selected_object(self)

    def change_script_list_visibility(self):
        script_widget.change_script_list_visibility(self)

    def code_item_changed(self,item):
        script_widget.item_changed(self,item)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(1200, 550)

    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()
