from __future__ import annotations
from uuid import uuid4
import SOMcreator
from .base import Hirarchy
import copy as cp
import logging
from ifcopenshell.util.unit import get_unit_name_universal


class Attribute(Hirarchy):
    _registry: set[Attribute] = set()

    def __init__(
        self,
        property_set: SOMcreator.PropertySet | None = None,
        name: str = "undef",
        value: list = None,
        value_type: str | None = None,
        data_type: str = SOMcreator.value_constants.LABEL,
        child_inherits_values: bool = False,
        uuid: str = None,
        description: None | str = None,
        optional: None | bool = None,
        revit_mapping: None | str = None,
        project: SOMcreator.Project | None = None,
        filter_matrix: list[list[bool]] = None,
        unit=None,
    ):

        super(Attribute, self).__init__(
            name, description, optional, project, filter_matrix
        )
        self._value = value
        self._property_set = property_set
        self._value_type = value_type
        self._data_type = data_type
        self._unit = unit
        self._registry.add(self)
        if revit_mapping is None:
            self._revit_name = name
        else:
            self._revit_name = revit_mapping

        self._child_inherits_values = child_inherits_values
        self.uuid = uuid

        if self.uuid is None:
            self.uuid = str(uuid4())
        if value is None:
            self.value = list()
        if value_type is None:
            self._value_type = SOMcreator.value_constants.LIST
        if property_set is not None:
            self.property_set = property_set

    def __str__(self) -> str:
        text = f"{self.property_set.name} : {self.name} = {self.value}"
        return text

    def __lt__(self, other):
        if isinstance(other, Attribute):
            return self.name < other.name
        else:
            return self.name < other

    def __copy__(self) -> Attribute:
        new_attrib = Attribute(
            property_set=None,
            name=self.name,
            value=cp.copy(self.value),
            value_type=cp.copy(self.value_type),
            data_type=cp.copy(self.data_type),
            child_inherits_values=self.child_inherits_values,
            uuid=str(uuid4()),
            description=self.description,
            optional=self.is_optional(ignore_hirarchy=True),
            revit_mapping=self.revit_name,
            project=self.project,
            filter_matrix=self._filter_matrix,
        )

        if self.parent is not None:
            self.parent.add_child(new_attrib)
        return new_attrib

    def get_all_parents(self) -> list[Attribute]:
        parent = self.parent
        if parent is None:
            return []
        return parent.get_all_parents() + [parent]

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
        # ToDo: add request for unlink
        self._name = value
        for child in self.get_children(filter=False):
            child.name = value

    @property
    def is_inheriting_values(self) -> bool:
        if self.parent is None:
            return False
        if self.parent.is_inheriting_values or self.parent.child_inherits_values:
            return True
        return False

    def get_own_values(self):
        """returns values without inherited values"""
        if not self.parent:
            return self._value
        return [v for v in self._value if v not in self.parent.value]

    @property
    def value(self) -> list:
        if self.is_inheriting_values:
            return self.parent.value + self.get_own_values()
        return self._value

    @value.setter
    def value(self, values: list) -> None:
        if self.is_inheriting_values:
            own_values = list()
            for value in values:
                if value not in self.parent.value:
                    own_values.append(value)
            self._value = own_values
        else:
            self._value = values

    @property
    def value_type(self) -> str:
        if self.is_child:
            return self.parent.value_type
        return self._value_type

    @value_type.setter
    def value_type(self, value: str):
        if self.is_child:
            logging.info(
                f"won't overwrite ValueType because Attribute '{self}' is child"
            )
            return
        self._value_type = value
        if self.is_parent:
            for child in self.get_children(filter=False):
                child._value_type = value

    @property
    def data_type(self) -> str:
        """
        IfcSimpleValue -> https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/
        :return:
        """
        if self.is_child:
            return self.parent.data_type
        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> None:
        if self.is_child:
            logging.info(
                f"won't overwrite Datatype because Attribute '{self}' is child"
            )
            return
        self._data_type = value
        if self.is_parent:
            for child in self.get_children(filter=False):
                child._data_type = value

    @property
    def unit(self) -> str:
        if self.is_child:
            return self.parent.unit
        return str(self._unit) if self._unit else None

    @unit.setter
    def unit(self, value: str) -> None:
        if self.is_child:
            logging.info(f"won't overwrite Unit because Attribute '{self}' is child")
            return

        if not value:
            self._unit = None
            return
        name = get_unit_name_universal(value)
        if not name:
            logging.warning(f"Unit '{value}' not found -> no unit asignment possible")
            return
        self._unit = value

        if self.is_parent:
            for child in self.get_children(filter=False):
                child._data_type = value

    @property
    def property_set(self) -> SOMcreator.PropertySet:
        return self._property_set

    @property_set.setter
    def property_set(self, value: SOMcreator.PropertySet) -> None:
        if value is None:
            if self._property_set is None:
                return
            self._property_set.remove_attribute(self)
            return
        if self not in value.get_attributes(filter=False):
            value.add_attribute(self)
        self._property_set = value

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
        else:
            return False

    def delete(self, recursive: bool = False) -> None:
        super(Attribute, self).delete(recursive)
        self.property_set.remove_attribute(self)

    def create_child(self) -> Attribute:
        child = cp.copy(self)
        self.add_child(child)
        return child
