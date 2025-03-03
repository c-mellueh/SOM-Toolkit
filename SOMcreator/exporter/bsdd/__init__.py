from __future__ import annotations
import SOMcreator
from .datastructure import (
    Dictionary,
    AllowedValue,
    Property,
    PropertyRelation,
    ClassProperty,
    Class,
    ClassRelation,
)
from .transformer import transform_project_to_dict, transform_objects_to_classes
from dataclasses import asdict
import json


def export(project: SOMcreator.SOMProject, path: str):
    dictionary = transform_project_to_dict(project)
    objects = list(project.get_classes(filter=True))
    predefined_psets = list(project.get_predefined_psets(filter=False))
    SOMcreator.exporter.bsdd.transformer.transform_objects_to_classes(
        dictionary, objects, predefined_psets
    )
    export_dict(dictionary, path)
    return


def export_dict(dictionary: Dictionary, path: str):
    with open(path, "w") as file:
        d = asdict(
            dictionary, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        json.dump(d, file, indent=2)
