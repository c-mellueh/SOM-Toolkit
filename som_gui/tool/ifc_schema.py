
from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import lxml
import som_gui.core.tool
import som_gui
import os
from som_gui.module.ifc_schema.constants import PSD,IFC4,IFC4_3,QTO
if TYPE_CHECKING:
    from som_gui.module.ifc_schema.prop import IfcSchemaProperties


class IfcSchema(som_gui.core.tool.IfcSchema):
    @classmethod
    def get_properties(cls) -> IfcSchemaProperties:
        return som_gui.IfcSchemaProperties

    @classmethod
    def set_active_versions(cls,versions:set[str]):
        cls.get_properties().active_versions = versions

    @classmethod
    def get_active_versions(cls):
        return cls.get_properties().active_versions

    @classmethod
    def get_resource_folder_path(cls):
        from som_gui.resources.data.ifc import PATH
        return PATH

    @classmethod
    def get_all_psets(cls):
        versions = cls.get_active_versions()
        allowed_psets = set()
        for version in versions:
            folder_path = os.path.join(cls.get_resource_folder_path(),version,PSD)
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"Version {version} not found")
            allowed_psets.update({os.path.splitext(fn)[0] for fn in os.listdir(folder_path)})
        return allowed_psets

