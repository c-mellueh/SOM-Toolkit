from __future__ import annotations

import copy
import logging

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QMenu, QTableWidgetItem, QTableWidget
from SOMcreator import constants, classes

from .. import icons
from ..QtDesigns import ui_widget
from ..Windows import popups


class CustomTableItem(QTableWidgetItem):
    def __init__(self, item: classes.Object | classes.PropertySet | classes.Attribute):
        super(CustomTableItem, self).__init__()
        self.linked_data = item
        self.setText(item.name)


class MappingTableItem(QTableWidgetItem):
    def __init__(self, attribute: classes.Attribute) -> None:
        super(MappingTableItem, self).__init__()
        self.attribute = attribute
        self.update()

    def update(self) -> None:
        self.setText(self.attribute.revit_name)


def float_to_string(value: float) -> str:
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


def fill_attribute_table(active_object: classes.Object,
                         table_widget: QTableWidget,
                         property_set: classes.PropertySet) -> None:
    def reformat_identifier(row: int) -> None:
        brush = QtGui.QBrush()
        brush.setColor(Qt.GlobalColor.lightGray)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        for column in range(4):
            item = table_widget.item(row, column)
            item.setBackground(brush)

    link_item = icons.get_link_icon()

    table_widget.setRowCount(len(property_set.attributes))

    for i, attribute in enumerate(property_set.attributes):
        value_item = CustomTableItem(attribute)

        if attribute.is_child:
            value_item.setIcon(link_item)
        table_widget.setItem(i, 0, value_item)
        table_widget.setItem(i, 1, QTableWidgetItem(attribute.data_type))
        table_widget.setItem(i, 2, QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[attribute.value_type]))
        table_widget.setItem(i, 3, QTableWidgetItem(str(attribute.value)))
        table_widget.setItem(i, 4, MappingTableItem(attribute))
        table_widget.resizeColumnsToContents()

        if active_object is None:
            return

        if attribute == active_object.ident_attrib:
            reformat_identifier(i)


