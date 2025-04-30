from __future__ import annotations

from typing import TYPE_CHECKING, Type
import SOMcreator
from som_gui.module.class_ import constants
import copy as cp
import uuid
import logging

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.class_.prop import ClassDataDict


def init(
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
    main_window: Type[tool.MainWindow],
):
    # Add Class Activate Functions
    def rewrite_label(som_class: SOMcreator.SOMClass | None):
        label = main_window.get_class_name_label()
        if som_class is None:
            label.setText("")
        else:
            label.setText(som_class.name)

    class_tool.connect_signals()
    main_window.signaller.change_active_class.connect(rewrite_label)
    # Add Creation Checks
    class_tool.add_class_creation_check(
        "ident_property_name", class_info.is_ident_property_valid
    )
    class_tool.add_class_creation_check("ident_value", class_info.is_identifier_unique)
    class_tool.signaller.class_deleted.connect(lambda c: logging.debug(f"Class Deleted: {c}") )

def modify_class(
    som_class: SOMcreator.SOMClass,
    data_dict: ClassDataDict,
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
    property_set: Type[tool.PropertySet],
    main_window: Type[tool.MainWindow],
    ifc_schema:Type[tool.IfcSchema],
):

    data_dict = class_info.generate_datadict()
    identifer = data_dict.get("ident_value")
    pset_name = data_dict.get("ident_pset_name")
    property_name = data_dict.get("ident_property_name")
    ident_value = data_dict.get("ident_value")
    is_group = (
        som_class.is_concept
        if data_dict.get("is_group") is None
        else data_dict.get("is_group")
    )

    # check if identifier is allowed
    if not class_tool.is_identifier_allowed(identifer, som_class.ident_value, is_group):
        class_tool.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle Plugin checks
    result = class_info.are_plugin_requirements_met(som_class, data_dict)
    if result != constants.OK:
        class_tool.handle_property_issue(result)
        return
    ifc_version = ifc_schema.get_newest_version(ifc_schema.get_active_versions())
    ifc_mappings = property_set.get_ifc_names(som_class.ifc_mapping[ifc_version],ifc_version)
    if not is_group and property_name and pset_name:
        pset = som_class.get_property_set_by_name(pset_name)
        if not pset:
            # create identifier property_set
            parent,mode = property_set.search_for_parent(pset_name,som_class,ifc_mappings)
            if mode == 0:
                return
            elif mode in (1,2):
                pset = property_set.create_property_set(pset_name, som_class, parent)
            elif mode == 3:
                pset = parent
                som_class.add_property_set(pset)
            else:
                pset = property_set.create_property_set(pset_name, som_class)

        ident_property = pset.get_property_by_name(property_name)
        if not ident_property:
            # create ident property
            ident_property = SOMcreator.SOMProperty(
                name=property_name,
            )
            pset.add_property(ident_property)
        ident_property.allowed_values = [ident_value]

    class_tool.modify_class(som_class, data_dict)
    class_info.add_plugin_infos_to_class(som_class, data_dict)
    main_window.signaller.change_active_class.emit(som_class)


def copy_class(
    som_class: SOMcreator.SOMClass,
    data_dict: ClassDataDict,
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
):

    # handle Group
    if data_dict.get("is_group"):
        group = cp.copy(som_class)
        group.identifier_property = uuid.uuid4()
        group.description = data_dict.get("description") or ""
        class_tool.signaller.modify_class.emit(group, data_dict)
        return
    # handle Identifier Value
    ident_value = data_dict.get("ident_value")
    if not class_tool.is_identifier_allowed(ident_value):
        class_tool.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle plugin checks
    result = class_info.are_plugin_requirements_met(som_class, data_dict)
    if result != constants.OK:
        class_tool.handle_property_issue(result)
        return

    new_class = cp.copy(som_class)
    class_tool.signaller.class_created.emit(new_class)
    class_tool.signaller.modify_class.emit(new_class, data_dict)
    

def create_class(
    data_dict: ClassDataDict,
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
    project: Type[tool.Project],
    property_set: Type[tool.PropertySet],
    ifc_schema:Type[tool.IfcSchema],

):
    name = data_dict["name"]
    is_group = data_dict["is_group"]
    identifier = data_dict.get("ident_value")
    pset_name = data_dict.get("ident_pset_name")
    property_name = data_dict.get("ident_property_name")
    description = data_dict.get("description") or ""
    ifc_mappings = data_dict.get("ifc_mappings")
    proj = project.get()
    # handle group
    if is_group:
        new_class = SOMcreator.SOMClass(name, project=proj)
        new_class.description = description
        class_tool.signaller.class_created.emit(new_class)
        return

    # handle identifier
    if not class_tool.is_identifier_allowed(identifier):
        class_tool.handle_property_issue(constants.IDENT_ISSUE)
        return

    # handle plugin checks
    result = class_info.are_plugin_requirements_met(None, data_dict)
    if result != constants.OK:
        class_tool.handle_property_issue(result)
        return
        # create identifier property_set
    ifc_mappings = ifc_mappings[ifc_schema.get_newest_version(ifc_schema.get_active_versions())]

    new_class = SOMcreator.SOMClass(name, project=proj)
    parent_uuid = data_dict.get("parent_uuid")
    if parent_uuid:
        parent_class = proj.get_element_by_uuid(parent_uuid)
        parent_class.add_child(new_class)
    parent_pset,mode = property_set.search_for_parent(pset_name,new_class,ifc_mappings)
    if mode ==0:
        return
    elif mode in (1,2):
        pset = parent_pset.create_child()
    elif mode == 3:
        pset = parent_pset
    else:
        pset = property_set.create_property_set(pset_name)
    
    new_class.description = description
    new_class.add_property_set(pset)
    # create identifier property
    ident_property = pset.get_property_by_name(property_name)
    if not ident_property:
        ident_property = SOMcreator.SOMProperty(
            pset,
            property_name,
        )
    ident_property.allowed_values = [identifier]
    ident_property.project = proj
    class_info.add_plugin_infos_to_class(new_class, data_dict)
    class_tool.modify_class(new_class, data_dict)

    class_tool.signaller.class_created.emit(new_class)