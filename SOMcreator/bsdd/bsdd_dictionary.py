from dataclasses import dataclass, field
from datetime import datetime
from .bsdd_class import Class
import json
import os


@dataclass
class Dictionary:
    OrganizationCode: str = field(init=True)
    DictionaryCode: str = field(init=True)
    DictionaryName: str = field(init=True)
    DictionaryVersion: str = field(init=True)
    LanguageIsoCode: str = field(init=True)
    LanguageOnly: bool = field(init=True)
    UseOwnUri: bool = field(init=True)
    DictionaryUri: str = field(init=False, default=None)
    License: str = field(init=False, default=None)
    LicenseUrl: str = field(init=False, default=None)
    ChangeRequestEmailAddress: str = field(init=False, default=None)
    ModelVersion: str = field(init=False, default="2.0")
    MoreInfoUrl: str = field(init=False, default=None)
    QualityAssuranceProcedure: str = field(init=False, default=None)
    QualityAssuranceProcedureUrl: str = field(init=False, default=None)
    ReleaseDate: datetime = field(init=False, default=None)
    Status: str = field(init=False, default=None)
    Classes = []
    Properties = []

    @classmethod
    def attributes(cls):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, "language.json"), "r") as f:
            language_json = json.load(f)
        return [
            ['OrganizationCode', str, None],
            ['DictionaryCode', str, None],
            ['DictionaryName', str, None],
            ['DictionaryVersion', str, None],
            ['LanguageIsoCode', str, [x.get("IsoCode") for x in language_json]],
            ['LanguageOnly', bool, None],
            ['UseOwnUri', bool, None],
            ['DictionaryUri', str, None],
            ['License', str, None],
            ['LicenseUrl', str, None],
            ['ChangeRequestEmailAddress', str, None],
            ['ModelVersion', str, ["1.0", "2.0"]],
            ['MoreInfoUrl', str, None],
            ['QualityAssuranceProcedure', str, None],
            ['QualityAssuranceProcedureUrl', str, None],
            ['ReleaseDate', str, None],
            ['Status', str, ["Preview", "Active", "Inactive"]],
        ]

    @classmethod
    def nested_classes(cls):
        return ['Classes', 'Properties']

    @property
    def mapping(self):
        mapping = {name: getattr(self, name) for name, datatype, preset in Dictionary.attributes()}
        nested_classes = {name: [x.serialize() for x in getattr(self, name)] for name in Dictionary.nested_classes()}
        mapping.update(nested_classes)
        return mapping

    def serialize(self):
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict

    def add_class(self, value: Class):
        self.Classes.append(value)
        value.dictionary = self

    def base(self) -> str:
        if self.UseOwnUri:
            return self.DictionaryUri
        return "https://identifier.buildingsmart.org"

    def uri(self) -> str:
        duri = self.base()
        orga_code = self.OrganizationCode
        dict_code = self.DictionaryCode
        version = self.DictionaryVersion
        return "/".join([duri, "uri", orga_code, f"{dict_code}/{version}"])
