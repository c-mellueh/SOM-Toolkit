import constants


class PropertySet:
    def __init__(self, name:str):
        self._name = name
        self._attributes = list()  # attribute_name:value
        self._object = None

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        self._object = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def attributes(self) -> list:
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict):
        self._attributes = value

    def add_attribute(self, value):
        self._attributes.append(value)

    def remove_attribute(self, value):


        self._attributes.pop(self._attributes.index(value))


class Attribute:
    def __init__(self,propertySet:PropertySet, name:str, value,value_type, data_type = "xs:string"):
        self._name = name
        self._value = value
        self._propertySet = propertySet
        self._value_type = value_type
        self._data_type = data_type
        self._object = None
        propertySet.add_attribute(self)

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self,value):
        self._object = value
        self.propertySet.object = self._object


    @property
    def name(self)->str:
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def value_type(self)-> int :
        return self._value_type

    @value_type.setter
    def value_type(self, value: int):
        self._value_type = value

    @property
    def data_type(self) -> int:
        return self._data_type

    @data_type.setter
    def data_type(self, value: int):
        self._data_type = value

    @property
    def propertySet(self)->PropertySet:
        return self._propertySet

    @propertySet.setter
    def propertySet(self, value:PropertySet):
        self.propertySet.remove_attribute(self)
        value.add_attribute(self)
        self._propertySet = value
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


class Group:
    def __init__(self,name):
        self._name = name
        self._objects = []
        self._parent = None
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def add_child(self,object):
        self._objects.append(object)
        object.parent = self

    def remove_child(self,object):
        self._objects.remove(object)
        object.parent= None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

class Object:
    iter = dict()

    def __init__(self, name, ident: Attribute,parent:Group = None):

        self._name = name
        self._identifier = ident
        self.iter[ident] = self
        self._parent = parent
        self._attributes = list()
        self.add_attribute(self._identifier)
        self._parent = None

    @property
    def parent(self) -> Group:
        return self._parent

    @parent.setter
    def parent(self,value:Group):
        self._parent = value
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def identifier(self) -> Attribute:
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def attributes(self)->list[Attribute]:
        return self._attributes

    def add_attribute(self,attribute):
        self._attributes.append(attribute)
        attribute.object = self

    def remove_attribute(self,attribute):
        self._attributes.pop(attribute)

    def attributes_to_psetdict(self):
        pset_dict = {}
        for el in self._attributes:
            pset = el.propertySet
            if pset in pset_dict.keys():
                list = pset_dict[pset]
                list.append(el)
            else: pset_dict[pset]=[el]

        return pset_dict

    @property
    def psetNameDict(self):
        p_set_dict = self.attributes_to_psetdict()
        new_dict = {}
        for key in p_set_dict.keys():
            new_dict[key.name]=key

        return new_dict

    def delete(self):
        self.iter.pop(self.identifier)







