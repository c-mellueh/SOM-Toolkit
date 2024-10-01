from .constants import value_constants
from .datastructure import Object
from .datastructure import PropertySet, Attribute, Aggregation, UseCase, Phase, Project

from .external_software import desite
from .util.project import merge_projects
from .core import export_excel as excel

__version__ = "1.8.0"
active_project = None
