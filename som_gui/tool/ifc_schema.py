from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import logging


from som_gui.module.ifc_schema.constants import PSD, VERSION_TYPE, QTO
import json

if TYPE_CHECKING:
    from som_gui.module.ifc_schema.prop import IfcSchemaProperties


class IfcSchema(som_gui.core.tool.IfcSchema):
    @classmethod
    def get_properties(cls) -> IfcSchemaProperties:
        return som_gui.IfcSchemaProperties  # type: ignore

    @classmethod
    def set_active_versions(cls, versions: set[VERSION_TYPE]):
        cls.get_properties().active_versions = versions

    @classmethod
    def get_active_versions(cls):
        return cls.get_properties().active_versions

    @classmethod
    def get_resource_folder_path(cls):
        from som_gui.resources.data.ifc import PATH

        return PATH

    @classmethod
    def get_all_psets(cls, version: VERSION_TYPE) -> set[str]:
        allowed_psets: set[str] = set()
        folder_path = os.path.join(cls.get_resource_folder_path(), version, PSD)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Version {version} not found")
        allowed_psets.update(
            {os.path.splitext(fn)[0] for fn in os.listdir(folder_path)}
        )
        return allowed_psets

    @classmethod
    def get_property_sets_of_class(
        cls, class_name: str, version: str, predefined_type: str | None = None
    ) -> set[str]:
        p = cls.get_resource_folder_path()
        with open(os.path.join(p, version, "parent.json"), "r") as f:
            parent_dict = json.load(f)

        with open(os.path.join(p, version, "pset_class.json"), "r") as f:
            property_dict = json.load(f)
        sets: set[str] = set()
        for c in parent_dict.get(class_name, []):
            sets.update(set(property_dict.get(c, set())))
        if predefined_type is not None:
            sets.update(
                set(property_dict.get(f"{class_name}/{predefined_type}", set()))
            )
        return sets

    @classmethod
    def get_property_set_path(
        cls, property_set_name: str, version: VERSION_TYPE
    ) -> str:
        path = cls.get_resource_folder_path()
        if property_set_name.startswith("Pset"):
            path = os.path.join(path, version, PSD)
        elif property_set_name.startswith("Qto"):
            path = os.path.join(path, version, QTO)
        else:
            raise ValueError(
                f"PropertySet '{property_set_name}' doesn't exist in IFC Specification"
            )

        file_path = os.path.join(path, f"{property_set_name}.xml")
        if not os.path.exists(file_path):
            raise ValueError(
                f"PropertySet '{property_set_name}' doesn't exist in {version}"
            )
        return file_path

    @classmethod
    def get_properties_by_pset_name(
        cls, property_set_name: str, version: VERSION_TYPE
    ) -> set[str]:
        file_path = cls.get_property_set_path(property_set_name, version)
        etree = ET.parse(file_path)
        definitions = etree.find("PropertyDefs")
        if definitions is None:
            return set()
        definitions = [property_def.find("Name") for property_def in definitions]
        names = {n.text for n in definitions if n is not None and n.text is not None}
        return names

    @classmethod
    def get_property_data(
        cls, property_set_name: str, property_name: str, version: VERSION_TYPE
    ) -> tuple[str, str, str]:
        def _get_property_def(name: str) -> Element[str]:
            for property_def in etree.getroot().find("PropertyDefs") or []:
                n = property_def.find("Name")
                n = n.text if n is not None else ""
                if n == name:
                    return property_def
            raise ValueError(
                f"Property '{property_name}' doesn't exist in PropertySet '{property_set_name}'"
            )

        def _get_type() -> str:
            missing_datype_error = ValueError(
                f"Property '{property_set_name}:{property_name}' has no Datatype"
            )
            property_type = definition.find("PropertyType")
            if property_type is None:
                raise missing_datype_error
            if len(property_type) > 1:
                raise ValueError(
                    f"Property '{property_set_name}:{property_name}' has multiple ValueTypes"
                )
            t = property_type[0]
            if t.tag != "TypePropertySingleValue":
                logging.info(f"ValueType {t.tag} unknown")
                return "IfcLabel"
            dt = t.find("DataType")
            if dt is None:
                raise missing_datype_error
            dt_value = dt.get("type")
            if dt_value is None:
                raise missing_datype_error
            return dt_value

        file_path = cls.get_property_set_path(property_set_name, version)
        etree = ET.parse(file_path)
        definition = _get_property_def(property_name)

        name = definition.find("Name")
        name = name.text if name is not None and name.text is not None else ""

        description = definition.find("Definition")
        description = (
            description.text
            if description is not None and description.text is not None
            else ""
        )
        datatype = _get_type()
        return (name, description, datatype)
