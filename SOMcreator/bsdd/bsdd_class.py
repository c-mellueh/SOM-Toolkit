from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from .bsdd_property import ClassProperty

if TYPE_CHECKING:
    from .bsdd_dictionary import Dictionary


@dataclass
class Class:
    Code: str = field(init=True)
    Name: str = field(init=True)
    ClassType: str = field(init=True)
    Definition: str = field(init=False, default=None)
    Description: str = field(init=False, default=None)
    ParentClassCode: str = field(init=False, default=None)
    RelatedIfcEntityNamesList: list[str] = field(init=False, default=None)
    Synonyms: list[str] = field(init=False, default=None)
    ActivationDateUtc: datetime = field(init=False, default=None)
    ReferenceCode: str = field(init=False, default=None)
    CountriesOfUse: list[str] = field(init=False, default=None)
    CountryOfOrigin: str = field(init=False, default=None)
    CreatorLanguageIsoCode: str = field(init=False, default=None)
    DeActivationDateUtc: datetime = field(init=False, default=None)
    DeprecationExplanation: str = field(init=False, default=None)
    DocumentReference: str = field(init=False, default=None)
    OwnedUri: str = field(init=False, default=None)
    ReplacedObjectCodes: list[str] = field(init=False, default=None)
    ReplacingObjectCodes: list[str] = field(init=False, default=None)
    RevisionDateUtc: datetime = field(init=False, default=None)
    RevisionNumber: int = field(init=False, default=None)
    Status: str = field(init=False, default=None)
    SubdivisionsOfUse: list[str] = field(init=False, default=None)
    Uid: str = field(init=False, default=None)
    VersionDateUtc: datetime = field(init=False, default=None)
    VersionNumber: int = field(init=False, default=None)
    VisualRepresentationUri: str = field(init=False, default=None)
    ClassProperties: list[ClassProperty] = field(init=True, default_factory=list)
    ClassRelations: list[ClassRelation] = field(init=True, default_factory=list)
    dictionary: Dictionary = field(init=False, default=None)

    @classmethod
    def attributes(cls):
        return [
            ['Code', str, None],
            ['Name', str, None],
            ['ClassType', str, None],
            ['Definition', str, None],
            ['Description', str, None],
            ['ParentClassCode', str, None],
            ['RelatedIfcEntityNamesList', list, None],
            ['Synonyms', list, None],
            ['ActivationDateUtc', datetime, None],
            ['ReferenceCode', str, None],
            ['CountriesOfUse', list, None],
            ['CountryOfOrigin', str, None],
            ['CreatorLanguageIsoCode', str, None],
            ['DeActivationDateUtc', datetime, None],
            ['DeprecationExplanation', str, None],
            ['DocumentReference', str, None],
            ['OwnedUri', str, None],
            ['ReplacedObjectCodes', list, None],
            ['ReplacingObjectCodes', list, None],
            ['RevisionDateUtc', datetime, None],
            ['RevisionNumber', int, None],
            ['Status', str, None],
            ['SubdivisionsOfUse', list, None],
            ['Uid', str, None],
            ['VersionDateUtc', datetime, None],
            ['VersionNumber', int, None],
            ['VisualRepresentationUri', str, None],

        ]

    @classmethod
    def nested_classes(cls):
        return ['ClassProperties', 'ClassRelations']

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in Class.attributes()}
        nested_classes = {name: [x.serialize() for x in getattr(self, name)] for name in Class.nested_classes()}
        mapping.update(nested_classes)
        return mapping

    def serialize(self):
        data_dict = dict()
        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict

    def uri(self):
        return "/".join([self.dictionary.uri(), "class", self.Code])


@dataclass
class ClassRelation:
    RelationType: str = field(init=True)
    RelatedClassUri: str = field(init=True)
    RelatedClassName: str = field(init=False, default=None)
    Fraction: float = field(init=False, default=None)
    OwnedUri: str = field(init=False, default=None)

    @classmethod
    def attributes(cls):
        return [
            ['RelationType', str, None],
            ['RelatedClassUri', str, None],
            ['RelatedClassName', str, None],
            ['Fraction', float, None],
            ['OwnedUri', str, None],
        ]

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in ClassRelation.attributes()}
        return mapping

    def serialize(self) -> dict:
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict
