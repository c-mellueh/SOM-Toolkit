from __future__ import annotations

import copy
from typing import Iterator, Type,TYPE_CHECKING
from uuid import uuid4

from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QListWidgetItem,QTableWidgetItem

if TYPE_CHECKING:
    from desiteRuleCreator.Windows import graphs_window
    from desiteRuleCreator.main_window import MainWindow


# Add child to Parent leads to reverse

class IterRegistry(type):
    _registry = list()
    """ Helper for Iteration"""

    def __iter__(self) -> Iterator:
        return iter(self._registry)

    def __len__(self) -> int:
        return len(self._registry)


class Project(object):
    def __init__(self, main_window:MainWindow, name: str, author: str = None) -> None:
        self._name = ""
        self._author = author
        self._version = "1.0.0"
        self._changed = True
        self.main_window = main_window
        self.name = name

    @property
    def changed(self) -> bool:
        def check_data():
            for obj in Object:
                if obj.changed:
                    return True
            return False

        data = check_data()
        if data or self._changed:
            self._changed = True
        else:
            self._changed = False

        return self._changed

    @changed.setter
    def changed(self, value: bool) -> None:
        self._changed = value

    def reset_changed(self) -> None:
        for obj in Object:
            obj.changed = False
        self._changed = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.main_window.setWindowTitle(value)
        self._changed = True

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value
        self._changed = True

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value
        self._changed = True


class Hirarchy(object, metaclass=IterRegistry):

    def __init__(self, name: str) -> None:

        self._parent = None
        self._children = list()
        self._name = name
        self.changed = True

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        for child in self.children:
            child.name = value
        self.changed = True

    @property
    def parent(self) -> Type[Hirarchy]:
        return self._parent

    @parent.setter
    def parent(self, parent: Type[Hirarchy]) -> None:
        self._parent = parent
        self.changed = True

    @property
    def is_parent(self) -> bool:
        if self.children:
            return True
        else:
            return False

    @property
    def is_child(self) -> bool:
        if self.parent is not None:
            return True
        else:
            return False

    @property
    def children(self) -> list[Type[Hirarchy]]:
        return self._children

    def add_child(self, child: Type[Hirarchy]) -> None:
        self.children.append(child)
        child.parent = self
        self.changed = True

    def remove_child(self, child: Type[Hirarchy]) -> None:
        self.children.remove(child)
        child.delete()

    def delete(self) -> None:
        if self in self._registry:
            self._registry.remove(self)


class PropertySet(Hirarchy):
    _registry: list[PropertySet] = list()

    def __init__(self, name: str, obj: Object = None, identifier: str = None) -> None:
        super(PropertySet, self).__init__(name)
        self._attributes = list()
        self._object = obj
        self._registry.append(self)
        self.identifier = identifier
        if self.identifier is None:
            self.identifier = str(uuid4())
        self.changed = True

    @property
    def is_predefined(self) -> bool:
        if self.object is None:
            return True
        else:
            return False

    @property
    def parent(self) -> PropertySet:
        parent = super(PropertySet, self).parent
        return parent

    @parent.setter
    def parent(self, parent: PropertySet) -> None:
        if parent is None:
            self.remove_parent(self._parent)
            return
        self._parent = parent

    def change_parent(self, new_parent: PropertySet) -> None:
        for attribute in self.attributes:
            if attribute.parent.property_set == self._parent:
                self.remove_attribute(attribute)
        self.parent = new_parent

    def delete(self) -> None:
        super(PropertySet, self).delete()
        if self.object is not None:
            ident = self.object.ident_attrib  # if identifier in Pset delete all attributes except identifier
            if ident in self.attributes:
                remove_list = [attribute for attribute in self.attributes if attribute != ident]
                for attribute in remove_list:
                    self.remove_attribute(attribute)
            else:
                self.object.remove_property_set(self)

    @property
    def object(self) -> Object:
        return self._object

    @object.setter
    def object(self, value: Object):
        self._object = value
        self.changed = True

    @property
    def attributes(self) -> list[Attribute]:
        return self._attributes

    @attributes.setter
    def attributes(self, value: list[Attribute]) -> None:
        self._attributes = value
        self.changed = True

    def add_attribute(self, value: Attribute) -> None:
        self._attributes.append(value)
        self.changed = True
        for child in self.children:
            attrib: Attribute = copy.copy(value)
            attrib.identifier = str(uuid4())
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value: Attribute) -> None:
        self._attributes.remove(value)
        for child in self.children:
            for attribute in child.attributes:
                if attribute.parent == value:
                    child.remove_attribute(attribute)
        self.changed = True

    def get_attribute_by_name(self, name: str):
        for attribute in self.attributes:
            if attribute.name.lower() == name.lower():
                return attribute
        return None

    def remove_parent(self, old_parent: PropertySet):
        remove_list = list()
        for attribute in self.attributes:
            if attribute.parent.property_set == old_parent:
                remove_list.append(attribute)

        for attribute in remove_list:
            self.remove_attribute(attribute)
        self._parent = None

    def __copy__(self):
        new_pset = PropertySet(self.name)
        for attribute in self.attributes:
            new_attrib = copy.copy(attribute)
            new_attrib.property_set = new_pset
        if self.parent is not None:
            self.parent.add_child(new_pset)

        return new_pset

    def create_child(self,name) -> PropertySet:
        child  = PropertySet(name)
        self.children.append(child)
        child.parent = self
        for attribute in self.attributes:
            new_attrib =attribute.create_child()
            new_attrib.property_set = child
        return child

