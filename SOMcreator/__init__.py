from .classes import PropertySet, Object, Project, Attribute, Aggregation, UseCase, Phase
from .external_software import desite, allplan, revit, vestra, card1
from .constants import json_constants, value_constants
from .tools import merge_projects
from .core import export_excel as excel

__version__ = "1.7.7"
active_project = None
