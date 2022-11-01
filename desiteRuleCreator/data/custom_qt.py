from __future__ import annotations
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QListWidgetItem, QTableWidgetItem
from SOMcreator import classes


class CustomTree(QTreeWidget):
    def __init__(self, layout) -> None:
        if layout is not None:
            super(CustomTree, self).__init__(layout)
        else:
            super(CustomTree, self).__init__()

    def dropEvent(self, event: QDropEvent) -> None:
        selected_items = self.selectedItems()
        droped_on_item = self.itemFromIndex(self.indexAt(event.pos()))
        if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            super(CustomTree, self).dropEvent(event)
            parent = droped_on_item.object

        else:
            super(CustomTree, self).dropEvent(event)
            parent = droped_on_item.object.parent

        for el in selected_items:
            obj = el.object
            if parent is not None:
                obj.parent = parent
            else:
                obj.parent = None


class CustomPsetTree(QTreeWidget):
    def __init__(self) -> None:
        super(CustomPsetTree, self).__init__()
        self.setExpandsOnDoubleClick(False)
        self.setColumnCount(1)
        self.setHeaderLabels(["Name"])


class CustomObjectTreeItem(QTreeWidgetItem):
    def __init__(self,obj: classes.Object,func = None) -> None:
        super(CustomObjectTreeItem, self).__init__()
        self._object = obj
        self._func = func
        self.update()


    def addChild(self, child: CustomObjectTreeItem) -> None:
        super(CustomObjectTreeItem, self).addChild(child)
        if child.object not in self.object.children:
            self.object.add_child(child.object)

    @property
    def object(self) -> classes.Object:
        return self._object

    def update(self) -> None:
        self.setText(0, self.object.name)
        if self._func is not None:
            self._func(self.object)
            return
        if self.object.is_concept:
            self.setText(1, "")
        else:
            self.setText(1, str(self.object.ident_attrib.value))



class CustomPSetTreeItem(QTreeWidgetItem):
    def __init__(self, tree: QTreeWidget, pset: classes.PropertySet) -> None:
        super(CustomPSetTreeItem, self).__init__(tree)
        self._property_set = pset
        self.update()

    @property
    def property_set(self) -> classes.PropertySet:
        return self._property_set

    def update(self) -> None:
        self.setText(0, self.property_set.name)


class CustomAttribTreeItem(QTreeWidgetItem):
    def __init__(self, tree: QTreeWidget, attribute: classes.Attribute) -> None:
        super(CustomAttribTreeItem, self).__init__(tree)
        self._attribute = attribute
        self.update()

    @property
    def attribute(self) -> classes.Attribute:
        return self._attribute

    def update(self) -> None:
        self.setText(0, self.attribute.name)


class CustomListItem(QListWidgetItem):
    def __init__(self, data: classes.PropertySet | classes.Object | classes.Attribute) -> None:
        super(CustomListItem, self).__init__()
        self._linked_data = data
        self.setText(data.name)

    @property
    def linked_data(self) -> classes.PropertySet | classes.Object | classes.Attribute:
        return self._linked_data

    def update(self) -> None:
        self.setText(self.linked_data.name)


class CustomTableItem(QTableWidgetItem):
    def __init__(self, item: classes.Object | classes.PropertySet | classes.Attribute):
        super(CustomTableItem, self).__init__()
        self.linked_data = item
        self.setText(item.name)

