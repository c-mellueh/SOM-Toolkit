from som_gui.module import objects
from PySide6.QtWidgets import QTreeWidget, QWidget, QDialog
from som_gui.module.objects.window import Ui_ObjectInfo

def load_triggers():
    objects.trigger.connect()


class ObjectTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.test_bool = False

    def paintEvent(self, event):
        super().paintEvent(event)
        objects.trigger.repaint_event()

    def changeEvent(self, event):
        super().changeEvent(event)
        objects.trigger.change_event()

    def dropEvent(self, event):
        objects.trigger.drop_event(event)
        super().dropEvent(event)


class ObjectInfoWidget(QDialog):
    def __init__(self):
        super(ObjectInfoWidget, self).__init__()
        #     def connect():
        #         self.widget.line_edit_attribute_value.textChanged.connect(self.ident_edited)
        #         self.widget.line_edit_abbreviation.textChanged.connect(self.abbrev_edited)
        #         self.widget.combo_box_pset.currentIndexChanged.connect(
        #             self.pset_combobox_change
        #         )
        #         self.widget.button_gruppe.clicked.connect(self.concept_state_changed)
        self.widget = Ui_ObjectInfo()
        self.widget.setupUi(self)

    #
    #     connect()
    #
    #     self.setWindowTitle(f"bearbeite Objektvorgabe '{self.object.name}'")
    #     self.setWindowIcon(get_icon())
    #
    #     self.widget.button_add_ifc.clicked.connect(self.add_line)
    #
    #     self.ifc_lines: list[QLineEdit] = [self.widget.line_edit_ifc]
    #     self.completer = QCompleter(IFC_4_1)
    #     self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    #     self.widget.line_edit_ifc.setCompleter(self.completer)
    #     self.fill_with_values()

    def paintEvent(self, event):
        objects.trigger.object_info_paint_event()
        super().paintEvent(event)

    # @property
    # def is_concept(self):
    #     return self.widget.button_gruppe.isChecked()
    #
    # def concept_state_changed(self):
    #     if self.widget.button_gruppe.isChecked():
    #         self.hide_identifier()
    #     else:
    #         self.show_identifier()
    #
    # def hide_identifier(self):
    #     for i in range(self.widget.layout_ident_attribute.count()):
    #         self.widget.layout_ident_attribute.itemAt(i).widget().hide()
    #
    # def show_identifier(self):
    #     for i in range(self.widget.layout_ident_attribute.count()):
    #         self.widget.layout_ident_attribute.itemAt(i).widget().show()
    #
    # def ident_edited(self, val):
    #     check_obj = self.object
    #     if self.copy:
    #         check_obj = None
    #
    #     if check_identifier(self.main_window.project, check_obj, val):
    #         style = "color:red"
    #     else:
    #         style = "color:black"
    #     self.widget.line_edit_attribute_value.setStyleSheet(style)
    #
    # def abbrev_edited(self, val):
    #     check_obj = self.object
    #     if self.copy:
    #         check_obj = None
    #     if check_abbrev(self.main_window.project, check_obj, val):
    #         style = "color:red"
    #     else:
    #         style = "color:black"
    #     self.widget.line_edit_abbreviation.setStyleSheet(style)
    #
    # def pset_combobox_change(self, item_index):
    #     self.widget.combo_box_attribute.clear()
    #     text = self.widget.combo_box_pset.itemText(item_index)
    #     pset = self.object.get_property_set_by_name(text)
    #     attribute_list = [
    #         attribute.name
    #         for attribute in pset.attributes
    #         if attribute.data_type == value_constants.LABEL
    #     ]
    #     self.widget.combo_box_attribute.addItems(attribute_list)
    #
    # def fill_with_values(self):
    #     self.widget.line_edit_abbreviation.setText(self.object.abbreviation)
    #     self.widget.line_edit_name.setText(self.object.name)
    #     ifc_mappings = len(self.object.ifc_mapping)
    #     self.widget.combo_box_pset.addItems(
    #         sorted([pset.name for pset in self.object.property_sets])
    #     )
    #     for _ in range(ifc_mappings - 1):
    #         self.add_line()
    #
    #     for index, ifc_mapping in enumerate(self.object.ifc_mapping):
    #         self.ifc_lines[index].setText(ifc_mapping)
    #
    #     if self.object.is_concept:
    #         self.hide_identifier()
    #         self.widget.button_gruppe.setChecked(True)
    #         return
    #
    #     self.widget.combo_box_pset.setCurrentText(
    #         self.object.ident_attrib.property_set.name
    #     )
    #     self.widget.combo_box_attribute.setCurrentText(self.object.ident_attrib.name)
    #     self.widget.line_edit_attribute_value.setText(self.object.ident_value)
    #
    # @property
    # def ifc_values(self) -> set[str]:
    #     return {line.text() for line in self.ifc_lines if line and line is not None}
    #
    # def add_line(self):
    #     line_edit = QLineEdit()
    #     line_edit.setCompleter(self.completer)
    #     self.ifc_lines.append(line_edit)
    #     self.widget.vertical_layout_ifc.addWidget(line_edit)
    #     line_edit.show()
    #
    # def exec(self):
    #     return_value = super().exec()
    #     if not return_value:
    #         return return_value
    #
    #     abbreviation = self.widget.line_edit_abbreviation.text()
    #     ident_value = self.widget.line_edit_attribute_value.text()
    #     if check_abbrev(self.main_window.project, self.object, abbreviation):
    #         popups.msg_abbrev_already_exists()
    #         return False
    #
    #     if self.object.is_concept:
    #         return return_value
    #
    #     if check_identifier(self.main_window.project, self.object, ident_value):
    #         popups.msg_ident_already_exists()
    #         return False
    #
    #     return return_value
