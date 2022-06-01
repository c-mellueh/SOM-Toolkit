from . import classes
from .QtDesigns import ui_PsetInheritance
from PySide6.QtWidgets import QWidget,QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
import re
class PsetItem(QListWidgetItem):
    iter = list()
    def __init__(self):
        super(PsetItem, self).__init__()

        self.property_set = classes.PropertySet(name = "NewPset")
        self.setText(f"NewPset_{self.get_number()}")
        self.iter.append(self)
        self.setFlags(self.flags()|Qt.ItemIsEditable)
        self.get_number()
    def setText(self, text:str) -> None:
        super(PsetItem, self).setText(text)
        self.property_set.name = text

    def delete(self):
        self.iter.remove(self)

    def get_number(self):
        if len(self.iter) >0:
            numbers = [int(re.search("(NewPset_)(\d+)",x.text()).group(2)) for x in self.iter if bool(re.search("NewPset_(\d+)",x.text()))] # find all texts matching the Format and return their numbers
            numbers.sort()
            highest_number = numbers[-1]
            new_number = highest_number+1
            return new_number
        else:
            return 1
class PropertySetInherWindow(QWidget):
    def __init__(self,mainWindow):
        def connect():
            self.widget.push_button_add_pset.clicked.connect(self.add_pset)
            self.widget.push_button_remove_pset.clicked.connect(self.remove_pset)
            self.widget.push_button_edit.clicked.connect(self.edit_pset)
            self.widget.list_view_pset.itemClicked.connect(self.single_click)
            self.widget.list_view_pset.itemDoubleClicked.connect(self.double_click)
            self.widget.list_view_pset.itemChanged.connect(self.item_changed)

            pass

        super().__init__()
        self.widget = ui_PsetInheritance.Ui_PsetInherWidget()
        self.widget.setupUi(self)
        self.widget.list_view_pset.clear()
        self.widget.list_view_existance.clear()
        self.show()
        self.resize(1000, 400)
        self.mainWindow = mainWindow
        connect()


    def edit_pset(self):
        sel_items = self.widget.list_view_pset.selectedItems()
        if len(sel_items) == 1:
            item = self.widget.list_view_pset.selectedItems()[0]
            self.mainWindow.pset_window = self.mainWindow.openPsetWindow(item.property_set,None,item.property_set.name)

    def add_pset(self):
        item = PsetItem()
        self.widget.list_view_pset.addItem(item)
        self.mainWindow.update_completer()
        self.widget.list_view_pset.setCurrentItem(item)
        pass

    def remove_pset(self):
        items = self.widget.list_view_pset.selectedItems()
        for item in items:
            self.widget.list_view_pset.removeItemWidget(item)
            item.property_set.delete()
            item.setHidden(True)
            item.delete()
        pass

    def double_click(self,item):
        pass

    def single_click(self,item:PsetItem):
        children = item.property_set.children
        self.widget.list_view_existance.clear()
        for child in children:
            text = f"{child.object.name} : {child.name}"
            item = QListWidgetItem(text)
            self.widget.list_view_existance.addItem(item)

    def item_changed(self,item:PsetItem):
        item.property_set.name = item.text()

    def showEvent(self, event:QShowEvent) -> None:
        if self.widget.list_view_pset.count()>0:
            self.single_click(self.widget.list_view_pset.item(0))
            self.widget.list_view_pset.setCurrentRow(0)
def open_pset_list(mainWindow):
    pset_window = PropertySetInherWindow(mainWindow)
    return pset_window