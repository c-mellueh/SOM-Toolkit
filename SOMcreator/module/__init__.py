from .ifctosql import IfcToSQLProperties
from .parsesql import ParseSQLProperties
from .export_excel import ExportExcelProperties
import SOMcreator

SOMcreator.ParseSQLProperties = ParseSQLProperties()
SOMcreator.IfcToSQLProperties = IfcToSQLProperties()
SOMcreator.ExportExcelProperties = ExportExcelProperties()
