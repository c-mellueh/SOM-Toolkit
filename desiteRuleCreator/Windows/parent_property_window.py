import re
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent,QIcon
from PySide6.QtWidgets import QWidget, QListWidgetItem

from desiteRuleCreator.QtDesigns import ui_PsetInheritance
from desiteRuleCreator.data import classes,constants
from desiteRuleCreator import icons
from desiteRuleCreator.Windows import popups

class PsetItem(QListWidgetItem):
    iter = list()

    def __init__(self, property_set=None):
        super(PsetItem, self).__init__()

        if property_set is None:
            self.property_set = classes.PropertySet(name="NewPset")
            self.setText(f"NewPset_{self.get_number()}")

        else:
            self.property_set = property_set
            self.setText(property_set.name)
        self.iter.append(self)
        self.setFlags(self.flags() | Qt.ItemIsEditable)

    def setText(self, text: str) -> None:
        super(PsetItem, self).setText(text)
        self.property_set.name = text

    def delete(self):
        self.iter.remove(self)

    def get_number(self):
        if len(self.iter) > 0:
            numbers = [int(re.search("(NewPset_)(\d+)", x.text()).group(2)) for x in self.iter if bool(
                re.search("NewPset_(\d+)", x.text()))]  # find all texts matching the Format and return their numbers
            numbers.sort()
            if len(numbers) > 0:
                highest_number = numbers[-1]
                new_number = highest_number + 1
                return new_number
            else:
                return 1
        else:
            return 1


class PropertySetInherWindow(QWidget):
    def __init__(self, main_window):
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
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle(constants.PREDEFINED_PROPERTY_WINDOW_NAME)
        self.widget.list_view_pset.clear()
        self.widget.list_view_existance.clear()
        self.show()
        self.resize(1000, 400)
        self.mainWindow = main_window
        connect()

    def edit_pset(self):
        sel_items = self.widget.list_view_pset.selectedItems()
        if len(sel_items) == 1:
            item = self.widget.list_view_pset.selectedItems()[0]
            self.mainWindow.pset_window = self.mainWindow.open_pset_window(item.property_set, None,
                                                                           item.property_set.name)

    def add_pset(self):
        item = PsetItem()
        self.widget.list_view_pset.addItem(item)
        self.widget.list_view_pset.setCurrentItem(item)
        self.mainWindow.update_completer()
        pass

    def remove_pset(self):
        items = self.widget.list_view_pset.selectedItems()
        string_list = [x.property_set.name for x in items]

        delete_request = popups.msg_del_items(string_list)

        if delete_request:
            for item in items:
                self.widget.list_view_pset.removeItemWidget(item)
                item.property_set.delete()
                item: PsetItem = self.widget.list_view_pset.takeItem(self.widget.list_view_pset.row(item))
                item.delete()
            self.select_first_item()

    def double_click(self, item):
        pass

    def single_click(self, item: PsetItem):
        children = item.property_set.children
        self.widget.list_view_existance.clear()
        for child in children:
            text = f"{child.object.name} : {child.name}"
            item = QListWidgetItem(text)
            self.widget.list_view_existance.addItem(item)

    def select_first_item(self):
        if self.widget.list_view_pset.count() > 0:
            self.single_click(self.widget.list_view_pset.item(0))
            self.widget.list_view_pset.setCurrentRow(0)

    def item_changed(self, item: PsetItem):
        item.property_set.name = item.text()
        self.mainWindow.update_completer()
        self.mainWindow.reload()

    def showEvent(self, event: QShowEvent) -> None:
        self.widget.list_view_pset.clear()
        for property_set in classes.PropertySet.iter:
            if property_set.object is None:
                item = PsetItem(property_set)
                self.widget.list_view_pset.addItem(item)
                # self.mainWindow.update_completer()
                self.widget.list_view_pset.setCurrentItem(item)

    def clear_all(self):
        self.widget.list_view_pset.clear()
        self.widget.list_view_existance.clear()


def open_pset_list(main_window):
    pset_window = PropertySetInherWindow(main_window)
    return pset_window


def reload(main_window):
    window: PropertySetInherWindow = main_window.parent_property_window
    widget = window.widget
    window.single_click(widget.list_view_pset.selectedItems()[0])
