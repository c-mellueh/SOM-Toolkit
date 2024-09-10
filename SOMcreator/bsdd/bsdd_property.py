from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Property:
    Code: str = field(init=True)
    Name: str = field(init=True)
    Definition: str = field(init=False, default=None)
    Description: str = field(init=False, default=None)
    DataType: str = field(init=False, default=None)
    Units: list[str] = field(init=False, default=None)
    Example: str = field(init=False, default=None)
    ActivationDateUtc: datetime = field(init=False, default=None)
    ConnectedPropertyCodes: list[str] = field(init=False, default=None)
    CountriesOfUse: list[str] = field(init=False, default=None)
    CountryOfOrigin: str = field(init=False, default=None)
    CreatorLanguageIsoCode: str = field(init=False, default=None)
    DeActivationDateUtc: datetime = field(init=False, default=None)
    DeprecationExplanation: str = field(init=False, default=None)
    Dimension: str = field(init=False, default=None)
    DimensionLength: int = field(init=False, default=None)
    DimensionMass: int = field(init=False, default=None)
    DimensionTime: int = field(init=False, default=None)
    DimensionElectricCurrent: int = field(init=False, default=None)
    DimensionThermodynamicTemperature: int = field(init=False, default=None)
    DimensionAmountOfSubstance: int = field(init=False, default=None)
    DimensionLuminousIntensity: int = field(init=False, default=None)
    DocumentReference: str = field(init=False, default=None)
    DynamicParameterPropertyCodes: list[str] = field(init=False, default=None)
    IsDynamic: bool = field(init=False, default=None)
    MaxExclusive: float = field(init=False, default=None)
    MaxInclusive: float = field(init=False, default=None)
    MinExclusive: float = field(init=False, default=None)
    MinInclusive: float = field(init=False, default=None)
    MethodOfMeasurement: str = field(init=False, default=None)
    OwnedUri: str = field(init=False, default=None)
    Pattern: str = field(init=False, default=None)
    PhysicalQuantity: str = field(init=False, default=None)
    PropertyValueKind: str = field(init=False, default=None)
    ReplacedObjectCodes: list[str] = field(init=False, default=None)
    ReplacingObjectCodes: list[str] = field(init=False, default=None)
    RevisionDateUtc: datetime = field(init=False, default=None)
    RevisionNumber: int = field(init=False, default=None)
    Status: str = field(init=False, default=None)
    SubdivisionsOfUse: list[str] = field(init=False, default=None)
    TextFormat: str = field(init=False, default=None)
    Uid: str = field(init=False, default=None)
    VersionDateUtc: datetime = field(init=False, default=None)
    VersionNumber: int = field(init=False, default=None)
    VisualRepresentationUri: str = field(init=False, default=None)
    PropertyRelations: list[PropertyRelation] = field(init=True, default_factory=list)
    AllowedValues: list[AllowedValue] = field(init=True, default_factory=list)

    @classmethod
    def attributes(cls):
        return [
            ['Code', str, None],
            ['Name', str, None],
            ['Definition', str, None],
            ['Description', str, None],
            ['DataType', str, None],
            ['Units', list, None],
            ['Example', str, None],
            ['ActivationDateUtc', datetime, None],
            ['ConnectedPropertyCodes', list, None],
            ['CountriesOfUse', list, None],
            ['CountryOfOrigin', str, None],
            ['CreatorLanguageIsoCode', str, None],
            ['DeActivationDateUtc', datetime, None],
            ['DeprecationExplanation', str, None],
            ['Dimension', str, None],
            ['DimensionLength', int, None],
            ['DimensionMass', int, None],
            ['DimensionTime', int, None],
            ['DimensionElectricCurrent', int, None],
            ['DimensionThermodynamicTemperature', int, None],
            ['DimensionAmountOfSubstance', int, None],
            ['DimensionLuminousIntensity', int, None],
            ['DocumentReference', str, None],
            ['DynamicParameterPropertyCodes', list, None],
            ['IsDynamic', bool, None],
            ['MaxExclusive', float, None],
            ['MaxInclusive', float, None],
            ['MinExclusive', float, None],
            ['MinInclusive', float, None],
            ['MethodOfMeasurement', str, None],
            ['OwnedUri', str, None],
            ['Pattern', str, None],
            ['PhysicalQuantity', str, None],
            ['PropertyValueKind', str, None],
            ['ReplacedObjectCodes', list, None],
            ['ReplacingObjectCodes', list, None],
            ['RevisionDateUtc', datetime, None],
            ['RevisionNumber', int, None],
            ['Status', str, None],
            ['SubdivisionsOfUse', list, None],
            ['TextFormat', str, None],
            ['Uid', str, None],
            ['VersionDateUtc', datetime, None],
            ['VersionNumber', int, None],
            ['VisualRepresentationUri', str, None],
        ]

    @classmethod
    def nested_classes(cls):
        return ['PropertyRelations', 'AllowedValues']

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in Property.attributes()}
        nested_classes = {name: [x.serialize() for x in getattr(self, name)] for name in Property.nested_classes()}
        mapping.update(nested_classes)
        return mapping

    def serialize(self):
        data_dict = dict()
        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict

    def __hash__(self) -> int:
        return hash(str(self.serialize()))


