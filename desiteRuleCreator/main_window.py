import os
import sys

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from . import constants
from . import filehandling
from . import object_widget
from . import property_widget
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

        # variables
        self.icon = get_icon()
        self.setWindowIcon(self.icon)
        self.save_path = None
        self.project_name = ""

        # init object and ProertyWidget
        object_widget.init(self)
        property_widget.init(self)

        # connect Menubar signals
        self.ui.action_file_Open.triggered.connect(self.openFile_dialog)
        self.ui.action_file_new.triggered.connect(self.new_file)
        self.ui.action_file_Save.triggered.connect(self.save_clicked)
        self.ui.action_file_Save_As.triggered.connect(self.save_as_clicked)

        # debug: preload file
        #self.openFile(path="E:/Cloud/OneDrive/Arbeit/DB_Werkstudent/Projekte/Karlsruhe_Durmersheim/Modelchecking/Regeln/Datenstruktur/22_04_18.xml")
        self.openFile("desiteRuleCreator/saves/test.xml")
        self.tree.resizeColumnToContents(0)
        self.changed = False

    def closeEvent(self, event):
        filehandling.close_event(self, event)

    # Filehandling
    def save_clicked(self):
        filehandling.save_clicked(self)

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

    def object_double_clicked(self, item):
        object_widget.double_click(self, item)

    def setIdentLineEnable(self, value: bool):
        object_widget.setIdentLineEnable(self, value)

    def treeObjectClicked(self):
        object_widget.single_click(self)

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

    def set_pset_window_enable(self, value: bool):
        property_widget.set_enable(self, value)

    def listObjectClicked(self, item):
        property_widget.left_click(self, item)

    def listObjectDoubleClicked(self, item):
        property_widget.double_click(self, item)

    def openPsetWindow(self, propertySet: PropertySet):
        return property_widget.openPsetWindow(propertySet)

    def addPset(self):
        property_widget.addPset(self)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(1200, 550)

    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()