class Attribute(Hirarchy):
    _registry: list[Attribute] = list()

    def __init__(self, property_set: PropertySet, name: str, value: list, value_type: int, data_type: str = "xs:string",
                 child_inherits_values: bool = False, identifier: str = None):

        super(Attribute, self).__init__(name=name)
        self._value = value
        self._propertySet = property_set
        self._value_type = value_type
        self._data_type = data_type
        self._object = None
        self._registry.append(self)

        self.changed = True
        self._child_inherits_values = child_inherits_values
        self.identifier = identifier
        if self.identifier is None:
            self.identifier = str(uuid4())
        property_set.add_attribute(self)

    def __str__(self) -> str:
        text = f"{self.property_set.name} : {self.name} = {self.value}"
        return text

    @property
    def child_inherits_values(self) -> bool:
        return self._child_inherits_values

    @child_inherits_values.setter
    def child_inherits_values(self, value: bool) -> None:
        self._child_inherits_values = value

    @property
    def name(self) -> str:
        return super(Attribute, self).name

    @name.setter
    def name(self, value: str) -> None:
        self.changed = True #ToDo: add request for unlink
        self._name = value
        for child in self.children:
            child.name = value

    @property
    def value(self) -> list:
        return self._value

    @value.setter
    def value(self, value: list) -> None:
        def can_be_changed() -> bool:
            change_bool = True
            if self.is_child:
                parent: Attribute = self.parent
                if parent.child_inherits_values:
                    change_bool = False
            return change_bool

        new_value = []

        for el in value:
            if isinstance(el, str):
                if "|" in el:
                    el = el.split("|")
                    for item in el:
                        new_value.append(item)
                else:
                    new_value.append(el)
            else:
                new_value.append(el)

        if can_be_changed():
            self._value = new_value
            self.changed = True

    @property
    def value_type(self) -> int:
        return self._value_type

    @value_type.setter
    def value_type(self, value: int):

        if not self.is_child:
            self._value_type = value
            self.changed = True

        if self.is_parent:
            for child in self.children:
                child._value_type = value
                self.changed = True

    @property
    def data_type(self) -> str:
        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> None:
        if not self.is_child:
            self._data_type = value
            self.changed = True

        if self.is_parent:
            for child in self.children:
                child._data_type = value
                self.changed = True

    @property
    def property_set(self) -> PropertySet:
        return self._propertySet

    @property_set.setter
    def property_set(self, value: PropertySet) -> None:
        self.property_set.remove_attribute(self)
        value.add_attribute(self)
        self._propertySet = value
        self.changed = True

    def is_equal(self, attribute: Attribute) -> bool:
        equal = True

        if self.name != attribute.name:
            equal = False

        if self.value != attribute.value:
            equal = False

        if self.property_set.name != attribute.property_set.name:
            equal = False

        if equal:
            return True

    def delete(self) -> None:
        self.property_set.remove_attribute(self)
        for child in self.children:
            child.delete()

    def create_child(self) -> Attribute:
        child = copy.copy(self)
        self.add_child(child)
        return child

    def __copy__(self) -> Attribute:
        new_attrib:Attribute = copy.deepcopy(self)
        new_attrib.identifier = uuid4()
        return new_attrib

