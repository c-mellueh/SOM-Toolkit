import SOMcreator
from SOMcreator.module import ParseSQLProperties
from typing import Callable
import os, tempfile, logging
import sqlite3
import re


class ParseSQL:
    @classmethod
    def get_properties(cls) -> ParseSQLProperties:
        return SOMcreator.ParseSQLProperties

    @classmethod
    def transform_guid(cls, guid: str, add_zero_width: bool):
        """Fügt Zero Width Character ein weil PowerBI (WARUM AUCH IMMER FÜR EIN BI PROGRAMM?????) Case Insensitive ist"""
        if add_zero_width:
            return re.sub(r"([A-Z])", lambda m: m.group(0) + u"\u200B", guid)
        else:
            return guid

    @classmethod
    def disconnect_from_data_base(cls):
        cls.get_properties().connection.commit()
        cls.get_properties().connection.close()
        cls.get_properties().connection = None

    @classmethod
    def connect_to_data_base(cls, path):
        conn = sqlite3.connect(path)
        cls.get_properties().connection = conn

    @classmethod
    def get_cursor(cls):
        return cls.get_properties().connection.cursor()

    @classmethod
    def commit_sql(cls):
        con = cls.get_properties().connection
        if con is None:
            return
        con.commit()

    @classmethod
    def get_database_path(cls) -> str:
        return cls.get_properties().database_path

    @classmethod
    def set_database_path(cls, path: str):
        cls.get_properties().database_path = path

    @classmethod
    def create_database(cls, db_path, create_table_function: Callable):
        if not db_path:
            db_path = os.path.abspath(tempfile.NamedTemporaryFile(suffix=".db").name)
        cls.set_database_path(db_path)
        logging.info(f"Database: {db_path}")

        cls.connect_to_data_base(db_path)
        create_table_function()
        cls.disconnect_from_data_base()
        return db_path
