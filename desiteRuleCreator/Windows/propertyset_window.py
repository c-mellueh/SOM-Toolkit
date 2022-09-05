from __future__ import annotations
import os
import logging
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox, QMenu,QTableWidgetItem

from desiteRuleCreator import icons
from desiteRuleCreator.QtDesigns import ui_widget,ui_mainwindow
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.data import constants,classes
from desiteRuleCreator.data.classes import PropertySet, Attribute
from desiteRuleCreator import icons

def float_to_string(value):
    value = str(value).replace(".", ",")
    return value


def string_to_float(value: str):
    value = float(value.replace(",", "."))

    return value

class LineInput(QLineEdit):
    def __init__(self,parent):
        super(LineInput, self).__init__(parent)
        self.pset_window = parent

    def keyPressEvent(self, event:QtGui.QKeyEvent) -> None:

        if event.matches(QtGui.QKeySequence.Paste):
            text = QtGui.QGuiApplication.clipboard().text()
            text_list = text.split(constants.DIVIDER)
            if len(text_list)<2:
                super(LineInput, self).keyPressEvent(event)
                return

            dif =len(text_list)- len (self.pset_window.input_lines)
            if dif >=0:
                for i in range(dif+1):
                    self.pset_window.new_line()

            lines = [line for line in self.pset_window.input_lines.values()]
            for i,text in enumerate(text_list):
                text = text.strip()
                line:LineInput = lines[i]
                line.setText(text)

        else:
            super(LineInput, self).keyPressEvent(event)