@dataclass
class ClassProperty:
    Code: str = field(init=True)
    PropertyCode: str = field(init=True)
    PropertyUri: str = field(init=True)
    Description: str = field(init=False, default=None)
    PropertySet: str = field(init=False, default=None)
    Unit: str = field(init=False, default=None)
    PredefinedValue: str = field(init=False, default=None)
    IsRequired: bool = field(init=False, default=None)
    IsWritable: bool = field(init=False, default=None)
    MaxExclusive: float = field(init=False, default=None)
    MaxInclusive: float = field(init=False, default=None)
    MinExclusive: float = field(init=False, default=None)
    MinInclusive: float = field(init=False, default=None)
    Pattern: str = field(init=False, default=None)
    OwnedUri: str = field(init=False, default=None)
    PropertyType: str = field(init=False, default=None)
    SortNumber: int = field(init=False, default=None)
    Symbol: str = field(init=False, default=None)
    AllowedValues: list[AllowedValue] = field(init=False, default_factory=list)

    @classmethod
    def attributes(cls):
        return [
            ['Code', str, None],
            ['PropertyCode', str, None],
            ['PropertyUri', str, None],
            ['Description', str, None],
            ['PropertySet', str, None],
            ['Unit', str, None],
            ['PredefinedValue', str, None],
            ['IsRequired', bool, None],
            ['IsWritable', bool, None],
            ['MaxExclusive', float, None],
            ['MaxInclusive', float, None],
            ['MinExclusive', float, None],
            ['MinInclusive', float, None],
            ['Pattern', str, None],
            ['OwnedUri', str, None],
            ['PropertyType', str, None],
            ['SortNumber', int, None],
            ['Symbol', str, None],
        ]

    @classmethod
    def nested_classes(cls):
        return ['AllowedValues']

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in ClassProperty.attributes()}
        nested_classes = {name: [x.serialize() for x in getattr(self, name)] for name in ClassProperty.nested_classes()}
        mapping.update(nested_classes)
        return mapping

    def serialize(self) -> dict:
        data_dict = dict()
        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict


@dataclass
class PropertyRelation:
    RelatedPropertyName: str = field(init=False, default=None)
    RelatedPropertyUri: str = field(init=True)
    RelationType: str = field(init=True)
    OwnedUri: str = field(init=False, default=None)

    @classmethod
    def attributes(cls):
        return [['RelatedPropertyName', str, None],
                ['RelatedPropertyUri', str, None],
                ['RelationType', str, None],
                ['OwnedUri', str, None], ]

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in PropertyRelation.attributes()}
        return mapping


    def serialize(self):
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict


@dataclass
class AllowedValue:
    Code: str = field(init=True)
    Value: str = field(init=True)
    Description: str = field(init=False, default=None)
    Uri: str = field(init=False, default=None)
    SortNumber: int = field(init=False, default=None)
    OwnedUri: str = field(init=False, default=None)

    @classmethod
    def attributes(cls):
        return [
            ['Code', str, None],
            ['Value', str, None],
            ['Description', str, None],
            ['Uri', str, None],
            ['SortNumber', int, None],
            ['OwnedUri', str, None], ]

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in AllowedValue.attributes()}
        return mapping

    def serialize(self):
        data_dict = dict()
        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict
