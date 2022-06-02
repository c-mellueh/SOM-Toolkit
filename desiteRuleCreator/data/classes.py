from PySide6.QtWidgets import QTreeWidget,QTreeWidgetItem,QAbstractItemView,QListWidgetItem
from PySide6.QtGui import QDropEvent
from PySide6.QtCore import Qt
from uuid import uuid4
from desiteRuleCreator import __version__ as project_version
global _changed
import copy

#Add child to Parent leads to reverse


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
    iter = list()
    def __init__(self, name):

        self._parent = None
        self._children = list()
        self.iter.append(self)
        self._name = name

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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent)-> None:
        self._parent = parent

    @property
    def is_parent(self)->bool:
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
    def children(self) -> list:
        return self._children

    def add_child(self, child,copy = None)-> None:
        self.children.append(child)
        child.parent = self

    def remove_child(self, child)-> None:
        self.children.remove(child)
        child.delete()

    def delete(self)-> None:
        if self in self.iter:
            self.iter.remove(self)


class PropertySet(Hirarchy):
    iter= list()

    def __init__(self, name:str, object = None, identifier = None):
        super(PropertySet, self).__init__(name)
        self._attributes = list()
        self._object = object
        self.identifier = identifier
        if self.identifier is None:
            self.identifier = str(uuid4())
        self.changed = True


    @property
    def is_predefined(self):
        if self.object is None:
            return True
        else:
            return False

    @property
    def parent(self):
        parent = super(PropertySet, self).parent
        return parent

    @parent.setter
    def parent(self, parent)->None:
        if parent is None:
            self.remove_parent(self._parent)
        else:
            self._parent = parent
            for par_attribute in parent.attributes:
                par_attribute: Attribute = par_attribute
                if par_attribute not in [attribute.parent for attribute in self.attributes]:
                    attribute = Attribute(self,par_attribute.name,par_attribute.value,par_attribute.value_type,par_attribute.data_type)
                    par_attribute.add_child(attribute)

    def change_parent(self,new_parent)->None:
        for attribute in self.attributes:
            if attribute.parent.propertySet == self._parent:
                self.remove_attribute(attribute)
        self.parent =new_parent

    def delete(self)->None:
        super(PropertySet, self).delete()
        if self.is_parent:
            for child in self.children:
                self.remove_child(child)
        if self.object is not None:
            ident = self.object.ident_attrib      # if identifier in Pset delete all attributes except identifier
            if ident in self.attributes:
                remove_list = [attribute for attribute in self.attributes if attribute != ident]
                for attribute in remove_list:
                    self.remove_attribute(attribute)
            else:
                self.object.remove_property_set(self)



    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        self._object = value
        self.changed = True

    @property
    def attributes(self) -> list:
        return self._attributes

    @attributes.setter
    def attributes(self, value: list)-> None:
        self._attributes = value
        self.changed = True

    def add_attribute(self, value)->None:
        self._attributes.append(value)
        self.changed = True
        for child in self.children:
            attrib:Attribute = copy.copy(value)
            attrib.identifier = str(uuid4())
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value)->None:
        self._attributes.remove(value)
        for child in self.children:
            for attribute in child.attributes:
                if attribute.parent == value:
                    child.remove_attribute(attribute)
        self.changed = True

    def get_attribute(self,name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None

    def remove_parent(self,old_parent):
        remove_list = list()
        for attribute in self.attributes:
            if attribute.parent.propertySet == old_parent:
                remove_list.append(attribute)

        for attribute in remove_list:
            self.remove_attribute(attribute)
        self._parent = None

class Attribute(Hirarchy):
    iter= list()

    def __init__(self,propertySet:PropertySet, name:str, value,value_type, data_type = "xs:string",child_inherits_values = False,identifier = None):
        super(Attribute, self).__init__(name=name)
        self._value = value
        self._propertySet = propertySet
        self._value_type = value_type
        self._data_type = data_type
        self._object = None
        self.changed = True
        self._child_inherits_values = child_inherits_values
        self.identifier = identifier
        if self.identifier is None:
            self.identifier = str(uuid4())
        propertySet.add_attribute(self)

    def __str__(self):
        text = f"{self.propertySet.name} : {self.name} = {self.value}"
        return text

    @property
    def child_inherits_values(self)-> bool:
        return self._child_inherits_values

    @child_inherits_values.setter
    def child_inherits_values(self, value:bool)->None:
        self._child_inherits_values = value

    @property
    def name(self)->str:
        return super(Attribute, self).name

    @name.setter
    def name(self, value:str)->None:
        self.changed = True

        if not self.is_child:
            self._name = value

        if self.is_parent:
            for child in self.children:
                child.name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value:list)->None:
        def can_be_changed(self)->bool:
            can_be_changed = True
            if self.is_child:
                parent: Attribute = self.parent
                if parent.child_inherits_values:
                    can_be_changed = False
            return can_be_changed

        new_value = []

        for el in value:
            if isinstance(el,str):
                if "|" in el:
                    el = el.split("|")
                    for item in el:
                        new_value.append(item)
                else:new_value.append(el)
            else:
                new_value.append(el)

        if can_be_changed(self):
            self._value = new_value
            self.changed = True

    @property
    def value_type(self):
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
    def data_type(self, value: str):
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

class Object(Hirarchy):
    iter= list()
    def __init__(self, name, ident_attrib: [Attribute, str], is_concept = False,identifier = None):
        super(Object, self).__init__(name = name)
        self._scripts = list()
        self._property_sets = list()
        self._ident_attrib = ident_attrib
        self._is_concept = is_concept
        self.changed = True
        if identifier is None:
            print("CREATE_NEW")
            self.identifier = str(uuid4())
        else:
            self.identifier = identifier

    @property
    def inherited_property_sets(self)->dict:
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
            inherited_property_sets = recursion(property_sets, self.parent)
        else:
            inherited_property_sets = dict()

        return inherited_property_sets

    @property
    def is_concept(self)->bool:
        return  self._is_concept

    @is_concept.setter
    def is_concept(self,value:bool)->None:
        self._is_concept = value
        self.changed = True

    @property
    def ident_attrib(self) -> Attribute:
        return self._ident_attrib

    @ident_attrib.setter
    def ident_attrib(self, value:Attribute)->None:
        self._ident_attrib = value
        self.changed = True

    @property
    def property_sets(self)->list[PropertySet]:
        return self._property_sets

    def add_property_set(self,property_set:PropertySet)->None:
        self._property_sets.append(property_set)
        property_set.object = self

    def remove_property_set(self,property_set:PropertySet)->None:
        self._property_sets.remove(property_set)

    def get_attributes(self,inherit = False):
        attributes = list()
        for property_set in self.property_sets:
            attributes += property_set.attributes

        if inherit:
            attributes+= self.parent.get_attributes(inherit=True)

        return attributes

    @property
    def scripts(self):
        return self._scripts

    def add_script(self,script):
        self._scripts.append(script)

    def delete_script(self,script):
        self._scripts.remove(script)

    def delete(self) -> None:
        super(Object, self).delete()
        pset:PropertySet
        for pset in self.property_sets:
            pset.delete()

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
    def object(self)->Object:
        return self._object

    def update(self):
        print("update")
        self.setText(0,self.object.name)
        self.setText(1,str(self.object.ident_attrib))






