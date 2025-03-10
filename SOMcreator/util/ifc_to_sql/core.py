from __future__ import annotations
import os, tempfile
from typing import Type, TYPE_CHECKING
import logging
from SOMcreator import SOMProject
import ifcopenshell
from ifcopenshell.util import element

if TYPE_CHECKING:
    from SOMcreator.util.sql.tool import ParseSQL
    from SOMcreator.util.ifc_to_sql.tool import IfcToSQL


def import_ifc_files(
    proj: SOMProject,
    main_pset_name: str,
    main_property_name: str,
    ifc_paths: list[os.PathLike],
    db_path,
    parse_sql: Type[ParseSQL],
    ifctosql: Type[IfcToSQL],
):
    db_path = parse_sql.create_database(db_path, ifctosql.create_tables)
    ifctosql.set_project_name(proj.name)
    parse_sql.connect_to_data_base(db_path)
    ifctosql.set_main_property(main_pset_name, main_property_name)
    for ifc_path in ifc_paths:
        ifctosql.set_ifc_file_name(os.path.basename(ifc_path))
        logging.debug(f"Import {os.path.basename(ifc_path)}")
        ifctosql.set_ifc(ifcopenshell.open(ifc_path))
        logging.debug("Import Done")
        _import_entities(ifctosql)
    parse_sql.disconnect_from_data_base()


def _import_entities(ifctosql: Type[IfcToSQL]):
    ifc = ifctosql.get_ifc()
    pset_name, property_name = ifctosql.get_main_property()
    for entity in ifc.by_type("IfcObject"):
        identifier = element.get_pset(entity, pset_name, property_name)
        if not identifier:
            continue
        ifctosql.db_create_entity(entity, identifier)
        _import_properties(entity, ifctosql)


def _import_properties(entity: ifcopenshell.entity_instance, ifctosql: Type[IfcToSQL]):
    properties = element.get_psets(entity)
    for pset_name, property_dict in properties.items():
        if pset_name == "Identity Data":
            continue
        for property_name, value in property_dict.items():
            ifctosql.db_create_property(
                entity, pset_name, property_name, value, "Test"
            )
