from .constants import value_constants
from .datastructure import SOMClass
from .datastructure import (
    SOMPropertySet,
    SOMProperty,
    SOMAggregation,
    UseCase,
    Phase,
    Project,
)

from .exporter import desite
from .util.project import merge_projects
from .exporter.excel.core import export as export_excel

__version__ = "1.8.2"
active_project = None
