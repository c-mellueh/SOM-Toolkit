from __future__ import annotations
from typing import TypedDict


class StandardDict(TypedDict):
    name: str
    optional: bool
    filter_matrix: list[list[bool]]
    parent: str | None
    description: str


class MainDict(TypedDict):
    Project: ProjectDict
    PredefinedPropertySets: dict[str, PropertySetDict]
    Objects: dict[str, ObjectDict]
    Aggregations: dict[str, AggregationDict]
    AggregationScenes: dict[str, AggregationScene]


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
    x_pos: float
    y_pos: float


class AggregationScene(TypedDict):
    Nodes: list[str]


class FilterDict(TypedDict):
    name: str
    long_name: str
    description: str