class Object(Hirarchy):
    _registry: list[Object] = list()

    def __init__(self, name: str, ident_attrib: [Attribute, str], identifier: str = None) -> None:
        super(Object, self).__init__(name=name)
        self._registry.append(self)

        self._scripts: list[Script] = list()
        self._property_sets: list[PropertySet] = list()
        self._ident_attrib = ident_attrib
        self._nodes: set[graphs_window.Node] = set()
        self.changed = True

        if identifier is None:
            self.identifier = str(uuid4())
        else:
            self.identifier = identifier

    def __str__(self):
        return f"Object {self.name}"

    @property
    def nodes(self) -> set[graphs_window.Node]:  # Todo: add nodes functionality to graphs_window
        return self._nodes

    def add_node(self, node: graphs_window.Node) -> None:
        self._nodes.add(node)

    def remove_node(self, node: graphs_window.Node) -> None:
        self.nodes.remove(node)

    @property
    def inherited_property_sets(self) -> dict[Object, list[PropertySet]]:
        def recursion(recursion_property_sets, recursion_obj: Object):
            psets = recursion_obj.property_sets

            if psets:
                recursion_property_sets[recursion_obj] = psets

            parent = recursion_obj.parent
            if parent is not None:
                recursion_property_sets = recursion(recursion_property_sets, parent)
            return recursion_property_sets

        property_sets = dict()
        if self.parent is not None:
            inherited_property_sets = recursion(property_sets, self.parent)
        else:
            inherited_property_sets = dict()

        return inherited_property_sets

    @property
    def is_concept(self) -> bool:
        if isinstance(self.ident_attrib, Attribute):
            return False
        else:
            return True

    @property
    def ident_attrib(self) -> Attribute:
        return self._ident_attrib

    @ident_attrib.setter
    def ident_attrib(self, value: Attribute) -> None:
        self._ident_attrib = value
        self.changed = True

    @property
    def property_sets(self) -> list[PropertySet]:
        return self._property_sets

    def add_property_set(self, property_set: PropertySet) -> None:
        self._property_sets.append(property_set)
        property_set.object = self

    def remove_property_set(self, property_set: PropertySet) -> None:
        if property_set in self._property_sets:
            self._property_sets.remove(property_set)

    def get_attributes(self, inherit: bool = False) -> list[Attribute]:
        attributes = list()
        for property_set in self.property_sets:
            attributes += property_set.attributes

        if inherit:
            attributes += self.parent.get_attributes(inherit=True)

        return attributes

    @property
    def scripts(self) -> list[Script]:
        return self._scripts

    def add_script(self, script: Script) -> None:
        self._scripts.append(script)

    def delete_script(self, script: Script) -> None:
        self._scripts.remove(script)

    def delete(self) -> None:
        super(Object, self).delete()
        pset: PropertySet
        for pset in self.property_sets:
            pset.delete()

        for node in self.nodes.copy():
            if node.scene() is not None:
                node.delete_clicked()


    def get_property_set_by_name(self, property_set_name: str) -> PropertySet | None:
        for property_set in self.property_sets:
            if property_set.name == property_set_name:
                return property_set
        return None


class Script(QListWidgetItem):
    def __init__(self, title: str, obj: Object) -> None:
        super(Script, self).__init__(title)
        self.code = str()
        self.changed = True
        self._object = obj
        obj.add_script(self)
        self._name = title
        self.setFlags(self.flags() | Qt.ItemIsEditable)

    @property
    def object(self) -> Object:
        return self._object

    @object.setter
    def object(self, value: Object) -> None:
        self._object.delete_script(self)
        self._object = value
        value.add_script(self)
        self.changed = True

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.changed = True


class CustomTree(QTreeWidget):
    def __init__(self, layout) -> None:
        super(CustomTree, self).__init__(layout)

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


class CustomTreeItem(QTreeWidgetItem):
    def __init__(self, tree: QTreeWidget, obj: Object) -> None:
        super(CustomTreeItem, self).__init__(tree)
        self._object = obj
        self.update()

    def addChild(self, child: CustomTreeItem) -> None:
        super(CustomTreeItem, self).addChild(child)
        if child.object not in self.object.children:
            self.object.add_child(child.object)

    @property
    def object(self) -> Object:
        return self._object

    def update(self) -> None:
        self.setText(0, self.object.name)
        if self.object.is_concept:
            self.setText(1, "")
        else:
            self.setText(1, str(self.object.ident_attrib.value))


class CustomListItem(QListWidgetItem):
    def __init__(self, property_set: PropertySet) -> None:
        super(CustomListItem, self).__init__()
        self._property_set = property_set
        self.setText(property_set.name)

    @property
    def property_set(self) -> PropertySet:
        return self._property_set

    def update(self) -> None:
        self.setText(self.property_set.name)

class CustomTableItem(QTableWidgetItem):
    def __init__(self,item:Object|PropertySet|Attribute):
        super(CustomTableItem, self).__init__()
        self.item = item