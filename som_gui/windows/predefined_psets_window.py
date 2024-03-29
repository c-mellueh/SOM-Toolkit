from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QListWidgetItem
from SOMcreator import classes

from .. import icons
from ..data import constants
from ..qt_designs import ui_predefined_property_sets
from ..windows import popups

from som_gui.core import property_set as property_set_core
from som_gui import tool
if TYPE_CHECKING:
    from ..main_window import MainWindow


class PsetItem(QListWidgetItem):
    _registry = list()

    def __init__(self, property_set: classes.PropertySet = None, project: classes.Project | None = None) -> None:
        super(PsetItem, self).__init__()

        if property_set is None:
            self.property_set = classes.PropertySet(name="NewPset", project=project)
            self.setText(f"NewPset_{self.get_number()}")

        else:
            self.property_set: classes.PropertySet = property_set
            self.setText(property_set.name, False)

        self._registry.append(self)
        self.setFlags(self.flags() | Qt.ItemIsEditable)

    def setText(self, text: str, overwrite: bool = True) -> None:
        super(PsetItem, self).setText(text)
        if overwrite:
            self.property_set.name = text

    def delete(self) -> None:
        self._registry.remove(self)
        self.property_set.delete()

    def get_number(self) -> int:
        if len(self._registry) > 0:
            numbers = [int(re.search("(NewPset_)(\d+)", x.text()).group(2)) for x in self._registry if bool(
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
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.widget.push_button_add_pset.clicked.connect(self.add_pset)
            self.widget.push_button_remove_pset.clicked.connect(self.remove_pset)
            self.widget.push_button_edit.clicked.connect(self.edit_pset)
            self.widget.list_view_pset.itemClicked.connect(self.single_click)
            self.widget.list_view_pset.itemDoubleClicked.connect(self.double_click)
            self.widget.list_view_pset.itemChanged.connect(self.item_changed)

            pass

        super().__init__()

        self.widget = ui_predefined_property_sets.Ui_PsetInherWidget()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle(constants.PREDEFINED_PROPERTY_WINDOW_NAME)
        self.widget.list_view_pset.clear()
        self.widget.list_view_existance.clear()
        self.show()
        self.resize(1000, 400)
        self.main_window = main_window
        connect()

    def edit_pset(self) -> None:
        sel_items = self.widget.list_view_pset.selectedItems()
        if len(sel_items) == 1:
            item = self.widget.list_view_pset.selectedItems()[0]
            property_set_core.open_pset_window(item.property_set, tool.PropertySet, tool.Attribute)

    def add_pset(self):
        item = PsetItem(project=self.main_window.project)
        self.widget.list_view_pset.addItem(item)
        self.widget.list_view_pset.setCurrentItem(item)
        pass

    def remove_pset(self):
        items = self.widget.list_view_pset.selectedItems()
        string_list = [x.property_set.name for x in items]

        delete_request, recursive_deletion = popups.msg_del_items(string_list, item_type=3)

        if delete_request:
            for item in items:
                self.widget.list_view_pset.removeItemWidget(item)
                item.property_set.delete(recursive_deletion)
                item: PsetItem = self.widget.list_view_pset.takeItem(self.widget.list_view_pset.row(item))
                item.delete()
            self.select_first_item()

    def double_click(self, item):
        pass

    def single_click(self, item: PsetItem):
        children = item.property_set.children
        self.widget.list_view_existance.clear()
        for child in children:
            if child.object is not None:
                text = f"{child.object.name} : {child.name}"
            else:
                text = f"{child}: {child.name}"
            item = QListWidgetItem(text)
            self.widget.list_view_existance.addItem(item)

    def select_first_item(self):
        if self.widget.list_view_pset.count() > 0:
            self.single_click(self.widget.list_view_pset.item(0))
            self.widget.list_view_pset.setCurrentRow(0)

    def item_changed(self, item: PsetItem):
        item.property_set.name = item.text()
        self.main_window.reload()

    def showEvent(self, event: QShowEvent) -> None:
        self.widget.list_view_pset.clear()
        for property_set in classes.PropertySet:
            if property_set.object is None:
                item = PsetItem(property_set)
                self.widget.list_view_pset.addItem(item)
                self.widget.list_view_pset.setCurrentItem(item)

    def clear_all(self):
        self.widget.list_view_pset.clear()
        self.widget.list_view_existance.clear()


def open_pset_list(main_window):
    pset_window = PropertySetInherWindow(main_window)
    return pset_window

