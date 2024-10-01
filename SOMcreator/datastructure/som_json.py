from __future__ import annotations
from typing import TypedDict


class StandardDict(TypedDict):
    name: str
    optional: bool
    filter_matrix: list[list[bool]] | int
    parent: str | None
    description: str


class MainDict(TypedDict):
    Project: ProjectDict
    PredefinedPropertySets: dict[str, PropertySetDict]
    Objects: dict[str, ObjectDict]
    Aggregations: dict[str, AggregationDict]
    AggregationScenes: dict[str, AggregationScene]
    FilterMatrixes: list[tuple[tuple[bool]]]

class ProjectDict(TypedDict):
    name: str
    author: str
    version: str
    AggregationAttributeName: str
    AggregationPsetName: str
    active_phases: list[int]  # was current_project_phase
    active_usecases: list[int]
    ProjectPhases: list[FilterDict]
    UseCases: list[FilterDict]
    filter_matrix: list[list[bool]]


class ObjectDict(StandardDict):
    IfcMappings: list[str]
    abbreviation: str
    ident_attribute: str
    PropertySets: dict[str, PropertySetDict]


class PropertySetDict(StandardDict):
    Attributes: dict[str, AttributeDict]


class AttributeDict(StandardDict):
    data_type: str
    value_type: str
    child_inherits_value: bool
    revit_mapping: str
    Value: list[str] | list[float] | list[[float, float]]


class AggregationDict(StandardDict):
    Object: str | None
    connection: int


class AggregationScene(TypedDict):
    Nodes: list[str]


class FilterDict(TypedDict):
    name: str
    long_name: str
    description: str


DESCRIPTION = "description"
OPTIONAL = "optional"
CURRENT_PR0JECT_PHASE = "current_project_phase"  # deprecated
CURRENT_USE_CASE = "current_use_case"  # deprecated
PROJECT_PHASES = "ProjectPhases"
USE_CASES = "UseCases"
FILTER_MATRIX = "filter_matrix"
FILTER_MATRIXES = "FilterMatrixes"
AGGREGATION_PSET = "AggregationPsetName"
AGGREGATION_ATTRIBUTE = "AggregationAttributeName"
PREDEFINED_PSETS = "PredefinedPropertySets"
PROPERTY_SETS = "PropertySets"
IDENT_ATTRIBUTE = "ident_attribute"
ATTRIBUTES = "Attributes"
OBJECT = "Object"
OBJECTS = "Objects"
AGGREGATIONS = "Aggregations"
NAME = "name"
PARENT = "parent"
DATA_TYPE = "data_type"
VALUE_TYPE = "value_type"
CHILD_INHERITS_VALUE = "child_inherits_value"
PROJECT = "Project"
VERSION = "version"
AUTHOR = "author"
X_POS = "x_pos"
Y_POS = "y_pos"
CONNECTION = "connection"
IFC_MAPPINGS = "IfcMappings"
IFC_MAPPING = "IfcMapping"
ABBREVIATION = "abbreviation"
REVIT_MAPPING = "revit_mapping"
VALUE = "Value"
IGNORE_PSET = "IFC"
ACTIVE_PHASES = "active_phases"
ACTIVE_USECASES = "active_usecases"
NODES = "Nodes"
INHERITED_TEXT = "Predefined Pset"
