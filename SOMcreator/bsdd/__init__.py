from __future__ import annotations
from typing import TYPE_CHECKING
import json

from .bsdd_dictionary import Dictionary
from .bsdd_class import Class
from .bsdd_property import Property


def export(dictionary: Dictionary, path):
    with open(path, "w") as file:
        json.dump(dictionary.serialize(), file, indent=2)
