from __future__ import annotations

import copy
from typing import Iterator, Type, TYPE_CHECKING
from uuid import uuid4

from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QListWidgetItem, QTableWidgetItem

from desiteRuleCreator.data import constants
from desiteRuleCreator.Filehandling import save_file,open_file

if TYPE_CHECKING:
    from desiteRuleCreator.Windows import graphs_window
    from desiteRuleCreator.main_window import MainWindow


# Add child to Parent leads to reverse

class IterRegistry(type):
    _registry= set()
    """ Helper for Iteration"""

    def __iter__(self) -> Iterator[PropertySet|Object|Attribute|Aggregation]:
        return iter(sorted(list(self._registry),key= lambda x:x.name))

    def __len__(self) -> int:
        return len(self._registry)


class Project(object):
    def __init__(self, main_window: MainWindow, name: str, author: str = None) -> None:
        self._name = ""
        self._author = author
        self._version = "1.0.0"
        self._changed = True
        self.main_window = main_window
        self.name = name
        self.seperator_status = True
        self.seperator = ","

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

    def save(self,path:str):
        save_file.save(self,path)

    def clear(self):
        for obj in Object:
            obj.delete()
            print(len(Object))
        for pset in PropertySet:
            pset.delete()

        for attribute in Attribute:
            attribute.delete()
        self.name = ""
        self.author = ""
        self.version = "1.0.0"
        self.changed = True
        self.name = ""
        self.seperator_status = True
        self.seperator = ","


    #
    # def open(self,path):
    #     open_file.o

class Hirarchy(object, metaclass=IterRegistry):

    def __init__(self, name: str) -> None:

        self._parent = None
        self._children = set()
        self._name = name
        self.changed = True
        self._mapping_dict = {
            constants.SHARED_PARAMETERS:True,
            constants.IFC_MAPPING:True
        }
    @property
    def mapping_dict(self) -> dict[str,bool]:
        return self._mapping_dict

    @mapping_dict.setter
    def mapping_dict(self,value:dict[str,bool]) -> None:
        self._mapping_dict = value

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
    def children(self) -> set[Type[Hirarchy]]:
        return self._children

    def add_child(self, child: Type[Hirarchy]) -> None:
        self.children.add(child)
        child.parent = self
        self.changed = True

    def remove_child(self, child: Type[Hirarchy]) -> None:
        self.children.remove(child)
        child.delete()

    def delete(self) -> None:
        if self in self._registry:
            self._registry.remove(self)


class PropertySet(Hirarchy):
    _registry: set[PropertySet] = set()

    def __init__(self, name: str, obj: Object = None, identifier: str = None) -> None:
        super(PropertySet, self).__init__(name)
        self._attributes = set()
        self._object = obj
        self._registry.add(self)
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
    def attributes(self) -> set[Attribute]:
        return self._attributes

    @attributes.setter
    def attributes(self, value: set[Attribute]) -> None:
        self._attributes = value
        self.changed = True

    def add_attribute(self, value: Attribute) -> None:
        self._attributes.add(value)
        self.changed = True

        # if value.property_set is not None:
        #     value.property_set.remove_attribute(value)
        value._property_set = self
        for child in self.children:
            attrib: Attribute = copy.copy(value)
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value: Attribute) -> None:
        if value in self.attributes:
            self.attributes.remove(value)
            for child in self.children:
                for attribute in list(child.attributes):
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
            new_pset.add_attribute(new_attrib)

        if self.parent is not None:
            self.parent.add_child(new_pset)

        return new_pset

    def create_child(self, name) -> PropertySet:
        child = PropertySet(name)
        self.children.append(child)
        child.parent = self
        for attribute in self.attributes:
            new_attrib = attribute.create_child()
            child.add_attribute(new_attrib)
        return child


class Attribute(Hirarchy):
    _registry: set[Attribute] = set()

    def __init__(self, property_set: PropertySet | None, name: str, value: list, value_type: int,
                 data_type: str = "xs:string",
                 child_inherits_values: bool = False, identifier: str = None):

        super(Attribute, self).__init__(name=name)
        self._value = value
        self._property_set = property_set
        self._value_type = value_type
        self._data_type = data_type
        self._registry.add(self)
        self._revit_name = name

        self.changed = True
        self._child_inherits_values = child_inherits_values
        self.identifier = identifier
        if self.identifier is None:
            self.identifier = str(uuid4())
        if property_set is not None:
            property_set.add_attribute(self)

    def __str__(self) -> str:
        text = f"{self.property_set.name} : {self.name} = {self.value}"
        return text

    @property
    def revit_name(self) -> str:
        return self._revit_name

    @revit_name.setter
    def revit_name(self, value: str) -> None:
        self._revit_name = value

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
        self.changed = True  # ToDo: add request for unlink
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
        """
        "xs:string"; "xs:double"; "xs:boolean"; XS_INT = "xs:int"
        :return:
        """

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
        return self._property_set

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
        new_attrib: Attribute = Attribute(None, self.name, self.value,
                                          self.value_type, self.data_type, self.child_inherits_values)
        if self.parent is not None:
            self.parent.add_child(new_attrib)
        return new_attrib


