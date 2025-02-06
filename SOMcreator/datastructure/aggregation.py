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
                 optional: None | bool = None, filter_matrix: list[list[bool]] = None,identity_text = None):

        super(Aggregation, self).__init__(obj.name, description, optional, obj.project, filter_matrix)
        self._registry.add(self)
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = str(uuid)
        self.object = obj
        self._parent: Aggregation | None = None
        self._parent_connection = parent_connection
        self._identity_text = "" if identity_text is None else identity_text
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

    def identity(self) -> str:
        """
        Generate a unique identifier for the aggregation group.

        This method constructs an identifier string by traversing the parent
        hierarchy of the current aggregation object. It includes the abbreviation
        of each parent object and its identity text, if available. The identifier
        is built in a reversed order, starting from the root to the current object.

        Returns:
            str: A unique identifier string for the aggregation group.
        """
        
        abbrev_list = list()

        def iter_id(element: Aggregation):
            if element.parent_connection in (SOMcreator.value_constants.AGGREGATION,
                                             SOMcreator.value_constants.AGGREGATION + SOMcreator.value_constants.INHERITANCE) or element.is_root:
                abbrev_list.append((element.object.abbreviation,element.get_identity_text() or "xxx"))
            if not element.is_root:
                iter_id(element.parent)

        iter_id(self)
        return "_".join([f'{abbrev}_{{{txt}}}' for  abbrev,txt in reversed(abbrev_list)])

    
    def get_identity_text(self) -> str:
        return str(self._identity_text)
    
    def set_identity_text(self, text:str):
        """
        Sets the identity text for the object.

        Args:
            text (str): The identity text to be set.
        """
        self._identity_text = text