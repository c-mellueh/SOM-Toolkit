from __future__ import annotations

from typing import TYPE_CHECKING, IO, Iterator

import SOMcreator
from SOMcreator.constants import value_constants

if TYPE_CHECKING:
    pass


def _transform_datatype(data_type: str, data_type_dict: dict[str, str]) -> str:
    if not data_type in data_type_dict:
        return "ERROR"
    return data_type_dict[data_type]


def export_ifc_template(
    path: str, pset_dict: dict[str, tuple[list[SOMcreator.SOMProperty], set[str]]]
) -> None:
    with open(path, "w") as file:
        property_set: SOMcreator.SOMPropertySet
        for pset_name, (attrib_list, ifc_mapping) in sorted(pset_dict.items()):
            file.write(f"PropertySet:   {pset_name} I  {','.join(ifc_mapping)} \n")
            for som_property in attrib_list:
                revit_datatype = _transform_datatype(
                    som_property.data_type, value_constants.REVIT_TEMPLATE_DATATYPE_DICT
                )
                file.write(f"   {som_property.name}    {revit_datatype}\n")
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

    def __init__(self, property_set_name:str, som_property:SOMcreator.SOMProperty, pset_number):
        self.__class__.add_item(self)
        self.property_set_name:str = property_set_name
        self.som_property:SOMcreator.SOMProperty = som_property
        self.pset_number:int = pset_number

    def output(self, file: IO):
        file.write(
            f"PARAM	{self.som_property.uuid}	{self.som_property.name}	{self.datatype()}		{self.pset_number}	1		1\n"
        )

    def datatype(self) -> str:
        return _transform_datatype(
            self.som_property.data_type, value_constants.REVIT_SHARED_PARAM_DATATYPE_DICT
        )


def export_shared_parameters(
    path: str, pset_dict: dict[str, (list[SOMcreator.SOMProperty], set[str])]
) -> None:
    with open(path, "w") as file:
        file.write(
            "# This is a Revit shared parameter file.\n"
            "# Do not edit manually.\n"
            "*META	VERSION	MINVERSION\n"
            "META	2	1\n"
            "*GROUP	ID	NAME\n"
        )

        for i, pset_name in enumerate(sorted(pset_dict.keys())):
            file.write(f"GROUP	{i + 1}	{pset_name}\n")

        file.write(
            "*PARAM	GUID	NAME	DATATYPE	DATACATEGORY	GROUP	VISIBLE	DESCRIPTION	USERMODIFIABLE\n"
        )

        property_set: SOMcreator.SOMPropertySet
        for i, (pset_name, (attrib_list, ifc_mapping)) in enumerate(
            sorted(pset_dict.items())
        ):
            for attrib in attrib_list:
                t = SP_Item(pset_name, attrib, i)

        for item in sorted(SP_Item, key=lambda x: x.som_property.name):
            item.output(file)
            pass
