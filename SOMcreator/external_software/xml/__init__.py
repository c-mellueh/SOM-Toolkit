from SOMcreator.constants.ifc_datatypes import LABEL, REAL, BOOLEAN, INTEGER, DATE

DATA_TYPE_MAPPING_DICT = {

    LABEL:   "xs:string",
    REAL:    "xs:double",
    BOOLEAN: "xs:boolean",
    INTEGER: "xs:int",
    DATE:    "xs:date",
}


def transform_data_format(data_format: str) -> str:
    """

    :param data_format: value like IfcLabel, IfcDate, IfcReal
    :return: xml_data_type
    """
    val = DATA_TYPE_MAPPING_DICT.get(data_format) or "xs:string"
    return val
