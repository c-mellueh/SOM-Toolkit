from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Property:
    code: str = field(init=True)
    name: str = field(init=True)
    definition: str = field(init=False, default=None)
    description: str = field(init=False, default=None)
    data_type: str = field(init=False, default=None)
    units: list[str] = field(init=False, default=None)
    example: str = field(init=False, default=None)
    activation_date_utc: datetime = field(init=False, default=None)
    connected_property_codes: list[str] = field(init=False, default=None)
    countries_of_use: list[str] = field(init=False, default=None)
    country_of_origin: str = field(init=False, default=None)
    creator_language_iso_code: str = field(init=False, default=None)
    de_activation_date_utc: datetime = field(init=False, default=None)
    deprecation_explanation: str = field(init=False, default=None)
    dimension: str = field(init=False, default=None)
    dimension_length: int = field(init=False, default=None)
    dimension_mass: int = field(init=False, default=None)
    dimension_time: int = field(init=False, default=None)
    dimension_electric_current: int = field(init=False, default=None)
    dimension_thermodynamic_temperature: int = field(init=False, default=None)
    dimension_amount_of_substance: int = field(init=False, default=None)
    dimension_luminous_intensity: int = field(init=False, default=None)
    document_reference: str = field(init=False, default=None)
    dynamic_parameter_property_codes: list[str] = field(init=False, default=None)
    is_dynamic: bool = field(init=False, default=None)
    max_exclusive: float = field(init=False, default=None)
    max_inclusive: float = field(init=False, default=None)
    min_exclusive: float = field(init=False, default=None)
    min_inclusive: float = field(init=False, default=None)
    method_of_measurement: str = field(init=False, default=None)
    owned_uri: str = field(init=False, default=None)
    pattern: str = field(init=False, default=None)
    physical_quantity: str = field(init=False, default=None)
    property_value_kind: str = field(init=False, default=None)
    replaced_object_codes: list[str] = field(init=False, default=None)
    replacing_object_codes: list[str] = field(init=False, default=None)
    revision_date_utc: datetime = field(init=False, default=None)
    revision_number: int = field(init=False, default=None)
    status: str = field(init=False, default=None)
    subdivisions_of_use: list[str] = field(init=False, default=None)
    text_format: str = field(init=False, default=None)
    uid: str = field(init=False, default=None)
    version_date_utc: datetime = field(init=False, default=None)
    version_number: int = field(init=False, default=None)
    visual_representation_uri: str = field(init=False, default=None)
    property_relations: list[PropertyRelation] = field(init=False, default=None)
    allowed_values: list[AllowedValue] = field(init=False, default=None)

    @property
    def mapping(self):
        mapping = {'Code':                              self.code,
                   'Name':                              self.name,
                   'Definition':                        self.definition,
                   'Description':                       self.description,
                   'DataType':                          self.data_type,
                   'Units':                             self.units,
                   'Example':                           self.example,
                   'ActivationDateUtc':                 self.activation_date_utc,
                   'ConnectedPropertyCodes':            self.connected_property_codes,
                   'CountriesOfUse':                    self.countries_of_use,
                   'CountryOfOrigin':                   self.country_of_origin,
                   'CreatorLanguageIsoCode':            self.creator_language_iso_code,
                   'DeActivationDateUtc':               self.de_activation_date_utc,
                   'DeprecationExplanation':            self.deprecation_explanation,
                   'Dimension':                         self.dimension,
                   'DimensionLength':                   self.dimension_length,
                   'DimensionMass':                     self.dimension_mass,
                   'DimensionTime':                     self.dimension_time,
                   'DimensionElectricCurrent':          self.dimension_electric_current,
                   'DimensionThermodynamicTemperature': self.dimension_thermodynamic_temperature,
                   'DimensionAmountOfSubstance':        self.dimension_amount_of_substance,
                   'DimensionLuminousIntensity':        self.dimension_luminous_intensity,
                   'DocumentReference':                 self.document_reference,
                   'DynamicParameterPropertyCodes':     self.dynamic_parameter_property_codes,
                   'IsDynamic':                         self.is_dynamic,
                   'MaxExclusive':                      self.max_exclusive,
                   'MaxInclusive':                      self.max_inclusive,
                   'MinExclusive':                      self.min_exclusive,
                   'MinInclusive':                      self.min_inclusive,
                   'MethodOfMeasurement':               self.method_of_measurement,
                   'OwnedUri':                          self.owned_uri,
                   'Pattern':                           self.pattern,
                   'PhysicalQuantity':                  self.physical_quantity,
                   'PropertyValueKind':                 self.property_value_kind,
                   'ReplacedObjectCodes':               self.replaced_object_codes,
                   'ReplacingObjectCodes':              self.replacing_object_codes,
                   'RevisionDateUtc':                   self.revision_date_utc,
                   'RevisionNumber':                    self.revision_number,
                   'Status':                            self.status,
                   'SubdivisionsOfUse':                 self.subdivisions_of_use,
                   'TextFormat':                        self.text_format,
                   'Uid':                               self.uid,
                   'VersionDateUtc':                    self.version_date_utc,
                   'VersionNumber':                     self.version_number,
                   'VisualRepresentationUri':           self.visual_representation_uri,
                   'PropertyRelations':                 self.property_relations,
                   'AllowedValues':                     self.allowed_values, }
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
    code: str = field(init=True)
    property_code: str = field(init=True)
    property_uri: str = field(init=False, default=None)
    description: str = field(init=False, default=None)
    property_set: str = field(init=False, default=None)
    unit: str = field(init=False, default=None)
    predefined_value: str = field(init=False, default=None)
    is_required: bool = field(init=False, default=None)
    is_writable: bool = field(init=False, default=None)
    max_exclusive: float = field(init=False, default=None)
    max_inclusive: float = field(init=False, default=None)
    min_exclusive: float = field(init=False, default=None)
    min_inclusive: float = field(init=False, default=None)
    pattern: str = field(init=False, default=None)
    owned_uri: str = field(init=False, default=None)
    property_type: str = field(init=False, default=None)
    sort_number: int = field(init=False, default=None)
    symbol: str = field(init=False, default=None)
    allowed_values: list[AllowedValue] = field(init=False, default_factory=list)

    @property
    def mapping(self):
        mapping = {'Code':            self.code,
                   'PropertyCode':    self.property_code,
                   'PropertyUri':     self.property_uri,
                   'Description':     self.description,
                   'PropertySet':     self.property_set,
                   'Unit':            self.unit,
                   'PredefinedValue': self.predefined_value,
                   'IsRequired':      self.is_required,
                   'IsWritable':      self.is_writable,
                   'MaxExclusive':    self.max_exclusive,
                   'MaxInclusive':    self.max_inclusive,
                   'MinExclusive':    self.min_exclusive,
                   'MinInclusive':    self.min_inclusive,
                   'Pattern':         self.pattern,
                   'OwnedUri':        self.owned_uri,
                   'PropertyType':    self.property_type,
                   'SortNumber':      self.sort_number,
                   'Symbol':          self.symbol,
                   'AllowedValues':   [v.serialize() for v in self.allowed_values], }
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
    related_property_name: str
    related_property_uri: str
    relation_type: str
    owned_uri: str

    @property
    def mapping(self):
        mapping = {'RelatedPropertyName': self.related_property_name,
                   'RelatedPropertyUri':  self.related_property_uri,
                   'RelationType':        self.relation_type,
                   'OwnedUri':            self.owned_uri, }
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
    code: str = field(init=True)
    value: str = field(init=True)
    description: str = field(init=False, default=None)
    uri: str = field(init=False, default=None)
    sort_number: int = field(init=False, default=None)
    owned_uri: str = field(init=False, default=None)

    @property
    def mapping(self):
        mapping = {'Code':        self.code,
                   'Value':       self.value,
                   'Description': self.description,
                   'Uri':         self.uri,
                   'SortNumber':  self.sort_number,
                   'OwnedUri':    self.owned_uri, }
        return mapping

    def serialize(self):
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict
