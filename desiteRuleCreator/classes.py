from PySide6.QtWidgets import QTreeWidget,QTreeWidgetItem,QAbstractItemView,QListWidgetItem
from PySide6.QtGui import QDropEvent
from PySide6.QtCore import Qt
from uuid import uuid4
from . import __version__ as project_version
global _changed
import copy

def attributes_to_psetdict(attributes):
    pset_dict = {}
    for attribute in attributes:
        pset = attribute.propertySet
        if pset in pset_dict.keys():
            list = pset_dict[pset]
            list.append(attribute)
        else:
            pset_dict[pset] = [attribute]

    return pset_dict

def inherited_attributes(obj):
    def recursion(attribute_dict,obj):
        attributes = obj.attributes

        if attributes:
            attribute_dict[obj] = attributes

        parent = obj.parent
        if parent is not None:
            attribute_dict = recursion(attribute_dict, parent)
        return attribute_dict

    attribute_dict = dict()
    if obj.parent is not None:
        attribute_dict = recursion(attribute_dict,obj.parent)
    return attribute_dict


class Project(object):
    def __init__(self,name,author = None):
        self._name = name
        self._author = author
        self._version = project_version
        self._changed = True

    @property
    def changed(self):
        def check_data():
            def check(obj):
                if obj.changed is True:
                    return True
                else:
                    return False

            for obj in Object.iter:
                if check(obj):
                    return True
                for attribute in obj.attributes:
                    if check(attribute) or check(attribute.propertySet):
                        return True

        data = check_data()
        if data or self._changed:
            self._changed = True
        else:
            self._changed = False

        return self._changed

    @changed.setter
    def changed(self,value):
        self._changed = value

    def reset_changed(self):
        global _changed
        for obj in Object.iter:
            obj.changed = False

            for attribute in obj.attributes:
                attribute.changed = False
                attribute.propertySet.changed = False
        self._changed = False


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value
        self._changed = True

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value
        self._changed = True


class Hirarchy(object):
    parent_iter = list()
    def __init__(self,is_parent,is_child):
        self._is_parent = is_parent
        self._is_child = is_child
        self._parent = None
        self._children = list()

        if is_parent:
            self.parent_iter.append(self)

    @property
    def parent(self):
        return self.parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def is_parent(self):
        return self._is_parent

    @is_parent.setter
    def is_parent(self, value):
        self._is_parent = value

    @property
    def is_child(self):
        return self._is_child

    @is_child.setter
    def is_child(self, value):
        self._is_child = value

    @property
    def children(self):
        return self._children

    def add_child(self, value):
        if self.is_parent:
            self.children.append(value)

    def remove_child(self, value):
        if self.is_parent:
            self.children.remove(value)


class PropertySet(Hirarchy):
    parent_iter = list()

    def __init__(self, name:str,is_parent = False, is_child = False):
        super(PropertySet, self).__init__(is_parent,is_child)
        self._name = name
        self._attributes = list()  # attribute_name:value
        self._object = None
        self.changed = True

    def delete(self):
        self.parent_iter.remove(self)

    @property
    def parent(self):
        super(PropertySet, self).parent()

    @parent.setter
    def parent(self, parent):
        self.is_child = True
        self._parent = parent
        for par_attribute in parent.attributes:
            attribute = Attribute(self,par_attribute.name,par_attribute.value,par_attribute.value_type,par_attribute.data_type,is_child=True)
            attribute.parent = par_attribute
        self._parent = parent

    @property
    def is_parent(self):
        return self._is_parent

    @is_parent.setter
    def is_parent(self,value):
        self._is_parent = value

    @property
    def is_child(self):
        return self._is_child

    @is_child.setter
    def is_child(self, value):
        self._is_child = value

    @property
    def children(self):
        return self._children

    def add_child(self,value):
        if self.is_parent:
            self.children.append(value)

    def remove_child(self,value):
        if self.is_parent:
            self.children.remove(value)

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        self._object = value
        self.changed = True

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value
        self.changed = True
    @property
    def attributes(self) -> list:
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict):
        self._attributes = value
        self.changed = True

    def add_attribute(self, value):
        self._attributes.append(value)
        self.changed = True

    def remove_attribute(self, value):
        self._attributes.pop(self._attributes.index(value))
        self.changed = True

class Attribute(Hirarchy):
    def __init__(self,propertySet:PropertySet, name:str, value,value_type, data_type = "xs:string",is_parent = False,is_child = False):
        super(Attribute, self).__init__(is_parent, is_child)
        self._name = name
        self._value = value
        self._propertySet = propertySet
        self._value_type = value_type
        self._data_type = data_type
        self._object = None
        propertySet.add_attribute(self)
        self.changed = True
        self._child_is_modifable = True

    def __str__(self):
        text = f"{self.propertySet.name} : {self.name} = {self.value}"
        return text

    @property
    def child_is_modifiable(self):
        return self._child_is_modifable

    @child_is_modifiable.setter
    def child_is_modifiable(self,value:bool):
        self._child_is_modifable = value

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self,value):
        self._object = value
        self.propertySet.object = self._object
        self.changed = True

    @property
    def name(self)->str:
        return self._name

    @name.setter
    def name(self, value:str):

        if not self.is_child:
            self._name = value
            self.changed = True

        if self.is_parent:
            for child in self.children:
                child._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        new_value = []
        for el in value:
            el:str = el
            if "|" in el:
                el = el.split("|")
                for item in el:
                    new_value.append(item)
            else:
                new_value.append(el)
        print(new_value)
        self._value = new_value
        self.changed = True

    @property
    def value_type(self)-> int :
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
    def data_type(self) -> int:
        return self._data_type

    @data_type.setter
    def data_type(self, value: int):
        if not self.is_child:
            self._data_type = value
            self.changed = True

        if self.is_parent:
            for child in self.children:
                child._data_type = value
                self.changed = True

    @property
    def propertySet(self)->PropertySet:
        return self._propertySet

    @propertySet.setter
    def propertySet(self, value:PropertySet):
        self.propertySet.remove_attribute(self)
        value.add_attribute(self)
        self._propertySet = value
        self.changed = True


    def is_equal(self,attribute):
        equal = True

        if self.name != attribute.name:
            equal = False

        if self.value != attribute.value:
            equal = False

        if self.propertySet.name != attribute.propertySet.name:
            equal = False

        if equal:
            return True

    def delete(self):
        self.propertySet.remove_attribute(self)
        for child in self.children:
            child.delete()

