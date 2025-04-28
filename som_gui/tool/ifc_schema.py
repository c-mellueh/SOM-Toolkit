from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Literal
import som_gui.core.tool
import som_gui
import os
import xml.etree.ElementTree as ET

from som_gui.module.ifc_schema.constants import PSD, VERSION_TYPE, QTO
import json

if TYPE_CHECKING:
    from som_gui.module.ifc_schema.prop import IfcSchemaProperties

VERSIONS = Literal["open", "closed", "pending"]


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
    def get_all_psets(cls, version: VERSIONS) -> set[str]:
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
    def get_properties_by_pset_name(
        cls, property_set_name: str, version: str
    ) -> set[str]:
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
        etree = ET.parse(file_path)
        definitions = etree.find("PropertyDefs")
        if definitions is None:
            return set()
        definitions = [property_def.find("Name") for property_def in definitions]
        names = {n.text for n in definitions if n is not None and n.text is not None}
        return names
