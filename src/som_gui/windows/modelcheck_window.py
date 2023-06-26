from __future__ import annotations
from typing import TYPE_CHECKING
import os
from ..qt_designs import ui_modelcheck
from PySide6.QtWidgets import QDialog,QFileDialog
from PySide6.QtGui import QPalette
from ..settings import get_ifc_path,get_issue_path,set_ifc_path,set_issue_path
if TYPE_CHECKING:
    from ..main_window import MainWindow

FILE_SPLIT = "; "


class ModelcheckWindow(QDialog):
    def __init__(self,main_window:MainWindow):
        super(ModelcheckWindow, self).__init__()
        self.main_window = main_window
        self.widget = ui_modelcheck.Ui_Dialog()
        self.widget.setupUi(self)

        self.widget.button_ifc.clicked.connect(self.ifc_file_dialog)
        self.widget.button_export.clicked.connect(self.export_file_dialog)
        pset,attribute = self.get_main_attribute()
        self.widget.line_edit_ident_pset.setText(pset)
        self.widget.line_edit_ident_attribute.setText(attribute)
        self.data_base_path = None
        self.widget.label_ifc_missing.hide()
        self.widget.label_export_missing.hide()
        self.widget.label_export_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.label_ifc_missing.setStyleSheet("QLabel { color : red; }")
        self.widget.line_edit_ifc.textEdited.connect(self.widget.label_ifc_missing.hide)
        self.widget.line_edit_export.textEdited.connect(self.widget.label_export_missing.hide)



    def accept(self) -> None:
        allow = True
        if not self.get_ifc_path():
            if self.widget.line_edit_ifc.text():
                self.widget.label_ifc_missing.setText("Path doesn't exist!")
            else:
                self.widget.label_ifc_missing.setText("IFC File Path is missing!")
            self.widget.label_ifc_missing.show()
            allow = False
        export_path = self.widget.line_edit_export.text()
        if not export_path:
            self.widget.label_export_missing.setText("Export Path is missing!")
            self.widget.label_export_missing.show()
            allow = False

        elif not os.path.exists(export_path):
            self.widget.label_export_missing.setText("Path doesn't exist!")
            self.widget.label_export_missing.show()
            allow = False


        if allow:
            super(ModelcheckWindow, self).accept()

    def ifc_file_dialog(self):
        file_text = "IFC Files (*.ifc *.IFC);;"
        path = QFileDialog.getOpenFileNames(self,"IFC-Files",get_ifc_path(),file_text)[0]
        if not path:
            return
        set_ifc_path(path)
        self.widget.line_edit_ifc.setText(FILE_SPLIT.join(path))

    def export_file_dialog(self):
        file_text = "Excel File (*.xlsx);;"
        path = QFileDialog.getSaveFileName(self, "Issue-Excel",get_issue_path(), file_text)[0]
        if not path:
            return
        set_issue_path(path)
        self.widget.line_edit_export.setText(path)

    def get_ifc_path(self) -> list[str]:
        paths = self.widget.line_edit_ifc.text().split(FILE_SPLIT)
        result = list()
        for path in paths:
            if not os.path.exists(path):
                print(f"IFC-File does not exist: '{path}'")
            else:
                result.append(path)
        return result

    def get_main_attribute(self) -> (str,str):
        proj = self.main_window.project
        ident_attributes = dict()
        ident_psets = dict()
        for obj in proj.objects:
            ident_pset = obj.ident_attrib.property_set.name
            ident_attribute = obj.ident_attrib.name
            if not ident_pset in ident_psets:
                ident_psets[ident_pset] = 0
            if not ident_attribute in ident_attributes:
                ident_attributes[ident_attribute] = 0
            ident_psets[ident_pset] +=1
            ident_attributes[ident_attribute]+=1

        ident_attribute = (sorted(ident_attributes.items(), key=lambda x: x[1]))
        ident_pset = (sorted(ident_psets.items(), key=lambda x: x[1]))
        if ident_attribute and ident_pset:
            return ident_pset[0][0],ident_attribute[0][0]
        else:
            return "",""
