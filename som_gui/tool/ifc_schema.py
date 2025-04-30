from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
import os

import SOMcreator
from som_gui.module.ifc_schema import ui, trigger
from SOMcreator.datastructure.ifc_schema import VERSION_TYPE, read_jsons
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import QCoreApplication, Qt

if TYPE_CHECKING:
    from som_gui.module.ifc_schema.prop import IfcSchemaProperties


class IfcSchema(som_gui.core.tool.IfcSchema):

    @classmethod
    def get_properties(cls) -> IfcSchemaProperties:
        return som_gui.IfcSchemaProperties  # type: ignore

    @classmethod
    def read_jsons(cls, version):
        read_jsons(version)

    @classmethod
    def set_active_versions(cls, versions: set[VERSION_TYPE]):
        cls.get_properties().active_versions = versions

    @classmethod
    def get_active_versions(
        cls,
    ):
        return cls.get_properties().active_versions

    @classmethod
    def create_mapping_widget(
        cls, som_class: SOMcreator.SOMClass | None, version: VERSION_TYPE
    ):
        if som_class is not None:
            existing_mappings = som_class.ifc_mapping.get(version, dict())
        else:
            existing_mappings = dict()
        widget = ui.MappingWidget(version)
        tv = widget.ui.table_view
        model = QStandardItemModel()
        tv.setModel(model)
        model.insertColumns(0, 2)
        t1 = QCoreApplication.translate("IFC-Mapping", "IFC-Entity")
        t2 = QCoreApplication.translate("IFC-Mapping", "Predefined Type")
        model.setHorizontalHeaderLabels([t1, t2])
        tv.setEditTriggers(tv.EditTrigger.AllEditTriggers)
        tv.setItemDelegate(ui.MappingDelegate(version))
        tv.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        hh = tv.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeMode.Fixed)
        widget.ui.button_add_ifc.pressed.connect(
            lambda: trigger.append_ifc_mapping(widget, "")
        )
        for mapping in existing_mappings:
            trigger.append_ifc_mapping(widget, mapping)
        widget.ui.label_ifc_mapping.setText(version)
        return widget
