from typing import Literal,get_args

IFC4_TYPE = Literal["IFC4"]
IFC4_3_TYPE = Literal["IFC4_3"]
IFC4 = get_args(IFC4_TYPE)[0]
IFC4_3 = get_args(IFC4_3_TYPE)[0]
VERSION_TYPE = Literal[IFC4_TYPE,IFC4_3_TYPE]
PSD = "psd"
QTO = "qto"

APPDATA_SECTION  = "ifc_schema"
VERSION_OPTION = "versions"
PREDEFINED_SPLITTER = "/"