from .ifc_datatypes import LABEL, REAL, BOOLEAN, DATE, INTEGER,IFC_DATATYPES

AGGREGATION = 1
INHERITANCE = 2

VALUE = "Value"
FORMAT = "Format"
RANGE = "Range"
LIST = "List"
SHARED_PARAMETERS = "SharedParameters"
EXISTS = "Exists"
VALUE_TYPES= [FORMAT,RANGE, LIST] # VALUE: "Value",

# DATATYPES
DATA_TYPES = IFC_DATATYPES
NUMBER_DATATYPES = [REAL, INTEGER]

# Datatype Mappings
OLD_DATATYPE_DICT = {"xs:string":  LABEL,
                     "xs:double":  REAL,
                     "xs:boolean": BOOLEAN,
                     "xs:long":    REAL,
                     "xs:int":     INTEGER}
XS_DATATYPE_DICT = {
    LABEL:   "xs:string",
    REAL:    "xs:double",
    BOOLEAN: "xs:boolean",
    INTEGER: "xs:int"
}
REVIT_TEMPLATE_DATATYPE_DICT = {INTEGER: "Integer",
                                LABEL:   "Label",
                                REAL:    "Real",
                                BOOLEAN: "Boolean",
                                DATE:    "Date"}

REVIT_SHARED_PARAM_DATATYPE_DICT = {INTEGER: "INTEGER",
                                    LABEL:   "TEXT",
                                    REAL:    "NUMBER",
                                    BOOLEAN: "YESNO",
                                    DATE:    "DATE"}
DATATYPE_DICT = {
    LABEL:   str,
    BOOLEAN: bool,
    INTEGER: int,
    REAL:    float
}

IDENTITY_PLACEHOLDER = "xxx"