from __future__ import annotations
import logging
from typing import TYPE_CHECKING
from desiteRuleCreator.data import classes,constants
if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow

def export_ifc_template(path:str) -> None:
    def transform_datatype(data_type:str) -> str:
        if data_type == constants.XS_INT:
            return "Integer"
        if data_type == constants.XS_STRING:
            return "Label"
        if data_type == constants.XS_DOUBLE:
            return "Real"
        if data_type == constants.XS_BOOL:
            return  "Boolean"
        return "ERROR"

    with open(path,"w") as file:
        property_set: classes.PropertySet
        for property_set in classes.PropertySet:

            obj = property_set.object
            if obj is not None:

                file.write(f"PropertySet:   {property_set.name} I  {','.join(property_set.ifc_mapping)} \n")
                for attribute in property_set.attributes:
                    revit_datatype= transform_datatype(attribute.data_type)
                    file.write(f"   {attribute.name}    {revit_datatype}\n")
                file.write("\n")

