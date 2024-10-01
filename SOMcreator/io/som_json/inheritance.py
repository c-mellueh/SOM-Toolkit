from __future__ import annotations
import SOMcreator


def _find_parent(uuid_dict, element):
    for test_el, identifier in SOMcreator.io.som_json.parent_dict.items():
        if type(test_el) is not type(element):
            continue
        if identifier not in uuid_dict:
            continue
        if test_el == element:
            continue
        if test_el.parent is not None:
            continue

        if test_el.name != element.name:
            continue

        if isinstance(test_el, SOMcreator.Attribute):
            if test_el.value == element.value:
                return identifier
        return identifier


def calculate(proj: SOMcreator.Project):
    uuid_dict = proj.get_uuid_dict()
    for entity, uuid in SOMcreator.io.som_json.parent_dict.items():
        if uuid is None:
            continue
        if uuid not in uuid_dict:
            uuid = _find_parent(uuid_dict, entity)
        if uuid is None:
            continue
        uuid_dict[uuid].add_child(entity)