class Object(object):
    iter = list()
    def __init__(self, name, ident: Attribute,parent = None, is_concept = False):
        self.iter.append(self)
        self._inherited_property_sets = dict()
        self._children = list()
        self._scripts = list()
        self._property_sets = list()

        self._name = name
        self._identifier = ident
        self._parent = parent
        self._is_concept = is_concept
        self.add_property_set(ident.propertySet)

        self.changed = True

    @property
    def inherited_property_sets(self):
        def recursion(property_sets, obj:Object):
            psets = obj.property_sets

            if psets:
                property_sets[obj] = psets

            parent = obj.parent
            if parent is not None:
                property_sets = recursion(property_sets, parent)
            return property_sets

        property_sets = dict()
        if self.parent is not None:
            self._inherited_property_sets = recursion(property_sets, self.parent)
        else:
            self._inherited_property_sets = dict()

        return self._inherited_attributes


    @property
    def is_concept(self):
        return  self._is_concept

    @is_concept.setter
    def is_concept(self,value:bool):
        self._is_concept = value
        self.changed = True

    @property
    def inherited_attributes(self) -> dict:
        def recursion(attribute_dict, obj):
            attributes = obj.attributes

            if attributes:
                attribute_dict[obj] = attributes

            parent = obj.parent
            if parent is not None:
                attribute_dict = recursion(attribute_dict, parent)
            return attribute_dict

        attribute_dict = dict()
        if self.parent is not None:
            self._inherited_attributes = recursion(attribute_dict, self.parent)
        return self._inherited_attributes

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,value):
        self._parent = value
        value.add_child(self)
        self.changed = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.changed = True


    @property
    def identifier(self) -> Attribute:
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value
        self.changed = True


    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self.changed = True

    @property
    def property_sets(self)->list[PropertySet]:
        return self._property_sets

    def add_property_set(self,property_set:PropertySet):
        self._property_sets.append(property_set)
        property_set.object = self
        print(f"PropertySet hat Objekt: {self}")
    def remove_property_set(self,property_set:PropertySet):
        self._property_sets.remove(property_set)

    #
    # @property
    # def attributes(self)->list[Attribute]:
    #     return self._attributes
    #
    # def add_attribute(self,attribute):
    #     self._attributes.append(attribute)
    #     attribute.object = self
    #     self.changed = True
    #
    #
    # def remove_attribute(self,attribute):
    #     self._attributes.remove(attribute)
    #     self.changed = True
    #
    #
    # def add_attributes(self,attribute_list):
    #     for attribute in attribute_list:
    #         self.add_attribute(attribute)
    #     self.changed = True

    @property
    def children(self):
        return self._children

    def add_child(self, object):
        self._children.append(object)
        self.changed = True


    def remove_child(self,object):
        self._children.remove(object)
        self.changed = True



    @property
    def psetNameDict(self):
        p_set_dict = attributes_to_psetdict(self._attributes)
        new_dict = {}
        for key in p_set_dict.keys():
            new_dict[key.name]=key
        return new_dict

    def delete(self):
        self.iter.remove(self)

    @property
    def scripts(self):
        return self._scripts

    def add_script(self,script):
        self._scripts.append(script)

    def delete_script(self,script):
        self._scripts.remove(script)



class Script(QListWidgetItem):
    def __init__(self,title:str,obj):
        super(Script, self).__init__(title)
        self.code = str()
        self.changed = True
        self._object = obj
        obj.add_script(self)
        self._name = "NewScript"
        self.setFlags(self.flags()|Qt.ItemIsEditable)

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self,value):
        self._object.delete_script(self)
        self._object = value
        value.add_script(self)
        self.changed = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.changed = True



class CustomTree(QTreeWidget):
    def __init__(self, layout):
        super(CustomTree, self).__init__(layout)

    def dropEvent(self, event:QDropEvent) -> None:

        selected_items = self.selectedItems()
        droped_on_item = self.itemFromIndex(self.indexAt(event.pos()))

        if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            super(CustomTree, self).dropEvent(event)
            parent = droped_on_item.object

        else:
            super(CustomTree, self).dropEvent(event)
            parent = droped_on_item.object.parent

        for el in selected_items:
            object = el.object
            if parent is not None:
                object.parent = parent
            else:
                object.parent = None


class CustomTreeItem(QTreeWidgetItem):
    def __init__(self, tree, object):
        super(CustomTreeItem, self).__init__(tree)
        self._object = object

    def addChild(self, child: QTreeWidgetItem) -> None:
        super(CustomTreeItem, self).addChild(child)
        self._object.add_child(child.object)

    @property
    def object(self):
        return self._object






