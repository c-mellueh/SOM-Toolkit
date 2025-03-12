from __future__ import annotations
import SOMcreator
from uuid import uuid4
from .base import filterable, BaseClass
import copy as cp
from typing import Iterator, TYPE_CHECKING, Self
import logging

if TYPE_CHECKING:
    from .base import BASE_TYPE


class SOMPropertySet(BaseClass):
    def __init__(
        self,
        name: str,
        som_class: SOMcreator.SOMClass | None = None,
        uuid: str | None = None,
        description: None | str = None,
        optional: None | bool = None,
        project: None | SOMcreator.SOMProject = None,
        filter_matrix: list[list[bool]] | None = None,
    ) -> None:

        super(SOMPropertySet, self).__init__(
            name, description, optional, project, filter_matrix
        )
        self._properties: set[SOMcreator.SOMProperty] = set()
        self._som_class: SOMcreator.SOMClass | None = som_class
        if som_class is not None:
            som_class.add_property_set(
                self
            )  # adds Pset to Class and sets pset.class = cls
        self.uuid = str(uuid4()) if uuid is None else uuid

    def __lt__(self, other):
        if isinstance(other, SOMPropertySet):
            return self.name < other.name
        else:
            return self.name < other

    def __str__(self):
        return f"PropertySet: {self.name}"

    def __copy__(self) -> SOMPropertySet:
        new_pset = SOMPropertySet(
            name=self.name,
            som_class=None,
            uuid=str(uuid4()),
            description=self.description,
            optional=self.is_optional(ignore_hirarchy=True),
            project=self.project,
            filter_matrix=self._filter_matrix,
        )

        for som_property in self.get_properties(filter=False):
            new_property = cp.copy(som_property)
            new_pset.add_property(new_property)

        if self.parent is not None:
            self.parent.add_child(new_pset)

        return new_pset

    @property
    def is_predefined(self) -> bool:
        return self.som_class is None

    @property
    def parent(self) -> SOMPropertySet | None:
        parent = super(SOMPropertySet, self).parent
        return parent

    @parent.setter
    def parent(self, parent: SOMPropertySet) -> None:
        """
        Use parent.add_child if you want to set the parent

        :param parent:
        :return:
        """
        if parent is None:
            self.remove_parent()
            return
        self._parent = parent  # type: ignore

    def remove_child(self, child: SOMPropertySet) -> None:
        super().remove_child(child)  # type: ignore
        child.remove_parent()
        for som_property in child.get_properties(filter=False):
            if som_property.parent is None:
                continue
            som_property.parent.remove_child(som_property)

    def change_parent(self, new_parent: SOMPropertySet) -> None:
        for som_property in self.get_properties(filter=False):
            if som_property.parent is None:
                continue
            if som_property.parent.property_set == self._parent:
                self.remove_property(som_property)
        self.parent = new_parent

    def delete(self, recursive: bool = False, override_ident_deletion=False) -> None:
        if self.som_class is not None:
            identifier_property = self.som_class.identifier_property
        else:
            identifier_property = None
        if (
            identifier_property in list(self.get_properties(filter=False))
            and not override_ident_deletion
        ):
            logging.error(
                f"Can't delete Propertyset {self.name} because it countains the identifier Property"
            )
            return

        super(SOMPropertySet, self).delete(recursive)
        [
            prop.delete(recursive)
            for prop in list(self.get_properties(filter=False))
            if prop is not None
        ]
        if self.som_class is not None:
            self.som_class.remove_property_set(self)

    @property
    def som_class(self) -> SOMcreator.SOMClass | None:
        return self._som_class

    @som_class.setter
    def som_class(self, value: SOMcreator.SOMClass):
        self._som_class = value

    @filterable
    def get_properties(self) -> Iterator[SOMcreator.SOMProperty]:
        """returns all Properties"""
        return iter(self._properties)

    def add_property(self, value: SOMcreator.SOMProperty) -> None:

        if value.property_set is not None and value.property_set != self:
            value.property_set.remove_property(value)

        if value not in self._properties:
            self._properties.add(value)
        else:
            return
        value.property_set = self
        for child in self.get_children(filter=False):
            child:SOMPropertySet
            som_property: SOMcreator.SOMProperty = cp.copy(value)
            value.add_child(som_property)
            child.add_property(som_property)

    def remove_property(self, value: SOMcreator.SOMProperty, recursive=False) -> None:
        if value in self.get_properties(filter=False):
            self._properties.remove(value)
            if recursive:
                for child in value.get_children(filter=False):
                    child:SOMcreator.SOMProperty
                    child.property_set.remove_property(child)
        else:
            logging.warning(f"{self.name} -> {value} not in SOMcreator.SOMPropertys")

    def get_property_by_name(self, name: str):
        for som_property in self.get_properties(filter=False):
            if som_property.name.lower() == name.lower():
                return som_property
        return None

    def create_child(self, name=None) -> SOMPropertySet:
        name = self.name if not name else name
        child = SOMPropertySet(name=name, project=self.project)
        self._children.add(child)
        child.parent = self
        for som_property in self.get_properties(filter=False):
            new_property = som_property.create_child()
            child.add_property(new_property)
        return child
    
    @property
    def project(self) -> SOMcreator.SOMProject | None:
        if self._project:
            return self._project
        if self.som_class:
            return self.som_class.project  
        return None

    @project.setter
    def project(self, value: SOMcreator.SOMProject) -> None:
        super(SOMPropertySet, self.__class__).project.__set__(self, value)