class PropertySetWindow(QtWidgets.QWidget):
    def __init__(self, main_window, property_set: PropertySet, active_object, window_title):
        super(PropertySetWindow, self).__init__()
        self.widget = ui_widget.Ui_layout_main()
        self.widget.setupUi(self)
        self.mainWindow = main_window
        self.property_set = property_set
        self.active_object = active_object
        fill_attribute_table(self.active_object,self.widget.table_widget,self.property_set)
        self.input_lines = {}
        self.widget.table_widget.itemClicked.connect(self.list_clicked)
        self.widget.combo_type.currentTextChanged.connect(self.combo_change)
        self.old_state = self.widget.combo_type.currentText()
        self.widget.lineEdit_name.textChanged.connect(self.text_changed)
        self.widget.combo_data_type.currentTextChanged.connect(self.data_combo_change)

        self.widget.button_add.clicked.connect(self.add_button_pressed)
        self.widget.button_add_line.clicked.connect(self.new_line)

        self.widget.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.table_widget.customContextMenuRequested.connect(self.open_menu)
        self.setWindowTitle(window_title)
        self.setWindowIcon(icons.get_icon())
        self.show()
        self.resize(1000, 400)
        self.new_line()

    def selected_items(self) -> list[classes.CustomTableItem]:
        selected_items = self.widget.table_widget.selectedItems()
        return selected_items

    def delete_selection(self):
        selected_items = self.selected_items()

        string_list = list()

        selected_rows = []
        for items in selected_items:
            row = items.row()
            if row not in selected_rows:
                name = self.widget.table_widget.item(row, 0).text()
                string_list.append(name)
                if attribute_is_identifier(self.active_object,self.get_attribute_by_name(name)):
                    popups.msg_mod_ident()
                    return
                else:
                    selected_rows.append(items.row())


        delete_request = popups.msg_del_items(string_list)

        if delete_request:

            selected_rows.sort(reverse=True)

            for row in selected_rows:
                name = self.widget.table_widget.item(row, 0).text()
                self.widget.table_widget.removeRow(row)
                attribute = self.get_attribute_by_name(name)
                attribute.delete()

            pass

    def open_menu(self, position):
        menu = QMenu()
        self.action_delete_attribute = menu.addAction("Delete")
        self.action_rename_attribute = menu.addAction("Rename")
        self.action_delete_attribute.triggered.connect(self.delete_selection)
        self.action_rename_attribute.triggered.connect(self.rename_selection)

        columns = self.widget.table_widget.columnCount()
        selected_rows = len(self.selected_items())/columns
        if logging.root.level <= logging.DEBUG and selected_rows ==1:
            self.action_info = menu.addAction("Info")
            self.action_info.triggered.connect(self.info)

        menu.exec(self.widget.table_widget.viewport().mapToGlobal(position))


    def info(self, main_window):
        table_item = self.selected_items()[0]
        item = table_item.item
        print(item.name)
        print(f"parent: {item.parent}")

        if item.children:
            print("children:")
            for child in item.children:
                print(f"  {child}")
        else:
            print("no children")


    def get_attribute_by_name(self, name):
        for attribute in self.property_set.attributes:
            if attribute.name == name:
                return attribute
        return False

    def rename_selection(self):  # TODO: check for existing Name
        selected_items = self.widget.table_widget.selectedItems()
        selected_rows = []
        for items in selected_items:
            row = items.row()
            if row not in selected_rows:
                name = self.widget.table_widget.item(row, 0).text()
                if attribute_is_identifier(self.active_object,self.get_attribute_by_name(name)):
                    popups.msg_mod_ident()
                    return
                else:
                    selected_rows.append(items.row())

        selected_rows.sort(reverse=True)

        if len(selected_rows) == 1:
            new_name, fulfilled = popups.req_new_name(self)
            if fulfilled:
                name = self.widget.table_widget.item(row, 0).text()
                attribute: Attribute = self.get_attribute_by_name(name)
                attribute.name = new_name
                self.widget.table_widget.item(row, 0).setText(new_name)

    def delete_attribute(self):

        attribute: Attribute = self.get_attribute_by_name(self.widget.lineEdit_name.text())
        if attribute:
            attribute.delete()
            row = self.widget.table_widget.findItems(attribute.name, Qt.MatchFlag.MatchExactly)[0].row()
            self.widget.table_widget.removeRow(row)

        self.clear_lines()

    def data_combo_change(self, text):
        if text == constants.DATATYPE_NUMBER:
            validator = QtGui.QDoubleValidator()
            validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        else:
            validator = QtGui.QRegularExpressionValidator()

        for el in self.input_lines.values():
            if self.widget.combo_type.currentText() == constants.RANGE:
                for item in el:
                    item.setValidator(validator)
            else:
                el.setValidator(validator)

    def text_changed(self, text):
        name_match = len([x for x in self.property_set.attributes if x.name == text]) > 0
        if name_match:
            self.widget.button_add.setText("Update")
        else:
            self.widget.button_add.setText("Add")

    def add_button_pressed(self):
        def fill_table_line(row, attribute: Attribute):
            table = self.widget.table_widget
            table.item(row, 0).setText(attribute.name)
            table.item(row, 1).setText(attribute.data_type)
            table.item(row, 2).setText(constants.VALUE_TYPE_LOOKUP[attribute.value_type])
            table.item(row, 3).setText(str(attribute.value))

        def add_table_line(row, attribute: Attribute):
            table = self.widget.table_widget
            table.setItem(row, 0, QTableWidgetItem(attribute.name))
            table.setItem(row, 1, QTableWidgetItem(attribute.data_type))
            table.setItem(row, 2, QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[attribute.value_type]))
            table.setItem(row, 3, QTableWidgetItem(str(attribute.value)))

        def get_values():
            values = []

            value_type = self.widget.combo_type.currentText()
            data_type = self.widget.combo_data_type.currentText()
            if value_type != constants.RANGE:
                for line in self.input_lines.values():
                    value = line.text()
                    if len(value.strip()) > 0:
                        values.append(value)
            else:
                for line in self.input_lines.values():
                    value1 = line[0].text()
                    value2 = line[1].text()
                    if len(value1.strip()) > 0 or len(value2.strip()) > 0:
                        values.append([value1, value2])

            if data_type == constants.DATATYPE_NUMBER:
                for i, value in enumerate(values):
                    try:
                        if self.widget.combo_type.currentText() == constants.RANGE:
                            values[i] = [string_to_float(value[0]), string_to_float(value[1])]
                        else:
                            values[i] = string_to_float(value)
                    except ValueError:  #move to popup
                        msg_box= QMessageBox()
                        msg_box.setText("Value can't be converted to Double!")
                        msg_box.setWindowTitle(" ")
                        msg_box.setIcon(QMessageBox.Icon.Warning)
                        msg_box.exec()
            return values

        def update_attribute(attribute: Attribute):
            if not attribute.is_child:
                attribute.value_type = self.widget.combo_type.currentText()
                attribute.data_type = self.widget.combo_data_type.currentText()
                attribute.child_inherits_values = self.widget.check_box_inherit.isChecked()
            values = get_values()
            attribute.value = values

            item: QTableWidgetItem = self.widget.table_widget.findItems(attribute.name, Qt.MatchFlag.MatchExactly)[0]
            row = item.row()
            fill_table_line(row, attribute)
            return attribute
        def add_attribute():
            name = self.widget.lineEdit_name.text()

            if name:
                values = get_values()
                value_type = self.widget.combo_type.currentText()
                data_type = self.widget.combo_data_type.currentText()

                attribute = Attribute(self.property_set, name, values, value_type, data_type)
                attribute.child_inherits_values = self.widget.check_box_inherit.isChecked()
                rows = self.widget.table_widget.rowCount() + 1
                self.widget.table_widget.setRowCount(rows)
                add_table_line(rows - 1, attribute)
                return attribute
            else:
                popups.msg_missing_input()
                return None

        already_exists = False
        attribute = None
        for attrib in self.property_set.attributes:
            if attrib.name == self.widget.lineEdit_name.text():
                attribute = update_attribute(attrib)
                already_exists = True

        if not already_exists:
            attribute = add_attribute()
        if attribute is not None:
            if attribute_is_identifier(self.mainWindow.active_object,attribute):
                self.mainWindow.reload_objects()
        self.clear_lines()

    def combo_change(self, event):
        if event in constants.RANGE_STRINGS:
            for el in self.input_lines:
                self.lineEdit_input2 = QLineEdit(self)
                el.addWidget(self.lineEdit_input2)
                el.removeWidget(self.widget.button_add_line)
                el.addWidget(self.widget.button_add_line)
                self.input_lines[el] = [self.input_lines[el], self.lineEdit_input2]

        elif self.old_state in constants.RANGE_STRINGS:
            for layout, items in self.input_lines.items():
                layout.removeWidget(items[1])
                items[1].setParent(None)
                self.input_lines[layout] = items[0]

        self.old_state = event

    

    def new_line(self):
        def range_mode(self):

            self.lineEdit_input2 = QLineEdit(self)
            self.new_layout.addWidget(self.lineEdit_input2)
            self.input_lines[self.new_layout] = [self.lineEdit_input, self.lineEdit_input2]
        # if len(self.input_lines)>0:
        self.widget.layout_input.removeWidget(self.widget.button_add_line)
        self.new_layout = QHBoxLayout()
        self.lineEdit_input = LineInput(self)
        self.new_layout.addWidget(self.lineEdit_input)

        self.widget.verticalLayout.insertLayout(0, self.new_layout)

        status = self.widget.combo_type.currentText()
        if status in constants.RANGE_STRINGS:
            range_mode()
            line_edit = [self.lineEdit_input, self.lineEdit_input2]

        else:
            self.input_lines[self.new_layout] = self.lineEdit_input
            line_edit = self.lineEdit_input
        self.new_layout.addWidget(self.widget.button_add_line)
        return line_edit



    def clear_lines(self):

        for key, item in tuple(self.input_lines.items()):
            if len(self.input_lines)>1:
                if key != self.widget.layout_input:
                    v_layout: QHBoxLayout = key.parent()
                    v_layout.removeItem(key)
                    key.setParent(None)
                    if isinstance(item, list):
                        for i in item:
                            v_layout.removeWidget(i)
                            i.setParent(None)
                    else:
                        v_layout.removeWidget(item)
                        item.setParent(None)
                    del self.input_lines[key]
            else:
                key.addWidget(self.widget.button_add_line)
        self.widget.lineEdit_name.setText("")
        for items in self.input_lines.values():
            if isinstance(items, list):
                for item in items:
                    item.setText("")
            else:
                items.setText("")
        #self.widget.layout_input


    def list_clicked(self, tree_item:QTableWidgetItem|classes.CustomTableItem ):

        item: QTableWidgetItem = self.widget.table_widget.item(tree_item.row(), 0)
        attribute: Attribute = self.get_attribute_by_name(item.text())
        index = self.widget.combo_type.findText(attribute.value_type)
        self.widget.combo_type.setCurrentIndex(index)
        index = self.widget.combo_data_type.findText(attribute.data_type)
        self.widget.combo_data_type.setCurrentIndex(index)
        self.clear_lines()

        # Add Values
        for k, value in enumerate(attribute.value):
            lines = self.new_line()
            if attribute.value_type == constants.RANGE:
                for k, val in enumerate(value):
                    if attribute.data_type == constants.XS_DOUBLE:
                        lines[k].setText(float_to_string(val))
                    else:
                        lines[k].setText(val)
            else:
                if attribute.data_type == constants.XS_DOUBLE:
                    lines.setText(float_to_string(value))
                else:
                    lines.setText(value)
        # input Name
        self.widget.lineEdit_name.setText(attribute.name)

        # set Editable
        self.widget.check_box_inherit.setChecked(attribute.child_inherits_values)

def fill_attribute_table(active_object,table_widget,property_set):
    def reformat_identifier(row):
        brush = QtGui.QBrush()
        brush.setColor(Qt.GlobalColor.lightGray)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        for column in range(4):
            item = table_widget.item(row, column)
            item.setBackground(brush)

    table_widget.setRowCount(len(property_set.attributes))

    link_item = icons.get_link_icon()

    for i, attribute in enumerate(property_set.attributes):
        attribute: Attribute = attribute
        value_item = classes.CustomTableItem(attribute)
        value_item.setText(attribute.name)

        if attribute.is_child:
            value_item.setIcon(link_item)
        table_widget.setItem(i, 0, value_item)
        table_widget.setItem(i, 1, QTableWidgetItem(attribute.data_type))
        table_widget.setItem(i, 2, QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[attribute.value_type]))
        table_widget.setItem(i, 3, QTableWidgetItem(str(attribute.value)))

        if attribute_is_identifier(active_object,attribute):
            reformat_identifier(i)

        table_widget.resizeColumnsToContents()

def attribute_is_identifier(active_object, attribute):
    if active_object is not None:
        if active_object.ident_attrib == attribute:
            return True
    return False