class LineInput(QLineEdit):
    def __init__(self, parent: PropertySetWindow) -> None:
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
    def __init__(self, main_window, property_set: classes.PropertySet, active_object: classes.Object, window_title):
        def connect_items():
            self.widget.table_widget.itemClicked.connect(self.table_clicked)
            self.widget.table_widget.itemDoubleClicked.connect(self.table_double_clicked)
            self.widget.combo_type.currentTextChanged.connect(self.combo_valuetype_change)
            self.widget.lineEdit_name.textChanged.connect(self.text_changed)
            self.widget.combo_data_type.currentTextChanged.connect(self.data_combo_change)
            self.widget.check_box_seperator.stateChanged.connect(self.seperator_status_changed)
            self.widget.line_edit_seperator.textChanged.connect(self.seperator_text_changed)
            self.widget.button_add.clicked.connect(self.add_attribute_button_pressed)
            self.widget.button_add_line.clicked.connect(self.new_line)
            self.widget.table_widget.customContextMenuRequested.connect(self.open_menu)
            self.widget.lineEdit_name.returnPressed.connect(self.add_attribute_button_pressed)

        super(PropertySetWindow, self).__init__()

        self.widget = ui_widget.Ui_layout_main()
        self.widget.setupUi(self)

        self.mainWindow = main_window
        self.property_set = property_set
        self.active_object = active_object
        self.input_lines = {}
        self.old_state = self.widget.combo_type.currentText()
        self._line_validator = QtGui.QRegularExpressionValidator()
        self.table: QTableWidget = self.widget.table_widget

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
    def line_validator(self, value: QtGui.QValidator) -> None:
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
        sender_attribute_names = {sender.item(row, 0).linked_data.name: row for row in selected_rows}
        receiver_attribute_names = [self.table.item(row, 0).linked_data.name for row in range(self.table.rowCount())]

        for name, row in sender_attribute_names.items():  # remove Rows with existing names
            if name in receiver_attribute_names:
                selected_rows.remove(row)

        for _ in selected_rows:
            self.table.insertRow(drop_row)

        for offset, row_index in enumerate(selected_rows):  # iterate rows
            for col_index in range(self.table.columnCount()):  # iterate columns
                old_item: CustomTableItem
                old_item = sender.item(row_index, col_index)

                if col_index == 0:  # get attribute
                    old_attribute: classes.Attribute = old_item.linked_data
                    new_attribute = copy.copy(old_attribute)
                    self.property_set.add_attribute(new_attribute)
                if old_item:
                    if col_index == 0:
                        new_item = CustomTableItem(new_attribute)
                        new_item.setText(new_attribute.name)
                        if new_attribute.is_child:
                            new_item.setIcon(icons.get_link_icon())
                    else:
                        new_item = QTableWidgetItem(old_item.text())
                    self.table.setItem(offset + drop_row, col_index, new_item)

    def tableDropMimeData(self, row, col, mimeData, action) -> bool:
        self.last_drop_row = row
        return True

    def seperator_text_changed(self, status: str) -> None:
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
        attributes = [self.table.item(row, 0).linked_data for row in selected_rows]

        if self.active_object.ident_attrib in attributes:
            popups.msg_mod_ident()
            return

        delete_request = popups.msg_del_items([attrib.name for attrib in attributes])
        if not delete_request:
            return

        for row in sorted(selected_rows, reverse=True):
            attribute = self.table.item(row, 0).linked_data
            self.widget.table_widget.removeRow(row)
            attribute.delete()

        self.mainWindow.reload()

    def open_menu(self, position: QPointF) -> None:
        menu = QMenu()
        self.action_delete_attribute = menu.addAction("Delete")
        self.action_rename_attribute = menu.addAction("Rename")
        self.action_delete_attribute.triggered.connect(self.delete_selection)
        self.action_rename_attribute.triggered.connect(self.rename_selection)

        selected_rows = get_selected_rows(self.widget.table_widget)
        # add info if logging= debug
        if logging.root.level <= logging.DEBUG and len(selected_rows) == 1:
            self.action_info = menu.addAction("Info")
            self.action_info.triggered.connect(self.info)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def info(self) -> None:
        """print infos of attribute to console (debug only)"""
        row = get_selected_rows(self.widget.table_widget)[0]
        table_item: CustomTableItem = self.widget.table_widget.item(row, 0)
        item = table_item.linked_data
        print(item.name)
        print(f"parent: {item.parent}")

        if item.children:
            print("children:")
            for child in item.children:
                print(f"  {child}")
        else:
            print("no children")

    def rename_selection(self) -> None:
        selected_rows = get_selected_rows(self.table)
        if len(selected_rows) != 1:
            return

        row = selected_rows[0]
        existing_names = [attrib.name for attrib in self.property_set.attributes]
        new_name, fulfilled = popups.req_new_name(self)

        if not fulfilled:
            return

        if new_name in existing_names:
            popups.msg_attribute_already_exists()
            return

        item = self.table.item(row, 0)
        attribute: classes.Attribute = item.item
        attribute.name = new_name
        self.widget.table_widget.item(row, 0).setText(new_name)
        self.mainWindow.reload()

    def data_combo_change(self, text: str) -> None:
        """if datatype changes to xs:double -> only digits are allowed to be entered into line edits"""

        if text == constants.DATATYPE_NUMBER:
            validator = QtGui.QDoubleValidator()
            validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        else:
            validator = QtGui.QRegularExpressionValidator()

        self.line_validator = validator

    def text_changed(self, text: str) -> None:
        """change text of button if name of attribute allready exists"""
        if self.find_attribute_by_name(text) is not None:
            self.widget.button_add.setText("Update")
        else:
            self.widget.button_add.setText("Add")

    def find_attribute_by_name(self, text: str) -> classes.Attribute | None:
        attrib_dict: dict[str, classes.Attribute] = {attrib.name: attrib for attrib in self.property_set.attributes}
        value = attrib_dict.get(text)
        return value

    def add_attribute_button_pressed(self) -> None:

        def get_values() -> list[str] | list[float] | None:
            """return line input values as list"""
            values = list()
            value_type = self.widget.combo_type.currentText()
            data_type = self.widget.combo_data_type.currentText()

            if value_type == constants.RANGE:
                for line in self.input_lines.values():
                    value1 = line[0].text()
                    value2 = line[1].text()
                    if len(value1.strip()) > 0 or len(value2.strip()) > 0:
                        values.append([value1, value2])
            else:
                for line in self.input_lines.values():
                    value = line.text()
                    if len(value.strip()) > 0:
                        values.append(value)

            if data_type == constants.DATATYPE_NUMBER:  # transform text to number
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

        def set_table_line(row: int, attrib: classes.Attribute) -> None:
            table = self.widget.table_widget
            table.setItem(row, 0, CustomTableItem(attrib))
            table.setItem(row, 1, QTableWidgetItem(attrib.data_type))
            table.setItem(row, 2, QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[attrib.value_type]))
            table.setItem(row, 3, QTableWidgetItem(str(attrib.value)))
            table.setItem(row, 4, QTableWidgetItem(str(attrib.revit_name)))

        def update_attribute() -> classes.Attribute | None:

            values = get_values()
            if values is None:
                return None

            if not attribute.is_child:
                attribute.value_type = self.widget.combo_type.currentText()
                attribute.data_type = self.widget.combo_data_type.currentText()
                attribute.child_inherits_values = self.widget.check_box_inherit.isChecked()

            attribute.value = values

            item: QTableWidgetItem = self.widget.table_widget.findItems(attribute.name, Qt.MatchFlag.MatchExactly)[0]
            set_table_line(item.row(), attribute)
            return attribute

        def add_attribute() -> classes.Attribute | None:
            name = self.widget.lineEdit_name.text()

            if not name:
                popups.msg_missing_input()
                return None

            values = get_values()
            if values is None:
                return None

            value_type = self.widget.combo_type.currentText()
            data_type = self.widget.combo_data_type.currentText()

            attrib = classes.Attribute(self.property_set, name, values, value_type, data_type)
            attrib.child_inherits_values = self.widget.check_box_inherit.isChecked()

            rows = self.widget.table_widget.rowCount()
            self.widget.table_widget.setRowCount(rows + 1)
            set_table_line(rows, attrib)

            return attrib

        new_name = self.widget.lineEdit_name.text()
        attribute = self.find_attribute_by_name(new_name)
        if attribute is not None:
            attribute = update_attribute()
        else:
            attribute = add_attribute()

        if attribute is None:
            return

        self.mainWindow.reload()
        self.clear_lines()

    def combo_valuetype_change(self, event: str) -> None:

        if event in constants.RANGE_STRINGS:  # create second column
            for el in self.input_lines:
                self.lineEdit_input2 = LineInput(self)
                el.addWidget(self.lineEdit_input2)
                el.removeWidget(self.widget.button_add_line)
                el.addWidget(self.widget.button_add_line)
                self.input_lines[el] = [self.input_lines[el], self.lineEdit_input2]

        elif self.old_state in constants.RANGE_STRINGS:  # remove second column
            for layout, items in self.input_lines.items():
                layout.removeWidget(items[1])
                items[1].setParent(None)
                self.input_lines[layout] = items[0]

        self.old_state = event

    def new_line(self) -> list[LineInput]:
        def add_column() -> None:
            self.lineEdit_input2 = LineInput(self)
            self.new_layout.addWidget(self.lineEdit_input2)
            self.input_lines[self.new_layout] = [self.lineEdit_input, self.lineEdit_input2]

        self.widget.layout_input.removeWidget(self.widget.button_add_line)
        self.new_layout = QHBoxLayout()
        self.lineEdit_input = LineInput(self)
        self.new_layout.addWidget(self.lineEdit_input)
        self.widget.verticalLayout.insertLayout(0, self.new_layout)

        status = self.widget.combo_type.currentText()
        if status in constants.RANGE_STRINGS:
            add_column()
            line_edit = [self.lineEdit_input, self.lineEdit_input2]

        else:
            self.input_lines[self.new_layout] = self.lineEdit_input
            line_edit = self.lineEdit_input
        self.new_layout.addWidget(self.widget.button_add_line)
        return line_edit

    def clear_lines(self) -> None:

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

    def fill_with_attribute(self, attribute: classes.Attribute) -> None:
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

    def table_clicked(self, table_item: QTableWidgetItem | CustomTableItem) -> None:
        item: CustomTableItem = self.table.item(table_item.row(), 0)
        attribute = item.linked_data
        self.fill_with_attribute(attribute)

    def table_double_clicked(self, table_item: QTableWidgetItem | CustomTableItem | MappingTableItem):
        if not isinstance(table_item, MappingTableItem):
            return
        popups.attribute_mapping(table_item.attribute)
        table_item.update()