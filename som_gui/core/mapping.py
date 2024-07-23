from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool


def open_window(mapping: Type[tool.Mapping]):
    window = mapping.get_window()
    window.show()


def export_revit_ifc_mapping(mapping: Type[tool.Mapping]):
    pass


def export_revit_shared_parameters(mapping: Type[tool.Mapping]):
    pass


def update_object_tree(mapping: Type[tool.Mapping], project: Type[tool.Project]):
    pass


def update_pset_tree(mapping: Type[tool.Mapping]):
    pass
