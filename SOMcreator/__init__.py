from .constants import value_constants
from .datastructure import Object
from .datastructure import PropertySet, Attribute, Aggregation, UseCase, Phase, Project

from .io import desite
from .util.project import merge_projects
from .io.excel.core import export as export_excel

__version__ = "1.8.0"
active_project = None
