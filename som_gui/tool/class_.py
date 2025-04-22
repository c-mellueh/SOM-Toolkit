from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import logging
from PySide6.QtCore import QCoreApplication, QObject, Signal
import som_gui.core.tool
import som_gui
from som_gui import tool
import SOMcreator
from som_gui.module.class_ import constants, trigger
from som_gui.module.class_.prop import ClassDataDict
import uuid

if TYPE_CHECKING:
    from som_gui.module.class_.prop import ClassProperties


class Signaller(QObject):
    create_class = Signal(ClassDataDict)
    copy_class = Signal(ClassDataDict, ClassDataDict)
    modify_class = Signal(SOMcreator.SOMClass, ClassDataDict)
    class_created = Signal(SOMcreator.SOMClass)
    class_deleted = Signal(SOMcreator.SOMClass)


class Class(som_gui.core.tool.Class):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> ClassProperties:
        return som_gui.ClassProperties

    @classmethod
    def connect_signals(cls):
        cls.signaller.create_class.connect(trigger.create_class_called)
        cls.signaller.copy_class.connect(trigger.copy_class_called)
        cls.signaller.modify_class.connect(trigger.modify_class_called)

    @classmethod
    def group_classes(
        cls, parent: SOMcreator.SOMClass, children: set[SOMcreator.SOMClass]
    ):
        for child in children:
            parent.add_child(child)

    @classmethod
    def handle_property_issue(cls, result: int):
        if result == constants.OK:
            return True
        if result == constants.IDENT_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Identifier exists allready or is not allowed"
            )
        elif result == constants.IDENT_PROPERTY_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Name of Property is not allowed"
            )
        elif result == constants.IDENT_PSET_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Name of PropertySet is not allowed"
            )
        else:
            return False
        logging.debug(text)
        tool.Popups.create_warning_popup(text)
        return False

    @classmethod
    def is_identifier_allowed(
        cls, identifier, ignore: list[str] = None, is_group=False
    ):
        """
        identifier: value which will be checked against all identifiers
        ignore: list of values which will be ignored
        """
        if is_group:
            return True
        if identifier is None:
            return False
        identifiers = cls.get_existing_ident_values()
        if ignore is not None:
            identifiers = list(filter(lambda i: i not in ignore, identifiers))
        if identifier in identifiers or not identifier:
            return False
        else:
            return True

    @classmethod
    def modify_class(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ) -> int:
        som_class.name = data_dict.get("name", som_class.name)
        som_class.ifc_mapping = data_dict.get("ifc_mappings", som_class.ifc_mapping)
        som_class.description = data_dict.get("description", "")

        if data_dict.get("is_group"):
            if not som_class.is_concept:
                som_class.identifier_property = str(uuid.uuid4())
            return

        pset_name = data_dict.get("ident_pset_name")
        identifier_name = data_dict.get("ident_property_name")
        if pset_name and identifier_name:
            ident_property = cls.find_property(som_class, pset_name, identifier_name)
            som_class.identifier_property = (
                ident_property or som_class.identifier_property
            )

        ident_value = data_dict.get("ident_value")
        if ident_value is not None:
            cls.set_ident_value(som_class, ident_value)

    @classmethod
    def create_class(
        cls,
        data_dict: ClassDataDict,
        property_set: SOMcreator.SOMPropertySet,
        identifier_property: SOMcreator.SOMProperty,
    ) -> SOMcreator.SOMClass:
        if data_dict.get("is_group", False):
            ident = str(uuid.uuid4())
            new_class = SOMcreator.SOMClass(data_dict["name"], ident, uuid=ident)
        else:
            new_class = SOMcreator.SOMClass(data_dict["name"], identifier_property)
            new_class.add_property_set(property_set)

        new_class.ifc_mapping = data_dict.get("ifc_mappings") or new_class.ifc_mapping
        return new_class

    @classmethod
    def check_class_creation_input(cls, data_dict: ClassDataDict) -> bool:
        prop = cls.get_properties()
        for key, check_function in prop.class_add_checks:
            if not check_function(data_dict):
                return False
        return True

    @classmethod
    def set_ident_value(cls, som_class: SOMcreator.SOMClass, value: str):
        if som_class.is_concept:
            return
        som_class.identifier_property.allowed_values = [value]

    @classmethod
    def find_property(
        cls, som_class: SOMcreator.SOMClass, pset_name: str, property_name: str
    ):
        pset = som_class.get_property_set_by_name(pset_name)
        if pset is None:
            return None
        return pset.get_property_by_name(property_name)

    @classmethod
    def add_class_creation_check(cls, key, check_function):
        cls.get_properties().class_add_checks.append((key, check_function))

    @classmethod
    def get_existing_ident_values(cls) -> set[str]:
        proj = tool.Project.get()
        ident_values = set()
        for som_class in proj.get_classes(filter=False):
            if som_class.ident_value:
                ident_values.add(som_class.ident_value)
        return ident_values

    @classmethod
    def delete_class(cls, som_class: SOMcreator.SOMClass, recursive: bool):
        def iterate_deletion(c: SOMcreator.SOMClass):
            if recursive:
                for child in list(c.get_children(filter=False)):
                    iterate_deletion(child)
            cls.signaller.class_deleted.emit(c)
            c.delete()

        iterate_deletion(som_class)

    @classmethod
    def inherit_property_set_to_all_children(
        cls, som_class: SOMcreator.SOMClass, property_set: SOMcreator.SOMPropertySet
    ):
        def iter_children(sc:SOMcreator.SOMClass):
            for child_class in sc.get_children(filter=False):
                child_class: SOMcreator.SOMClass
                pset_dict = {p.name: p for p in child_class.get_property_sets(filter=False)}
                child_pset = pset_dict.get(property_set.name)
                if child_pset is None:
                    child_pset = property_set.create_child()
                    child_class.add_property_set(child_pset)
                for som_property in property_set.get_properties(filter=False):
                    new_property = child_pset.get_property_by_name(som_property.name)
                    if not new_property:
                        new_property = som_property.create_child()
                        child_pset.add_property(new_property)
                    else:
                        new_property.parent = som_property
                iter_children(child_class)
        iter_children(som_class)
