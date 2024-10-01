from __future__ import annotations
import SOMcreator
from uuid import uuid4
from .base import filterable, Hirarchy
import copy as cp
from typing import Iterator
import logging


class PropertySet(Hirarchy):
    _registry: set[PropertySet] = set()

    def __init__(self, name: str, obj: SOMcreator.Object = None, uuid: str = None, description: None | str = None,
                 optional: None | bool = None, project: None | SOMcreator.Project = None,
                 filter_matrix: list[list[bool]] = None) -> None:
        super(PropertySet, self).__init__(name, description, optional, project, filter_matrix)
        self._attributes = set()
        self._object = None
        if obj is not None:
            obj.add_property_set(self)  # adds Pset to Object and sets pset.object = obj
        self._registry.add(self)
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = str(uuid4())

    def __lt__(self, other):
        if isinstance(other, PropertySet):
            return self.name < other.name
        else:
            return self.name < other

    def __str__(self):
        return f"PropertySet: {self.name}"

    def __copy__(self) -> PropertySet:
        new_pset = PropertySet(name=self.name, obj=None, uuid=str(uuid4()), description=self.description,
                               optional=self.is_optional(ignore_hirarchy=True), project=self.project,
                               filter_matrix=self._filter_matrix)

        for attribute in self.get_attributes(filter=False):
            new_attribute = cp.copy(attribute)
            new_pset.add_attribute(new_attribute)

        if self.parent is not None:
            self.parent.add_child(new_pset)

        return new_pset

    @property
    def is_predefined(self) -> bool:
        return self.object is None

    @property
    def parent(self) -> PropertySet:
        parent = super(PropertySet, self).parent
        return parent

    @parent.setter
    def parent(self, parent: PropertySet) -> None:
        """
        Use parent.add_child if you want to set the parent

        :param parent:
        :return:
        """
        if parent is None:
            self.remove_parent()
            return
        self._parent = parent

    def remove_child(self, child: PropertySet) -> None:
        super().remove_child(child)
        child.remove_parent()
        for attribute in [a for a in child.get_attributes(filter=False) if a.parent]:
            attribute.parent.remove_child(attribute)

    def change_parent(self, new_parent: PropertySet) -> None:
        for attribute in self.get_attributes(filter=False):
            if attribute.parent.property_set == self._parent:
                self.remove_attribute(attribute)
        self.parent = new_parent

    def delete(self, recursive: bool = False, override_ident_deletion=False) -> None:
        ident_attrib = None
        if self.object is not None:
            ident_attrib = self.object.ident_attrib

        if ident_attrib in self.get_attributes(filter=False) and not override_ident_deletion:
            logging.error(f"Can't delete Propertyset {self.name} because it countains the identifier Attribute")
            return

        super(PropertySet, self).delete()
        [attrib.delete(recursive) for attrib in self.get_attributes(filter=False) if attrib]
        if self.object is not None:
            self.object.remove_property_set(self)

    @property
    def object(self) -> SOMcreator.Object:
        return self._object

    @object.setter
    def object(self, value: SOMcreator.Object):
        self._object = value

    @filterable
    def get_attributes(self) -> Iterator[SOMcreator.Attribute]:
        """returns all Attributes even if they don't fit the current Project Phase"""
        return iter(self._attributes)

    def add_attribute(self, value: SOMcreator.Attribute) -> None:
        if value.property_set is not None and value.property_set != self:
            value.property_set.remove_attribute(value)
        self._attributes.add(value)

        value.property_set = self
        for child in self.get_children(filter=False):
            attrib: SOMcreator.Attribute = cp.copy(value)
            value.add_child(attrib)
            child.add_attribute(attrib)

    def remove_attribute(self, value: SOMcreator.Attribute, recursive=False) -> None:
        if value in self.get_attributes(filter=False):
            self._attributes.remove(value)
            if recursive:
                for child in value.get_children(filter=False):
                    child.property_set.remove_attribute(child)
        else:
            logging.warning(f"{self.name} -> {value} not in SOMcreator.Attributes")

    def get_attribute_by_name(self, name: str):
        for attribute in self.get_attributes(filter=False):
            if attribute.name.lower() == name.lower():
                return attribute
        return None

    def create_child(self, name) -> PropertySet:
        child = PropertySet(name=name, project=self.project)
        self._children.add(child)
        child.parent = self
        for attribute in self.get_attributes(filter=False):
            new_attrib = attribute.create_child()
            child.add_attribute(new_attrib)
        return child
