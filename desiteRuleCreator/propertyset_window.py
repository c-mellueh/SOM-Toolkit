from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize,QModelIndex,Qt
from PySide6.QtWidgets import QTableWidgetItem, QHBoxLayout, QLineEdit,QPushButton,QSizePolicy,QMessageBox, QMenu
from .QtDesigns.ui_widget import Ui_layout_main
from .classes import PropertySet,Attribute
from . import constants

def make_string_printable(value):
    value = str(value).replace(".",",")
    return value

def string_to_float(value:str):
    value = float(value.replace(",","."))

    return value

class PropertySetWindow(QtWidgets.QWidget):
    def __init__(self,property_set:PropertySet):
        super(PropertySetWindow, self).__init__()
        self.widget = Ui_layout_main()
        self.widget.setupUi(self)
        self.property_set = property_set
        self.widget.table_widget.data_dict = dict()
        self.fill_table()
        self.setWindowTitle(f"{property_set.object.name}:{property_set.name}")
        self.widget.button_add_line.clicked.connect(self.new_line)
        self.input_lines = {self.widget.layout_input:self.widget.lineEdit_input}
        self.widget.table_widget.itemDoubleClicked.connect(self.list_clicked)
        self.widget.combo_type.currentTextChanged.connect(self.combo_change)
        self.old_state = self.widget.combo_type.currentText()
        self.widget.lineEdit_name.textChanged.connect(self.text_changed)
        self.widget.combo_data_type.currentTextChanged.connect(self.data_combo_change)

        #Buttons
        self.widget.button_add.clicked.connect(self.add_button_pressed)
        self.widget.button_delete.clicked.connect(self.delete_attribute)

        self.widget.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.table_widget.customContextMenuRequested.connect(self.openMenu)
        icon = QtGui.QIcon(constants.ICON_PATH)
        self.setWindowIcon(icon)
        self.show()
        self.resize(1000,400)
    def delete_selection(self):
        selected_items = self.widget.table_widget.selectedItems()
        selected_rows = []
        for items in selected_items:
            row = items.row()
            if row not in selected_rows:
                name = attribute = self.widget.table_widget.item(row,0).text()
                if self.get_attribute_by_name(name) == self.property_set.object.identifier:
                    msgBox = QMessageBox()
                    msgBox.setText("Identifier can't be deleted!")
                    msgBox.setWindowTitle(" ")
                    msgBox.setIcon(QMessageBox.Icon.Warning)
                    msgBox.exec()
                    return
                else:
                    selected_rows.append(items.row())

        selected_rows.sort(reverse=True)

        for row in selected_rows:
            name = self.widget.table_widget.item(row,0).text()
            self.widget.table_widget.removeRow(row)
            attribute = self.get_attribute_by_name(name)
            attribute.delete()

        pass



    def openMenu(self,position):
        menu = QMenu()
        self.action_delete_objects = menu.addAction("Delete")
        self.action_delete_objects.triggered.connect(self.delete_selection)

        menu.exec(self.widget.table_widget.viewport().mapToGlobal(position))

    def get_attribute_by_name(self,name):
        for attribute in self.property_set.attributes:
            if attribute.name == name:
                return attribute
        return False

    def delete_attribute(self):
        already_exists = False

        attribute = self.get_attribute_by_name(self.widget.lineEdit_name.text())
        if attribute:
            attribute.delete()
            row = self.widget.table_widget.findItems(attribute.name,Qt.MatchFlag.MatchExactly)[0].row()
            self.widget.table_widget.removeRow(row)

        self.clear_lines()

    def data_combo_change(self,text):
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

    def text_changed(self,text):
        name_match = len([x for x in self.property_set.attributes if x.name == text])>0
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

        def add_table_line(row, attribute:Attribute):
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
                    if len(value.strip())>0:
                        values.append(value)
            else:
                for line in self.input_lines.values():
                    value1 = line[0].text()
                    value2 = line[1].text()
                    if len(value1.strip())> 0 or len(value2.strip())>0:
                        values.append([value1,value2])

            if data_type == constants.DATATYPE_NUMBER:
                for i,value in enumerate(values):
                    try:
                        if self.widget.combo_type.currentText() == constants.RANGE:
                            values[i] = [string_to_float(value[0]),string_to_float(value[1])]
                        else:
                            values[i] = string_to_float(value)
                    except ValueError:
                        msgBox = QMessageBox()
                        msgBox.setText("Value can't be converted to Double!")
                        msgBox.setWindowTitle(" ")
                        msgBox.setIcon(QMessageBox.Icon.Warning)
                        msgBox.exec()
            return values

        def update_attribute(attribute:Attribute):

            attribute.value_type = self.widget.combo_type.currentText()
            attribute.data_type = self.widget.combo_data_type.currentText()
            values = get_values()
            attribute.value = values

            item: QTableWidgetItem = self.widget.table_widget.findItems(attribute.name,Qt.MatchFlag.MatchExactly)[0]
            row = item.row()
            fill_table_line(row,attribute)

        def add_attribute():
            name = self.widget.lineEdit_name.text()
            values = get_values()
            value_type = self.widget.combo_type.currentText()
            data_type = self.widget.combo_data_type.currentText()

            attribute = Attribute(self.property_set,name,values,value_type,data_type)
            self.property_set.object.add_attribute(attribute)
            rows = self.widget.table_widget.rowCount()+1
            self.widget.table_widget.setRowCount(rows)
            add_table_line(rows-1,attribute)


        already_exists = False
        for attribute in self.property_set.attributes:
            if attribute.name == self.widget.lineEdit_name.text():
                update_attribute(attribute)
                already_exists = True

        if not already_exists and self.widget.lineEdit_name.text():
            add_attribute()

        self.clear_lines()


    def combo_change(self,event):
        if event in constants.RANGE_STRINGS:
            for el in self.input_lines:
                self.lineEdit_input2 = QLineEdit(self)
                el.addWidget(self.lineEdit_input2)
                el.removeWidget(self.widget.button_add_line)
                el.addWidget(self.widget.button_add_line)
                self.input_lines[el] = [self.input_lines[el],self.lineEdit_input2]

        elif self.old_state in constants.RANGE_STRINGS:
            for layout,items in self.input_lines.items():
                layout.removeWidget(items[1])
                items[1].setParent(None)
                self.input_lines[layout]= items[0]

        self.old_state = event



    def fill_table(self):
        table = self.widget.table_widget
        table.setRowCount(len(self.property_set.attributes))

        for i,value in enumerate(self.property_set.attributes):
            value:Attribute = value


            table.setItem(i,0,QTableWidgetItem(value.name))
            table.setItem(i,1,QTableWidgetItem(value.data_type))
            table.setItem(i,2,QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[value.value_type]))
            table.setItem(i,3,QTableWidgetItem(str(value.value)))
            if value == self.property_set.object.identifier:
                print(value.name)
                brush = QtGui.QBrush()
                brush.setColor(Qt.GlobalColor.lightGray)
                brush.setStyle(Qt.BrushStyle.SolidPattern)
                print(brush)
                for k in range (4):
                    item = table.item(i,k)
                    item.setBackground(brush)
                    print(item.text())

            table.resizeColumnsToContents()
            table.data_dict[value.name]=value

    def new_line(self):
        self.widget.layout_input.removeWidget(self.widget.button_add_line)
        self.new_layout = QHBoxLayout(self)
        self.lineEdit_input = QLineEdit(self)
        self.new_layout.addWidget(self.lineEdit_input)

        self.widget.verticalLayout.insertLayout(0,self.new_layout)

        status = self.widget.combo_type.currentText()
        if status in constants.RANGE_STRINGS:
            self.range_mode()
            line_edit = [self.lineEdit_input,self.lineEdit_input2]

        else:
            self.input_lines[self.new_layout] = self.lineEdit_input
            line_edit = self.lineEdit_input
        self.new_layout.addWidget(self.widget.button_add_line)
        return line_edit

    def range_mode(self):

        self.lineEdit_input2 = QLineEdit(self)
        self.new_layout.addWidget(self.lineEdit_input2)
        self.input_lines[self.new_layout] =[self.lineEdit_input,self.lineEdit_input2]

    def clear_lines(self):

        for key,item in tuple(self.input_lines.items()):

            if key != self.widget.layout_input:
                v_layout:QHBoxLayout = key.parent()
                v_layout.removeItem(key)
                key.setParent(None)
                if isinstance(item,list):
                    for i in item:
                        v_layout.removeWidget(i)
                        i.setParent(None)
                else:
                    v_layout.removeWidget(item)
                    item.setParent(None)
                del self.input_lines[key]

        self.widget.lineEdit_name.setText("")
        for items in self.input_lines.values():
            if isinstance(items,list):
                for item in items:
                    item.setText("")
            else:
                items.setText("")
        self.widget.layout_input.addWidget(self.widget.button_add_line)



    def list_clicked(self,event:QModelIndex):

        item:QTableWidgetItem = self.widget.table_widget.item(event.row(),0)
        attribute:Attribute= self.widget.table_widget.data_dict[item.text()]

        if attribute != self.property_set.object.identifier:

            index = self.widget.combo_type.findText(attribute.value_type)
            self.widget.combo_type.setCurrentIndex(index)
            index = self.widget.combo_data_type.findText(attribute.data_type)
            self.widget.combo_data_type.setCurrentIndex(index)
            self.clear_lines()

            for i,value in enumerate(attribute.value):
                if i ==0:
                    lines = self.input_lines[self.widget.layout_input]
                else:
                    lines = self.new_line()
                if attribute.value_type == constants.RANGE:
                    for i,val in enumerate(value):
                        lines[i].setText(make_string_printable(val))
                else:
                    lines.setText(make_string_printable(value))

            self.widget.lineEdit_name.setText(attribute.name)