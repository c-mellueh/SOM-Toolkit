from dataclasses import dataclass, field
from datetime import datetime
from .bsdd_class import Class


@dataclass
class Dictionary:
    organization_code: str = field(init=True)
    dictionary_code: str = field(init=True)
    dictionary_name: str = field(init=True)
    dictionary_version: str = field(init=True)
    language_iso_code: str = field(init=True)
    language_only: bool = field(init=True)
    use_own_uri: bool = field(init=True)
    dictionary_uri: str = field(init=False, default=None)
    license: str = field(init=False, default=None)
    license_url: str = field(init=False, default=None)
    model_version: str = field(init=False, default="2.0")
    mori_info_url: str = field(init=False, default=None)
    quality_assurance_procedure: str = field(init=False, default=None)
    quality_assurance_procedure_url: str = field(init=False, default=None)
    release_date: datetime = field(init=False, default=None)
    status: str = field(init=False, default=None)
    classes = []
    properties = []

    @property
    def mapping(self):
        mapping = {
            'Classes':                      [c.serialize() for c in self.classes],
            'DictionaryCode':               self.dictionary_code,
            'DictionaryName':               self.dictionary_name,
            'DictionaryUri':                self.dictionary_uri,
            'DictionaryVersion':            self.dictionary_version,
            'LanguageIsoCode':              self.language_iso_code,
            'LanguageOnly':                 self.language_only,
            'License':                      self.license,
            'LicenseUrl':                   self.license_url,
            'ModelVersion':                 self.model_version,
            'MoriInfoUrl':                  self.mori_info_url,
            'OrganizationCode':             self.organization_code,
            'Properties':                   [p.serialize() for p in self.properties],
            'QualityAssuranceProcedure':    self.quality_assurance_procedure,
            'QualityAssuranceProcedureUrl': self.quality_assurance_procedure_url,
            'ReleaseDate':                  self.release_date,
            'Status':                       self.status,
            'UseOwnUri':                    self.use_own_uri,
        }
        return mapping

    def serialize(self):
        data_dict = dict()

        for key, value in self.mapping.items():
            if value is None:
                continue
            data_dict[key] = value
        return data_dict

    def add_class(self, value: Class):
        self.classes.append(value)
        value.dictionary = self

    def base(self) -> str:
        if self.use_own_uri:
            return self.dictionary_uri
        return "https://identifier.buildingsmart.org"

    def uri(self) -> str:
        duri = self.base()
        orga_code = self.organization_code
        dict_code = self.dictionary_code
        version = self.dictionary_version
        return "/".join([duri, "uri", orga_code, f"{dict_code}/{version}"])
