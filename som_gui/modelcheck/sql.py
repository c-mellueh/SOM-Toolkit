import datetime
import re
import sqlite3

from ifcopenshell import entity_instance

from . import issues

guids = dict()


def sql_command(func):
    def inner(data_base, *args, **kwargs):
        if isinstance(data_base, str):
            conn = sqlite3.connect(data_base)
            cursor = conn.cursor()
            value = func(cursor, *args, **kwargs)
            conn.commit()
            conn.close()
        elif isinstance(data_base, sqlite3.Cursor):
            cursor = data_base
            value = func(cursor, *args, **kwargs)
        else:
            raise AttributeError(f"Wrong input type: {type(data_base)}")
        return value

    return inner


@sql_command
def remove_existing_issues(cursor, project_name, creation_date, file_name):
    query = f"""
    DELETE FROM issues
    WHERE short_description in (
    SELECT short_description from issues
    INNER JOIN entities  on issues.GUID = entities.GUID
    where issues.creation_date = '{creation_date}'
    AND entities.Project = '{project_name}'
    AND entities.datei = '{file_name}')
    """
    cursor.execute(query)


@sql_command
def create_tables(cursor):
    # entities
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS entities
              ([GUID_ZWC] CHAR(64) PRIMARY KEY,[GUID] CHAR(64),[Name] CHAR(64),[Project] TEXT, [ifc_type] TEXT,[x_pos] DOUBLE,
              [y_pos] DOUBLE,[z_pos] DOUBLE,[datei] TEXT,[bauteilKlassifikation] TEXT)
              ''')

    # issues
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS issues
              ([creation_date] TEXT,[GUID] CHAR(64), [short_description] TEXT,[issue_type] INT,
              [PropertySet] TEXT, [Attribut] TEXT)
              ''')


@sql_command
def add_issues(cursor, guid, description, issue_type, attribute, pset_name="", attribute_name=""):
    guid = transform_guid(guid, True)
    date = datetime.date.today()
    if attribute is not None:
        pset_name = attribute.property_set.name
        attribute_name = attribute.name
    cursor.execute(f'''
          INSERT INTO issues (creation_date,GUID,short_description,issue_type,PropertySet,Attribut)
                VALUES
                ('{date}','{guid}','{description}',{issue_type},'{pset_name}','{attribute_name}')
          ''')


def transform_guid(guid: str, add_zero_width: bool):
    """Fügt Zero Width Character ein weil PowerBI (WARUM AUCH IMMER FÜR EIN BI PROGRAMM?????) Case Insensitive ist"""
    if add_zero_width:
        return re.sub(r"([A-Z])", lambda m: m.group(0) + u"\u200B", guid)
    else:
        return guid


@sql_command
def db_create_entity(cursor, element: entity_instance, project, file_name, bauteil_klasse):
    guid_zwc = transform_guid(element.GlobalId, True)
    guid = transform_guid(element.GlobalId, False)
    name = element.Name
    ifc_type = element.is_a()
    center = [0, 0, 0]
    if guid in guids:
        if file_name != guids[guid]:
            issues.guid_issue(cursor, guid, file_name, guids[guid])
        return
    else:
        guids[guid] = file_name
    try:
        cursor.execute(f'''
                  INSERT INTO entities (GUID_ZWC,GUID,Name,Project,ifc_type,x_pos,y_pos,z_pos,datei,bauteilKlassifikation)
                        VALUES
                        ('{guid_zwc}','{guid}','{name}','{project}','{ifc_type}',{center[0]},{center[1]},{center[2]},'{file_name}','{bauteil_klasse}')
                  ''')
    except sqlite3.IntegrityError:
        print("Integrity Error -> Element allready exists")
        pass


@sql_command
def query_issues(cursor: sqlite3.Cursor) -> list:
    cursor.execute(
        "SELECT i.creation_date, e.GUID,i.short_description,i.issue_type,e.Name,i.PropertySet,i.Attribut, e.datei, e.bauteilKlassifikation  FROM issues AS i JOIN entities e on i.GUID = e.GUID_ZWC")

    query = cursor.fetchall()
    return query
