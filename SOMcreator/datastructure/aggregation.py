from __future__ import annotations
from uuid import uuid4
import SOMcreator
from .base import Hirarchy


class Aggregation(Hirarchy):
    _registry: set[Aggregation] = set()

    def __str__(self):
        return self.name

    def __init__(self, obj: SOMcreator.Object, parent_connection=SOMcreator.value_constants.AGGREGATION,
                 uuid: str | None = None,
                 description: None | str = None,
                 optional: None | bool = None, filter_matrix: list[list[bool]] = None):

        super(Aggregation, self).__init__(obj.name, description, optional, obj.project, filter_matrix)
        self._registry.add(self)
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = str(uuid)
        self.object = obj
        self._parent: Aggregation | None = None
        self._parent_connection = parent_connection
        self.object.add_aggregation(self)

    def delete(self, recursive: bool = False) -> None:
        super(Aggregation, self).delete(recursive)

        self.object.remove_aggregation(self)
        if not self.is_root:
            self.parent.remove_child(self)

    @property
    def project(self) -> SOMcreator.Project | None:
        return self.object.project

    @property
    def parent_connection(self):
        if self.parent is None:
            return None
        return self._parent_connection

    @parent_connection.setter
    def parent_connection(self, value):
        self._parent_connection = value

    @property
    def parent(self) -> Aggregation:
        return self._parent

    def set_parent(self, value, connection_type):
        if self.parent is not None and value != self.parent:
            return False
        self._parent = value
        self._parent_connection = connection_type
        return True

    def add_child(self, child: Aggregation, connection_type: int = SOMcreator.value_constants.AGGREGATION) -> bool:
        """returns if adding child is allowed"""

        def loop_parents(element, search_value):
            if element.parent is None:
                return True
            if element.parent.object == search_value:
                return False
            else:
                return loop_parents(element.parent, search_value)

        if child.object == self.object:
            return False

        if not loop_parents(self, child.object):
            return False

        if not child.set_parent(self, connection_type):
            return False

        self._children.add(child)
        child.parent_connection = connection_type
        return True

    @property
    def is_root(self):
        if self.parent is None:
            return True
        return False

    def id_group(self) -> str:
        abbrev_list = list()

        def iter_id(element: Aggregation):
            if element.parent_connection in (SOMcreator.value_constants.AGGREGATION,
                                             SOMcreator.value_constants.AGGREGATION + SOMcreator.value_constants.INHERITANCE):
                abbrev_list.append(element.parent.object.abbreviation)
            if not element.is_root:
                iter_id(element.parent)

        if self.is_root:
            return ""

        iter_id(self)
        return "_xxx_".join(reversed(abbrev_list)) + "_xxx"

    def identity(self) -> str:
        return self.id_group() + "_" + self.object.abbreviation + "_xxx"
