import os, tempfile
from typing import Type
from SOMcreator.tool import ParseSQL, IfcToSQL
import logging
from SOMcreator import Project
import ifcopenshell
from ifcopenshell.util import element


def import_ifc_files(proj: Project, main_pset_name, main_attribute_name, ifc_paths: list[os.PathLike], db_path,
                     parse_sql: Type[ParseSQL], ifctosql: Type[IfcToSQL]):
    db_path = parse_sql.create_database(db_path, ifctosql.create_tables)
    ifctosql.set_project_name(proj.name)
    parse_sql.connect_to_data_base(db_path)
    ifctosql.set_main_attribute(main_pset_name, main_attribute_name)
    for ifc_path in ifc_paths:
        ifctosql.set_ifc_file_name(os.path.basename(ifc_path))
        logging.debug(f"Import {os.path.basename(ifc_path)}")
        ifctosql.set_ifc(ifcopenshell.open(ifc_path))
        logging.debug("Import Done")
        _import_entities(ifctosql)
    parse_sql.disconnect_from_data_base()


def _import_entities(ifctosql: Type[IfcToSQL]):
    ifc = ifctosql.get_ifc()
    pset_name, attribute_name = ifctosql.get_main_attribute()
    for entity in ifc.by_type("IfcObject"):
        identifier = element.get_pset(entity, pset_name, attribute_name)
        if not identifier:
            continue
        ifctosql.db_create_entity(entity, identifier)
        _import_attributes(entity, ifctosql)


def _import_attributes(entity: ifcopenshell.entity_instance, ifctosql: Type[IfcToSQL]):
    properties = element.get_psets(entity)
    for pset_name, attribute_dict in properties.items():
        if pset_name == "Identity Data":
            continue
        for attribute_name, value in attribute_dict.items():
            ifctosql.db_create_attribute(entity, pset_name, attribute_name, value, "Test")
