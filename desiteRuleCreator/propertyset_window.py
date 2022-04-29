from PySide6 import QtWidgets
from PySide6.QtWidgets import QTableWidgetItem
from QtDesigns.ui_widget import Ui_layout_main
from classes import PropertySet,Attribute
import constants

class PropertySetWindow(QtWidgets.QWidget):
    def __init__(self,property_set:PropertySet):
        super(PropertySetWindow, self).__init__()
        self.widget = Ui_layout_main()
        self.widget.setupUi(self)
        self.show()
        self.property_set = property_set
        self.fill_table()
        self.setWindowTitle(f"{property_set.object.name}:{property_set.name}")


    def fill_table(self):
        table = self.widget.table_widget
        table.setRowCount(len(self.property_set.attributes))

        for i,value in enumerate(self.property_set.attributes):
            value:Attribute = value
            table.setItem(i,0,QTableWidgetItem(value.name))
            table.setItem(i,1,QTableWidgetItem(value.data_type))
            table.setItem(i,2,QTableWidgetItem(constants.VALUE_TYPE_LOOKUP[value.value_type]))
            table.setItem(i,3,QTableWidgetItem(str(value.value)))
            table.resizeColumnsToContents()
