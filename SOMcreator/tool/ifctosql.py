from SOMcreator.module.ifctosql import IfcToSQLProperties
import SOMcreator
import sqlite3
from SOMcreator import tool
from ifcopenshell import entity_instance
import ifcopenshell
import logging
import datetime


class IfcToSQL():

    @classmethod
    def set_ifc(cls, ifc: ifcopenshell.file):
        cls.get_properties().ifc = ifc

    @classmethod
    def get_ifc(cls, ) -> ifcopenshell.file:
        return cls.get_properties().ifc

    @classmethod
    def set_main_attribute(cls, pset_name, attribute_name):
        cls.get_properties().main_attribute = (pset_name, attribute_name)

    @classmethod
    def get_main_attribute(cls):
        return cls.get_properties().main_attribute

    @classmethod
    def set_project_name(cls, name: str):
        cls.get_properties().project_name = name

    @classmethod
    def set_ifc_file_name(cls, name: str):
        cls.get_properties().ifc_file_name = name

    @classmethod
    def get_properties(cls) -> IfcToSQLProperties:
        return SOMcreator.IfcToSQLProperties

    @classmethod
    def create_tables(cls):
        cursor = tool.ParseSQL.get_cursor()
        # entities
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS entities
                  ([GUID_ZWC] CHAR(64) PRIMARY KEY,[GUID] CHAR(64),[Name] CHAR(64),[Project] TEXT, [ifc_type] TEXT,[x_pos] DOUBLE,
                  [y_pos] DOUBLE,[z_pos] DOUBLE,[datei] TEXT,[bauteilKlassifikation] TEXT)
                  ''')
        tool.ParseSQL.commit_sql()
        # issues
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS attribute
                  ([creation_date] TEXT,[GUID] CHAR(64), [PropertySet] TEXT,[Attribut] TEXT,
                  [Value] TEXT, [Type] TEXT)
                  ''')
        tool.ParseSQL.commit_sql()

    @classmethod
    def db_create_entity(cls, entity: entity_instance, bauteil_klasse):
        cursor = tool.ParseSQL.get_cursor()
        file_name = cls.get_properties().ifc_file_name
        project = cls.get_properties().project_name
        guid_zwc = tool.ParseSQL.transform_guid(entity.GlobalId, True)
        guid = tool.ParseSQL.transform_guid(entity.GlobalId, False)
        name = entity.Name
        ifc_type = entity.is_a()
        center = [0, 0, 0]
        guids = cls.get_properties().guids
        if guid in guids:
            return
        else:
            guids[guid] = file_name
        try:
            cursor.execute(f'''
                      INSERT INTO entities (GUID_ZWC,GUID,Name,Project,ifc_type,x_pos,y_pos,z_pos,datei,bauteilKlassifikation)
                            VALUES
                            ('{guid_zwc}','{guid}','{name}','{project}','{ifc_type}',{center[0]},{center[1]},{center[2]},'{file_name}','{bauteil_klasse}')
                      ''')
            tool.ParseSQL.commit_sql()
        except sqlite3.IntegrityError:
            logging.warning("Integrity Error -> Element allready exists")
            pass

    @classmethod
    def db_create_attribute(cls, entity, pset_name, attribute_name, value, data_type):
        guid = entity.GlobalId
        cursor = tool.ParseSQL.get_cursor()
        date = datetime.date.today()

        cursor.execute(f'''
                          INSERT INTO attribute (creation_date, GUID, PropertySet, Attribut, Value, Type)
                                VALUES
                                ('{date}','{guid}','{pset_name}','{attribute_name}','{value}','{data_type}')
                          ''')
        tool.ParseSQL.commit_sql()
