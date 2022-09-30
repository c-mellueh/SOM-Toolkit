from __future__ import annotations

from typing import TYPE_CHECKING, IO, Iterator

from desiteRuleCreator.data import classes, constants

if TYPE_CHECKING:
    pass


def export_ifc_template(path: str, pset_dict: dict[str, (list[classes.Attribute], set[str])]) -> None:
    def transform_datatype(data_type: str) -> str:
        if data_type == constants.XS_INT:
            return "Integer"
        if data_type == constants.XS_STRING:
            return "Label"
        if data_type == constants.XS_DOUBLE:
            return "Real"
        if data_type == constants.XS_BOOL:
            return "Boolean"
        return "ERROR"

    with open(path, "w") as file:
        property_set: classes.PropertySet
        for pset_name, (attrib_list, ifc_mapping) in sorted(pset_dict.items()):
            file.write(f"PropertySet:   {pset_name} I  {','.join(ifc_mapping)} \n")
            for attribute in attrib_list:
                revit_datatype = transform_datatype(attribute.data_type)
                file.write(f"   {attribute.name}    {revit_datatype}\n")
            file.write("\n")


class IterItem(type):
    _registry = set()

    def __iter__(cls) -> Iterator[SP_Item]:
        return iter(cls._registry)

    def add_item(cls, item):
        cls._registry.add(item)

    def __len__(cls):
        return len(cls._registry)

    # def __new__(meta,name,bases,attrs):
    #     attrs['_cars'] = weaker.WeakSet()
    #     return type.__new__(meta, name, bases, attrs)


class SP_Item(metaclass=IterItem):

    def __init__(self, property_set_name, attribute, pset_number):
        self.__class__.add_item(self)
        self.property_set_name = property_set_name
        self.attribute = attribute
        self.pset_number = pset_number

    def print(self, file: IO):
        file.write(
            f"PARAM	{self.attribute.identifier}	{self.attribute.name}	{self.datatype()}		{self.pset_number}	1		1\n")

    def datatype(self) -> str:
        data_type = self.attribute.data_type
        if data_type == constants.XS_INT:
            return "INTEGER"
        if data_type == constants.XS_STRING:
            return "TEXT"
        if data_type == constants.XS_DOUBLE:
            return "NUMBER"
        if data_type == constants.XS_BOOL:
            return "YESNO"
        return "ERROR"


def export_shared_parameters(path: str, pset_dict: dict[str, (list[classes.Attribute], set[str])]) -> None:
    with open(path, "w") as file:
        file.write("# This is a Revit shared parameter file.\n"
                   "# Do not edit manually.\n"
                   "*META	VERSION	MINVERSION\n"
                   "META	2	1\n"
                   "*GROUP	ID	NAME\n")

        for i, pset_name in enumerate(sorted(pset_dict.keys())):
            file.write(f"GROUP	{i + 1}	{pset_name}\n")

        file.write(
            "*PARAM	GUID	NAME	DATATYPE	DATACATEGORY	GROUP	VISIBLE	DESCRIPTION	USERMODIFIABLE\n")

        property_set: classes.PropertySet
        for i, (pset_name, (attrib_list, ifc_mapping)) in enumerate(sorted(pset_dict.items())):
            for attrib in attrib_list:
                t = SP_Item(pset_name, attrib, i)

        for item in sorted(SP_Item, key=lambda x: x.attribute.name):
            item.print(file)
            pass
