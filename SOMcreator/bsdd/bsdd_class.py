from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from .bsdd_property import ClassProperty

if TYPE_CHECKING:
    from .bsdd_dictionary import Dictionary


@dataclass
class Class:
    code: str = field(init=True)
    name: str = field(init=True)
    class_type: str = field(init=True)
    definition: str = field(init=False, default=None)
    description: str = field(init=False, default=None)
    parent_class_code: str = field(init=False, default=None)
    related_ifc_entity_names_list: list[str] = field(init=False, default=None)
    synonyms: list[str] = field(init=False, default=None)
    activation_date_utc: datetime = field(init=False, default=None)
    reference_code: str = field(init=False, default=None)
    countries_of_use: list[str] = field(init=False, default=None)
    country_of_origin: str = field(init=False, default=None)
    creator_language_iso_code: str = field(init=False, default=None)
    de_activation_date_utc: datetime = field(init=False, default=None)
    deprecation_explanation: str = field(init=False, default=None)
    document_reference: str = field(init=False, default=None)
    owned_uri: str = field(init=False, default=None)
    replaced_object_codes: list[str] = field(init=False, default=None)
    replacing_object_codes: list[str] = field(init=False, default=None)
    revision_date_utc: datetime = field(init=False, default=None)
    revision_number: int = field(init=False, default=None)
    status: str = field(init=False, default=None)
    subdivisions_of_use: list[str] = field(init=False, default=None)
    uid: str = field(init=False, default=None)
    version_date_utc: datetime = field(init=False, default=None)
    version_number: int = field(init=False, default=None)
    visual_representation_uri: str = field(init=False, default=None)
    class_properties: list[ClassProperty] = field(init=False, default=None)
    class_relations: list[ClassRelation] = field(init=False, default=None)
    dictionary: Dictionary = field(init=False, default=None)

    @property
    def mapping(self):
        mapping = {
            'Code':                      self.code,
            'Name':                      self.name,
            'ClassType':                 self.class_type,
            'Definition':                self.definition,
            'Description':               self.description,
            'ParentClassCode':           self.parent_class_code,
            'RelatedIfcEntityNamesList': self.related_ifc_entity_names_list,
            'Synonyms':                  self.synonyms,
            'ActivationDateUtc':         self.activation_date_utc,
            'ReferenceCode':             self.reference_code,
            'CountriesOfUse':            self.countries_of_use,
            'CountryOfOrigin':           self.country_of_origin,
            'CreatorLanguageIsoCode':    self.creator_language_iso_code,
            'DeActivationDateUtc':       self.de_activation_date_utc,
            'DeprecationExplanation':    self.deprecation_explanation,
            'DocumentReference':         self.document_reference,
            'OwnedUri':                  self.owned_uri,
            'ReplacedObjectCodes':       self.replaced_object_codes,
            'ReplacingObjectCodes':      self.replacing_object_codes,
            'RevisionDateUtc':           self.revision_date_utc,
            'RevisionNumber':            self.revision_number,
            'Status':                    self.status,
            'SubdivisionsOfUse':         self.subdivisions_of_use,
            'Uid':                       self.uid,
            'VersionDateUtc':            self.version_date_utc,
            'VersionNumber':             self.version_number,
            'VisualRepresentationUri':   self.visual_representation_uri,
            'ClassProperties':           [c.serialize() for c in self.class_properties],
            'ClassRelations':            [c.serialize() for c in self.class_relations],
        }
        return mapping

    def serialize(self):

        data_dict = dict()
        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict

    def uri(self):
        return "/".join([self.dictionary.uri(), "class", self.code])


@dataclass
class ClassRelation:
    relation_type: str = field(init=True)
    related_class_uri: str = field(init=True)
    related_class_name: str = field(init=False, default=None)
    fraction: float = field(init=False, default=None)
    owned_uri: str = field(init=False, default=None)

    @property
    def mapping(self):
        mapping = {
            'RelationType':     self.relation_type,
            'RelatedClassUri':  self.related_class_uri,
            'RelatedClassName': self.related_class_name,
            'Fraction':         self.fraction,
            'OwnedUri':         self.owned_uri,
        }
        return mapping

    def serialize(self) -> dict:
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict
