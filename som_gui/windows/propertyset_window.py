from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QMenu, QTableWidgetItem, QTableWidget
from SOMcreator import classes
from SOMcreator import constants as som_cr_constants

from .. import icons, settings
from ..data import constants as constants
from ..qt_designs import ui_property_set_window
from ..widgets import property_widget
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow


class CustomTableItem(QTableWidgetItem):
    def __init__(self, item: classes.Object | classes.PropertySet | classes.Attribute, text: str):
        super(CustomTableItem, self).__init__()
        self.linked_data = item
        self.setText(text)

    def update(self):
        pass


class CustomCheckItem(QTableWidgetItem):
    def __init__(self, linked_item: classes.PropertySet | classes.Attribute):
        super(CustomCheckItem, self).__init__()
        if linked_item.optional:
            self.setCheckState(Qt.CheckState.Checked)
        else:
            self.setCheckState(Qt.CheckState.Unchecked)
        self.linked_item = linked_item

    def update(self):
        check_state = self.checkState()
        if check_state == Qt.CheckState.Checked:
            check_bool = True
        elif check_state == Qt.CheckState.Unchecked:
            check_bool = False
        elif check_state == Qt.CheckState.PartiallyChecked:
            logging.error("Partially Checking not Allowed")
            check_bool = True
        else:
            check_bool = True
        self.linked_item.optional = check_bool


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


def set_table_line(table, row: int, attrib: classes.Attribute) -> None:
    name_item = CustomTableItem(attrib, attrib.name)
    if attrib.value_type == som_cr_constants.RANGE:
        value_text = ";".join("-".join((str(x) for x in ran)) for ran in attrib.value)
    else:
        value_text = ";".join(str(x) for x in attrib.value)

    table.setItem(row, 0, name_item)
    table.setItem(row, 1, CustomTableItem(attrib, attrib.data_type))
    table.setItem(row, 2, CustomTableItem(attrib, constants.VALUE_TYPE_LOOKUP[attrib.value_type]))
    table.setItem(row, 3, CustomTableItem(attrib, value_text))
    table.setItem(row, 4, CustomCheckItem(attrib))
    if attrib.is_child:
        link_item = icons.get_link_icon()
        name_item.setIcon(link_item)


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

    icons.get_link_icon()

    table_widget.setRowCount(len(property_set.attributes))

    for i, attribute in enumerate(property_set.attributes):
        CustomTableItem(attribute, attribute.name)

        set_table_line(table_widget, i, attribute)
        if active_object is None:
            continue
        if attribute == active_object.ident_attrib:
            reformat_identifier(i)

    table_widget.resizeColumnsToContents()


class LineInput(QLineEdit):
    def __init__(self, parent: PropertySetWindow) -> None:
        super(LineInput, self).__init__(parent)
        self.pset_window = parent
        self.setValidator(self.pset_window.line_validator)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        seperator = settings.get_seperator()
        sep_bool = settings.get_seperator_status()
        if event.matches(QtGui.QKeySequence.Paste) and sep_bool:
            text = QtGui.QGuiApplication.clipboard().text()
            text_list = text.split(seperator)
            if len(text_list) < 2:
                super(LineInput, self).keyPressEvent(event)
                return

            dif = len(text_list) - len(self.pset_window.input_lines2)
            if dif >= 0:
                for i in range(dif + 1):
                    self.pset_window.new_line()
            for i, text, lines in enumerate(zip(text_list, self.pset_window.input_lines2.values())):
                text = text.strip()
                line: LineInput = lines[0]
                line.setText(text)

        else:
            super(LineInput, self).keyPressEvent(event)


class PropertySetWindow(QtWidgets.QWidget):
    def __init__(self, main_window: MainWindow, property_set: classes.PropertySet, active_object: classes.Object,
                 window_title: str):
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
            self.widget.description.textChanged.connect(self.decription_changed)

        super(PropertySetWindow, self).__init__()
        self.widget = ui_property_set_window.Ui_layout_main()
        self.widget.setupUi(self)

        self.mainWindow = main_window
        self.property_set = property_set
        self.active_object = active_object
        self.old_state = self.widget.combo_type.currentText()
        self._line_validator = QtGui.QRegularExpressionValidator()
        self.table: QTableWidget = self.widget.table_widget

        self.setWindowTitle(window_title)
        self.setWindowIcon(icons.get_icon())
        fill_attribute_table(self.active_object, self.widget.table_widget, self.property_set)
        seperator_status = settings.get_seperator_status()
        seperator = settings.get_seperator()
        self.widget.check_box_seperator.setChecked(seperator_status)
        self.widget.line_edit_seperator.setText(seperator)
        self.widget.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.table_widget.orig_drop_event = self.widget.table_widget.dropEvent
        self.widget.table_widget.dropEvent = self.tableDropEvent
        self.widget.table_widget.dropMimeData = self.tableDropMimeData

        # Fillst combo_Data_type with own Values
        for i in reversed(range(self.widget.combo_data_type.count())):
            self.widget.combo_data_type.removeItem(i)

        self.widget.combo_data_type.addItems(list(constants.DATA_TYPES))
        self.show()
        self.resize(1000, 400)

        self._description_changed = False

        self.horizontal_layout_list: list[QHBoxLayout] = list()
        self.line_edit_list: list[LineInput] = list()
        self.active_line_edit: LineInput | None = None
        connect_items()
        self.new_line()

    @property
    def input_lines2(self) -> dict[QHBoxLayout, list[LineInput]]:
        line_dict = dict()
        for layout in self.horizontal_layout_list:
            line_dict[layout] = list()
            for index in range(layout.count()):
                line_dict[layout].append(layout.itemAt(index).widget())
        return line_dict

    def item_changed(self, item: CustomCheckItem):
        item.update()

    @property
    def line_validator(self) -> QtGui.QValidator:
        return self._line_validator

    @line_validator.setter
    def line_validator(self, value: QtGui.QValidator) -> None:
        self._line_validator = value
        for line_list in self.input_lines2.values():
            for line in line_list:
                line.setValidator(value)

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
                        new_item = CustomTableItem(new_attribute, new_attribute.name)
                        if new_attribute.is_child:
                            new_item.setIcon(icons.get_link_icon())
                    else:
                        new_item = QTableWidgetItem(old_item.text())
                    self.table.setItem(offset + drop_row, col_index, new_item)

    def tableDropMimeData(self, row, col, mimeData, action) -> bool:
        self.last_drop_row = row
        return True

    def seperator_text_changed(self, status: str) -> None:
        settings.set_seperator(status)

    def seperator_status_changed(self, status: int) -> None:
        if status == 2:
            b = True
        else:
            b = False
        settings.set_seperator_status(b)
        self.widget.line_edit_seperator.setEnabled(b)

    def delete_selection(self) -> None:
        """delete selected Table items"""

        selected_rows = get_selected_rows(self.table)
        attributes: list[classes.Attribute] = [self.table.item(row, 0).linked_data for row in selected_rows]
        if self.active_object is not None:

            if self.active_object.ident_attrib in attributes:
                popups.msg_mod_ident()
                return

        delete_request = popups.msg_del_items([attrib.name for attrib in attributes], item_type=4)
        if not delete_request:
            return

        for row in sorted(selected_rows, reverse=True):
            attribute: classes.Attribute = self.table.item(row, 0).linked_data
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
        print(f"property_set: {item.property_set}")
        print(f"in pset: {item in self.property_set.attributes}")
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
        item: CustomTableItem = self.table.item(row, 0)
        attribute: classes.Attribute = item.linked_data
        old_name = attribute.name
        existing_names = [attrib.name for attrib in self.property_set.attributes]
        new_name, fulfilled = popups.req_attribute_name(self, old_name)

        if not fulfilled:
            return

        if new_name == old_name:
            return

        if new_name in existing_names:
            popups.msg_attribute_already_exists()
            return

        attribute.name = new_name
        self.widget.table_widget.item(row, 0).setText(new_name)
        self.mainWindow.reload()

    def data_combo_change(self, text: str) -> None:
        """if datatype changes to xs:double -> only digits are allowed to be entered into line edits"""

        if text == som_cr_constants.DATATYPE_NUMBER:
            validator = QtGui.QDoubleValidator()
            validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        else:
            validator = QtGui.QRegularExpressionValidator()

        self.line_validator = validator
        self.update_tab_order()

    def enable_menus(self, status: bool):
        self.widget.combo_type.setEnabled(status)
        self.widget.combo_data_type.setEnabled(status)
        self.widget.check_box_inherit.setEnabled(status)

    def text_changed(self, text: str) -> None:
        """change text of button if name of attribute allready exists"""
        attribute = self.find_attribute_by_name(text)
        status = True
        if attribute is not None:
            self.widget.button_add.setText("Update")
            if attribute.is_child:
                status = False
        else:
            self.widget.button_add.setText("Add")
        self.enable_menus(status)

    def find_attribute_by_name(self, text: str) -> classes.Attribute | None:
        attrib_dict: dict[str, classes.Attribute] = {attrib.name: attrib for attrib in self.property_set.attributes}
        value = attrib_dict.get(text)
        return value

    def add_attribute_button_pressed(self) -> None:

        def get_values() -> list[str] | list[float] | None:
            """return line input values as list"""
            values = list()

            if value_type in constants.RANGE_STRINGS:
                for lines in self.input_lines2.values():
                    value1 = lines[0].text()
                    value2 = lines[1].text()
                    if len(value1.strip()) > 0 or len(value2.strip()) > 0:
                        values.append([value1, value2])
            else:
                for lines in self.input_lines2.values():
                    for line in lines:
                        value = line.text()
                        if len(value.strip()) > 0:
                            values.append(value)

            if data_type == som_cr_constants.DATATYPE_NUMBER:  # transform text to number
                for i, value in enumerate(values):
                    try:
                        if self.widget.combo_type.currentText() in constants.RANGE_STRINGS:
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

        def update_attribute() -> classes.Attribute | None:

            values = get_values()
            if values is None:
                return None

            if not attribute.is_child:
                attribute.value_type = value_type
                attribute.data_type = data_type
                attribute.child_inherits_values = self.widget.check_box_inherit.isChecked()

            description = self.widget.description.toPlainText()
            if self._description_changed:  # override description only if description was changed (usefull if description is inherited from parent)
                attribute.description = description
            attribute.value = values

            item: QTableWidgetItem = self.widget.table_widget.findItems(attribute.name, Qt.MatchFlag.MatchExactly)[0]
            set_table_line(self.table, item.row(), attribute)
            return attribute

        def create_attribute() -> classes.Attribute | None:
            name = self.widget.lineEdit_name.text()

            if not name:
                popups.msg_missing_input()
                return None

            values = get_values()
            if values is None:
                return None

            description = self.widget.description.toPlainText()
            attrib = classes.Attribute(property_set=self.property_set, name=name, value=values, value_type=value_type,
                                       data_type=data_type, description=description)
            attrib.child_inherits_values = self.widget.check_box_inherit.isChecked()

            rows = self.widget.table_widget.rowCount()
            self.widget.table_widget.setRowCount(rows + 1)
            set_table_line(self.table, rows, attrib)

            return attrib

        value_type = constants.VALUE_TYPE_LOOKUP[self.widget.combo_type.currentText()]
        data_type = self.widget.combo_data_type.currentText()
        new_name = self.widget.lineEdit_name.text()
        attribute = self.find_attribute_by_name(new_name)

        if attribute is not None:
            attribute = update_attribute()
        else:
            attribute = create_attribute()

        if attribute is None:
            return

        property_widget.reload(self.mainWindow)
        self.clear_lines()

    def split_input_lines(self):
        for layout in self.input_lines2.keys():
            layout.addWidget(LineInput(self))

    def remove_input_split(self):
        for layout, lines in self.input_lines2.items():
            combi_text = "".join([line.text() for line in lines])
            layout.removeWidget(lines[1])
            lines[1].deleteLater()
            lines[0].setText(combi_text)

    def combo_valuetype_change(self, event: str) -> None:
        if event in constants.RANGE_STRINGS:  # create second column
            self.split_input_lines()

        elif self.old_state in constants.RANGE_STRINGS:  # remove second column
            self.remove_input_split()

        self.old_state = event
        self.update_tab_order()

    def update_tab_order(self):
        last_line = None
        for layout in self.horizontal_layout_list:
            lines = self.input_lines2[layout]
            for line in lines:
                if last_line is not None:
                    self.setTabOrder(last_line, line)
                last_line = line

    def new_line(self) -> list[LineInput]:

        status = self.widget.combo_type.currentText()
        layout = QHBoxLayout()
        self.widget.verticalLayout.addLayout(layout)
        self.horizontal_layout_list.append(layout)

        if status in constants.RANGE_STRINGS:
            self.active_line_edit = LineInput(self)
            self.line_edit_list.append(self.active_line_edit)
            layout.addWidget(self.active_line_edit)
        self.active_line_edit = LineInput(self)
        self.line_edit_list.append(self.active_line_edit)
        layout.addWidget(self.active_line_edit)
        self.update_tab_order()
        return [layout.itemAt(index).widget() for index in range(layout.count())]

    def clear_lines(self) -> None:
        for layout, lines in self.input_lines2.items():
            for line in lines:
                line.deleteLater()
            layout.deleteLater()
        self.widget.description.clear()
        self._description_changed = False
        self.horizontal_layout_list = list()
        self.new_line()
        self.update_tab_order()

    def fill_with_attribute(self, attribute: classes.Attribute) -> None:
        eng_type = constants.VALUE_TYPE_LOOKUP[attribute.value_type]
        index = self.widget.combo_type.findText(constants.GER_TYPES_LOOKUP[eng_type])
        self.widget.combo_type.setCurrentIndex(index)

        index = self.widget.combo_data_type.findText(attribute.data_type)
        self.widget.combo_data_type.setCurrentIndex(index)

        self.clear_lines()

        # Add Values
        for _ in range(len(attribute.value) - 1):
            self.new_line()

        for attribute_value, lines in zip(attribute.value, self.input_lines2.values()):
            if len(lines) > 1:
                for k, val in enumerate(attribute_value):
                    if attribute.data_type == som_cr_constants.XS_DOUBLE:
                        lines[k].setText(float_to_string(val))
                    else:
                        lines[k].setText(val)
            else:
                line = lines[0]
                if attribute.data_type == som_cr_constants.XS_DOUBLE:
                    line.setText(float_to_string(attribute_value))
                else:
                    line.setText(attribute_value)
        # input Name
        self.widget.lineEdit_name.setText(attribute.name)

        # set Editable
        self.widget.check_box_inherit.setChecked(attribute.child_inherits_values)

        self.widget.description.setText(attribute.description)
        self._description_changed = False
        self.update_tab_order()

    def table_clicked(self, table_item: QTableWidgetItem | CustomTableItem | None, attribute=None) -> None:
        if attribute is None:
            self.item_changed(table_item)
            item: CustomTableItem = self.table.item(table_item.row(), 0)
            attribute = item.linked_data
        if attribute.is_child:
            status = False
            self.widget.combo_type.setToolTip("Attribut wurde geerbt -> Keine Änderung des Types möglich")
            self.widget.combo_data_type.setToolTip("Attribut wurde geerbt -> Keine Änderung des Datentyps möglich")
        else:
            status = True
            self.widget.combo_type.setToolTip("")
            self.widget.combo_data_type.setToolTip("")
        self.enable_menus(status)
        self.fill_with_attribute(attribute)

    def table_double_clicked(self, table_item: QTableWidgetItem | CustomTableItem | MappingTableItem):
        if not isinstance(table_item, MappingTableItem):
            return
        popups.attribute_mapping(table_item.attribute)
        table_item.update()

    def decription_changed(self):
        """if description is changed self._description_changed will be set to True
        -> to override Parent description"""
        self._description_changed = True