class Object(Hirarchy):
    _registry: set[Object] = set()

    def __init__(self, name: str, ident_attrib: [Attribute, str], identifier: str = None, ifc_mapping:set[str]|None = None ) -> None:
        super(Object, self).__init__(name=name)
        self._registry.add(self)

        self._scripts: list[Script] = list()
        self._property_sets: list[PropertySet] = list()
        self._ident_attrib = ident_attrib
        self._nodes: set[graphs_window.Node] = set()

        if ifc_mapping is None:
            self._ifc_mapping = {"IfcBuildingElementProxy"}
        else:
            self._ifc_mapping = ifc_mapping

        self.changed = True

        if identifier is None:
            self.identifier = str(uuid4())
        else:
            self.identifier = identifier

    def __str__(self):
        return f"Object {self.name}"

    @property
    def ifc_mapping(self) -> set[str]:
        return self._ifc_mapping

    @ifc_mapping.setter
    def ifc_mapping(self, value: set[str]):
        value_set = set()
        for item in value:  #filter empty Inputs
            if not (item == "" or item is None):
                value_set.add(item)
        self._ifc_mapping = value_set

    def add_ifc_map(self, value: str) -> None:
        self._ifc_mapping.add(value)

    def remove_ifc_map(self, value: str) -> None:
        self._ifc_mapping.remove(value)

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
        Object._registry.remove(self)
        pset: PropertySet
        for pset in self.property_sets:
            pset.delete()

        for node in self.nodes.copy():
            if node.scene() is not None:
                node.delete()

    def get_property_set_by_name(self, property_set_name: str) -> PropertySet | None:
        for property_set in self.property_sets:
            if property_set.name == property_set_name:
                return property_set
        return None


class Aggregation(Hirarchy):
    _registry: set[Aggregation] = set()

    def __init__(self,obj:Object,uuid:str|None = None):
        super(Aggregation, self).__init__(name = obj.name)
        self._registry.add(self)
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = str(uuid)
        self.object = obj
        self.parent:Aggregation|None = None
        self.connection_dict:dict[Aggregation,int] = dict()

    def add_child(self,child:Aggregation,connection_type: int = constants.AGGREGATION) -> Aggregation:
        self.children.add(child)
        child.parent = self
        self.connection_dict[child]= connection_type
        return child

    @property
    def is_root(self):
        return not self.children


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
    def __init__(self,obj: Object,func = None) -> None:
        super(CustomObjectTreeItem, self).__init__()
        self._object = obj
        self._func = func
        self.update()


    def addChild(self, child: CustomObjectTreeItem) -> None:
        super(CustomObjectTreeItem, self).addChild(child)
        if child.object not in self.object.children:
            self.object.add_child(child.object)

    @property
    def object(self) -> Object:
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
    def __init__(self, tree: QTreeWidget, pset: PropertySet) -> None:
        super(CustomPSetTreeItem, self).__init__(tree)
        self._property_set = pset
        self.update()

    @property
    def property_set(self) -> PropertySet:
        return self._property_set

    def update(self) -> None:
        self.setText(0, self.property_set.name)


class CustomAttribTreeItem(QTreeWidgetItem):
    def __init__(self, tree: QTreeWidget, attribute: Attribute) -> None:
        super(CustomAttribTreeItem, self).__init__(tree)
        self._attribute = attribute
        self.update()

    @property
    def attribute(self) -> Attribute:
        return self._attribute

    def update(self) -> None:
        self.setText(0, self.attribute.name)


class CustomListItem(QListWidgetItem):
    def __init__(self, data: PropertySet | Object | Attribute) -> None:
        super(CustomListItem, self).__init__()
        self._linked_data = data
        self.setText(data.name)

    @property
    def linked_data(self) -> PropertySet | Object | Attribute:
        return self._linked_data

    def update(self) -> None:
        self.setText(self.linked_data.name)


class CustomTableItem(QTableWidgetItem):
    def __init__(self, item: Object | PropertySet | Attribute):
        super(CustomTableItem, self).__init__()
        self.linked_data = item
        self.setText(item.name)

































