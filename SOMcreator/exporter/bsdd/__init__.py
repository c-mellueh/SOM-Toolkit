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
from .transformer import transform_project_to_dict, transform_som_class_to_bsdd_class
from dataclasses import asdict
import json
import os


def export(project: SOMcreator.SOMProject, path: str | os.PathLike):
    dictionary = transform_project_to_dict(project)
    classes = list(project.get_classes(filter=True))
    predefined_psets = list(project.get_predefined_psets(filter=False))
    SOMcreator.exporter.bsdd.transformer.transform_som_class_to_bsdd_class(
        dictionary, classes, predefined_psets
    )
    export_dict(dictionary, path)
    return


def export_dict(dictionary: Dictionary, path: str | os.PathLike):
    with open(path, "w") as file:
        d = asdict(
            dictionary, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        json.dump(d, file, indent=2)
