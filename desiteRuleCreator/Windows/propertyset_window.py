from __future__ import annotations

import copy
import logging

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt,QPointF
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QMenu, QTableWidgetItem, QTableWidget

from desiteRuleCreator import icons
from desiteRuleCreator.QtDesigns import ui_widget
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.data import constants, classes
from desiteRuleCreator.data.classes import PropertySet, Attribute


def float_to_string(value:float) -> str:
    value = str(value).replace(".", ",")
    return value


def string_to_float(value: str) -> float:
    value = float(value.replace(",", "."))

    return value


def get_selected_rows(table_widget: QTableWidget) -> list[int]:
    selectedRows = []
    for item in table_widget.selectedItems():
        if item.row() not in selectedRows:
            selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows


class LineInput(QLineEdit):
    def __init__(self, parent:PropertySetWindow) -> None:
        super(LineInput, self).__init__(parent)
        self.pset_window = parent
        self.setValidator(self.pset_window.line_validator)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        seperator = self.pset_window.mainWindow.project.seperator
        sep_bool = self.pset_window.mainWindow.project.seperator_status
        if event.matches(QtGui.QKeySequence.Paste) and sep_bool:
            text = QtGui.QGuiApplication.clipboard().text()
            text_list = text.split(seperator)
            if len(text_list) < 2:
                super(LineInput, self).keyPressEvent(event)
                return

            dif = len(text_list) - len(self.pset_window.input_lines)
            if dif >= 0:
                for i in range(dif + 1):
                    self.pset_window.new_line()

            lines = [line for line in self.pset_window.input_lines.values()]
            for i, text in enumerate(text_list):
                text = text.strip()
                line: LineInput = lines[i]
                line.setText(text)

        else:
            super(LineInput, self).keyPressEvent(event)


