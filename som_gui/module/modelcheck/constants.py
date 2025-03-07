IDENT_PROPERTY_SET_ISSUE = 1
IDENT_PROPERTY_ISSUE = 2
IDENT_PROPERTY_UNKNOWN = 3
GUID_ISSUE = 4
PROPERTY_SET_ISSUE = 5
PROPERTY_EXIST_ISSUE = 6
PROPERTY_VALUE_ISSUES = 7
PARENT_ISSUE = 8
SUBGROUP_ISSUE = 9  # Gruppe besitzt verschiedene Untergruppen
EMPTY_GROUP_ISSUE = 10
NO_GROUP_ISSUE = 11
REPETETIVE_GROUP_ISSUE = 12
DATATYPE_ISSUE = 13

ISSUE_PATH = "issue_path"
ISSUE_TABLE_HEADER = [
    "GUID_ZWC",
    "GUID",
    "creation_date",
    "short_description",
    "issue_type",
    "PropertySet",
    "Attribut",
    "Value",
]
ISSUE_TABLE_DATATYPES = [
    "CHAR(64)",
    "CHAR(64)",
    "TEXT",
    "TEXT",
    "INT",
    "TEXT",
    "TEXT",
    "TEXT",
]
ENTITY_TABLE_HEADER = [
    "GUID_ZWC",
    "GUID",
    "Name",
    "Project",
    "ifc_type",
    "x_pos",
    "y_pos",
    "z_pos",
    "datei",
    "bauteilKlassifikation",
]
ENTITY_TABLE_DATATYPES = [
    "CHAR(64)",
    "CHAR(64)",
    "TEXT",
    "TEXT",
    "TEXT",
    "DOUBLE",
    "DOUBLE",
    "DOUBLE",
    "TEXT",
    "TEXT",
]
