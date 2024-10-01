from .constants import json_constants, value_constants
from .datastructure import Project, Object, PropertySet, Attribute, Aggregation, UseCase, Phase

from .external_software import desite, allplan, revit, vestra, card1
from .tools import merge_projects
from .core import export_excel as excel

__version__ = "1.8.0"
active_project = None
