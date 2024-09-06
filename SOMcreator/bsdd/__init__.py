from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .bsdd_dictionary import Dictionary


def export(dictionary: Dictionary, path):
    with open(path, "w") as file:
        json.dump(dictionary.serialize(), file, indent=2)