class PropertySetWindow(QtWidgets.QWidget):
    def __init__(self, main_window, property_set: PropertySet, active_object:classes.Object, window_title):
        def connect_items():
            self.widget.table_widget.itemClicked.connect(self.list_clicked)
            self.widget.combo_type.currentTextChanged.connect(self.combo_change)
            self.widget.lineEdit_name.textChanged.connect(self.text_changed)
            self.widget.combo_data_type.currentTextChanged.connect(self.data_combo_change)
            self.widget.check_box_seperator.stateChanged.connect(self.seperator_status_changed)
            self.widget.line_edit_seperator.textChanged.connect(self.seperator_text_changed)
            self.widget.button_add.clicked.connect(self.add_button_pressed)
            self.widget.button_add_line.clicked.connect(self.new_line)
            self.widget.table_widget.customContextMenuRequested.connect(self.open_menu)

        super(PropertySetWindow, self).__init__()

        self.widget = ui_widget.Ui_layout_main()
        self.widget.setupUi(self)

        self.mainWindow = main_window
        self.property_set = property_set
        self.active_object= active_object
        self.input_lines = {}
        self.old_state = self.widget.combo_type.currentText()
        self._line_validator = QtGui.QRegularExpressionValidator()
        self.table:QTableWidget = self.widget.table_widget

        self.setWindowTitle(window_title)
        self.setWindowIcon(icons.get_icon())
        fill_attribute_table(self.active_object, self.widget.table_widget, self.property_set)

        self.widget.check_box_seperator.setChecked(self.mainWindow.project.seperator_status)
        self.widget.line_edit_seperator.setText(self.mainWindow.project.seperator)
        self.widget.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.table_widget.orig_drop_event = self.widget.table_widget.dropEvent
        self.widget.table_widget.dropEvent = self.tableDropEvent
        self.widget.table_widget.dropMimeData = self.tableDropMimeData

        self.show()
        self.resize(1000, 400)
        self.new_line()

        connect_items()

    @property
    def attribute_type(self) -> str:
        return self.widget.combo_type.currentText()

    @property
    def line_validator(self) -> QtGui.QValidator:
        return self._line_validator

    @line_validator.setter
    def line_validator(self,value:QtGui.QValidator) -> None:
        self._line_validator = value
        for el in self.input_lines.values():
            if self.attribute_type == constants.RANGE:  # if range -> two inputs per line
                for item in el:
                    item.setValidator(value)
            else:
                el.setValidator(value)

    def tableDropEvent(self, event: QtGui.QDropEvent) -> None:

        sender: QTableWidget = event.source()
        if sender == self.table:
            return

        self.widget.table_widget.orig_drop_event(event)
        drop_row = self.last_drop_row
        selected_rows = get_selected_rows(sender)

        sender_attribute_names = {sender.item(row, 0).item.name: row for row in selected_rows}
        receiver_attribute_names = [self.table.item(row, 0).item.name for row in range(self.table.rowCount())]

        for name, row in sender_attribute_names.items():  # remove Rows with existing names
            if name in receiver_attribute_names:
                selected_rows.remove(row)

        for _ in selected_rows:
            self.table.insertRow(drop_row)

        for offset, row_index in enumerate(selected_rows):  # iterate rows
            for col_index in range(self.table.columnCount()):  # iterate columns
                old_item: classes.CustomTableItem
                old_item = sender.item(row_index, col_index)

                if col_index == 0:  # get attribute
                    old_attribute: classes.Attribute = old_item.item
                    new_attribute = copy.copy(old_attribute)
                    self.property_set.add_attribute(new_attribute)
                if old_item:
                    if col_index == 0:
                        new_item = classes.CustomTableItem(new_attribute)
                        new_item.setText(new_attribute.name)
                        if new_attribute.is_child:
                            new_item.setIcon(icons.get_link_icon())
                    else:
                        new_item = QTableWidgetItem(old_item.text())
                    self.table.setItem(offset + drop_row, col_index, new_item)

    def tableDropMimeData(self, row, col, mimeData, action) -> bool:
        self.last_drop_row = row
        return True

    def seperator_text_changed(self, status:str) -> None:
        self.mainWindow.project.seperator = status

    def seperator_status_changed(self, status: int) -> None:
        if status == 2:
            b = True
        else:
            b = False
        self.mainWindow.project.seperator_status = b
        self.widget.line_edit_seperator.setEnabled(b)

    def delete_selection(self) -> None:
        """delete selected Table items"""

        selected_rows = get_selected_rows(self.table)
        attributes = [self.table.item(row,0).item for row in selected_rows]

        if self.active_object.ident_attrib in attributes:
            popups.msg_mod_ident()
            return

        delete_request = popups.msg_del_items([attrib.name for attrib in attributes])
        if not delete_request:
            return

        for row in sorted(selected_rows,reverse=True):
            attribute = self.table.item(row, 0).item
            self.widget.table_widget.removeRow(row)
            attribute.delete()

        self.mainWindow.reload()

    def open_menu(self, position:QPointF) -> None:
        menu = QMenu()
        self.action_delete_attribute = menu.addAction("Delete")
        self.action_rename_attribute = menu.addAction("Rename")
        self.action_delete_attribute.triggered.connect(self.delete_selection)
        self.action_rename_attribute.triggered.connect(self.rename_selection)

        selected_rows = get_selected_rows(self.widget.table_widget)
        #add info if logging= debug
        if logging.root.level <= logging.DEBUG and len(selected_rows) == 1:
            self.action_info = menu.addAction("Info")
            self.action_info.triggered.connect(self.info)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def info(self) -> None:
        """print infos of attribute to console (debug only)"""
        row = get_selected_rows(self.widget.table_widget)[0]
        item = self.widget.table_widget.item(row,0).item
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
        selected_rows = get_selected_rows(self.table)

        if len(selected_rows) == 1:
            row = selected_rows[0]
            new_name, fulfilled = popups.req_new_name(self)
            if fulfilled:
                item = self.table.item(row, 0)
                name = item.text()
                attribute: Attribute = item.item
                attribute.name = new_name
                self.widget.table_widget.item(row, 0).setText(new_name)
                self.mainWindow.reload()

    def data_combo_change(self, text):

        if text == constants.DATATYPE_NUMBER:
            validator = QtGui.QDoubleValidator()
            validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        else:
            validator = QtGui.QRegularExpressionValidator()

        self.line_validator = validator

    def text_changed(self, text):
        name_match = len([x for x in self.property_set.attributes if x.name == text]) > 0
        if name_match:
            self.widget.button_add.setText("Update")
        else:
            self.widget.button_add.setText("Add")

    def add_button_pressed(self):
        def fill_table_line(row, attribute: Attribute):
            table = self.widget.table_widget
            table.setItem(row, 0, classes.CustomTableItem(attribute))
            table.item(row, 1).setText(attribute.data_type)
            table.item(row, 2).setText(constants.VALUE_TYPE_LOOKUP[attribute.value_type])
            table.item(row, 3).setText(str(attribute.value))

        def add_table_line(row, attribute: Attribute):
            table = self.widget.table_widget
            table.setItem(row, 0, classes.CustomTableItem(attribute))
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
                    except ValueError:  # move to popup
                        msg_box = QMessageBox()
                        msg_box.setText("Value can't be converted to Double!")
                        msg_box.setWindowTitle(" ")
                        msg_box.setIcon(QMessageBox.Icon.Warning)
                        msg_box.exec()
                        return None
            return values

        def update_attribute(attribute: Attribute):
            values = get_values()
            if values is None:
                return None

            if not attribute.is_child:
                attribute.value_type = self.widget.combo_type.currentText()
                attribute.data_type = self.widget.combo_data_type.currentText()
                attribute.child_inherits_values = self.widget.check_box_inherit.isChecked()

            attribute.value = values

            item: QTableWidgetItem = self.widget.table_widget.findItems(attribute.name, Qt.MatchFlag.MatchExactly)[0]
            row = item.row()
            fill_table_line(row, attribute)
            return attribute

        def add_attribute():
            name = self.widget.lineEdit_name.text()

            if name:
                values = get_values()
                if values is None:
                    return None
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
                if attribute is None:
                    return
                already_exists = True

        if not already_exists:
            attribute = add_attribute()
        if attribute is not None:
            if attribute_is_identifier(self.mainWindow.active_object, attribute):
                self.mainWindow.reload_objects()
            self.clear_lines()
            self.mainWindow.reload_pset_widget()

    def combo_change(self, event):
        if event in constants.RANGE_STRINGS:
            for el in self.input_lines:
                self.lineEdit_input2 = LineInput(self)
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
        def range_mode():
            self.lineEdit_input2 = LineInput(self)
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
            if len(self.input_lines) > 1:
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
        # self.widget.layout_input

    def fill_with_attribute(self, attribute: classes.Attribute):
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

    def list_clicked(self, tree_item: QTableWidgetItem | classes.CustomTableItem):
        item: QTableWidgetItem = self.widget.table_widget.item(tree_item.row(), 0)
        attribute: Attribute = self.get_attribute_by_name(item.text())
        self.fill_with_attribute(attribute)


def fill_attribute_table(active_object, table_widget, property_set):
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

        if attribute_is_identifier(active_object, attribute):
            reformat_identifier(i)

        table_widget.resizeColumnsToContents()


def attribute_is_identifier(active_object, attribute):
    if active_object is not None:
        if active_object.ident_attrib == attribute:
            return True
    return False
