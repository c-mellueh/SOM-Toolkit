from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
from SOMcreator.exporter import bsdd
from SOMcreator.constants import value_constants
import logging
import datetime

DATATYPE_MAPPING = {
    value_constants.LABEL: "String",
    value_constants.INTEGER: "Integer",
    value_constants.BOOLEAN: "Boolean",
    value_constants.REAL: "Real",
    value_constants.DATE: "Time",
}

PROPERTY_KIND_MAPPING = {
    value_constants.FORMAT: "Single",
    value_constants.RANGE: "Range",
    value_constants.LIST: "List",
}


def transform_objects_to_classes(
    dictionary: bsdd.Dictionary,
    objects: list[SOMcreator.SOMClass],
    predefined_psets: list[SOMcreator.SOMPropertySet],
):
    """
    Adds objects and Properties to bsdd.Dictionary
    """
    predefined_properties = [
        a for p in predefined_psets for a in p.get_properties(filter=True)
    ]
    properties = _get_all_properties(objects)
    dictionary.Properties, all_class_properties = _create_properties(
        predefined_properties, properties
    )
    class_dict = _create_classes(objects, all_class_properties, dictionary)
    _iterate_parent_relations(objects, class_dict)
    _iterate_aggregations(objects, class_dict)


def transform_project_to_dict(proj: SOMcreator.SOMProject):
    d = bsdd.Dictionary("", proj.name, proj.name, proj.version, "de-DE", False, False)
    d.License = "MIT"
    d.LicenseUrl = "https://www.mit.edu/~amini/LICENSE.md"
    d.ReleaseDate = str(datetime.datetime.now().replace(microsecond=0).isoformat())
    return d


def _check_for_existance(
    som_property: SOMcreator.SOMProperty, properties: list[bsdd.Property]
) -> bsdd.Property | None:
    new_code = str(som_property.name).lower()
    return {p.Code.lower(): p for p in properties}.get(new_code)


def _create_property(som_property: SOMcreator.SOMProperty) -> bsdd.Property:
    code = str(som_property.name)
    p = bsdd.Property(code, som_property.name)
    p.property = som_property
    p.Definition = som_property.description
    p.DataType = DATATYPE_MAPPING[som_property.data_type]
    if som_property.value_type == value_constants.FORMAT and som_property.allowed_values:
        p.Pattern = "|".join(som_property.allowed_values)
    p.PropertyValueKind = PROPERTY_KIND_MAPPING[som_property.value_type]
    return p


def _find_differences(obj_1: bsdd.Property, obj_2: bsdd.Property) -> dict:
    difference_dict = dict()
    for property_name in obj_1.__annotations__.keys():
        value_1 = getattr(obj_1, property_name)
        value_2 = getattr(obj_2, property_name)
        if value_1 != value_2:
            difference_dict[property_name] = [value_1, value_2]
    return difference_dict


def _create_class_property(
    som_property: SOMcreator.SOMProperty, existing_properties: list[bsdd.Property]
):
    code = str(som_property.name)
    if parent_property := _check_for_existance(som_property, existing_properties):
        pass
    else:
        parent_property = _create_property(som_property)
        existing_properties.append(parent_property)

    class_property = bsdd.ClassProperty(code, parent_property.Code, "")
    (
        class_property.property,
        class_property.Description,
        class_property.PropertySet,
        class_property.IsRequired,
    ) = (
        som_property,
        som_property.description,
        str(som_property.property_set.name),
        not som_property.is_optional(ignore_hirarchy=True),
    )

    if not som_property.allowed_values:
        return class_property
    if som_property.value_type == value_constants.FORMAT:
        class_property.Pattern = som_property.allowed_values[0]
    elif som_property.value_type == value_constants.RANGE:
        class_property.MinInclusive = som_property.allowed_values[0][0]
        class_property.MaxInclusive = som_property.allowed_values[0][1]
    elif som_property.value_type == value_constants.LIST:
        for val in som_property.allowed_values:
            class_property.AllowedValues.append(bsdd.AllowedValue(str(val), str(val)))
    return class_property


def _create_properties(
    predefined_properties: list[SOMcreator.SOMProperty],
    class_properties: list[SOMcreator.SOMProperty],
):
    properties = list()
    for som_property in predefined_properties:
        if old_property := _check_for_existance(som_property, properties):
            new_property = _create_property(som_property)
            if old_property != new_property:
                difference = _find_differences(new_property, old_property)
                logging.warning(
                    f"Property mismatch found! There are two properties with the same code ({new_property.Code}) but different values for 'Property.{'|'.join(difference.keys())}'! -> keeping first property"
                )
                continue
        else:
            new_property = _create_property(som_property)
            properties.append(new_property)
    class_properties = [
        _create_class_property(p, properties) for p in class_properties
    ]
    return properties, class_properties


def _create_class(obj: SOMcreator.SOMClass, d: bsdd.Dictionary):
    c = bsdd.Class(d, str(obj.ident_value), obj.name, "Class")
    c.Description = obj.description
    c.RelatedIfcEntityNamesList = list(obj.ifc_mapping)
    c.CountriesOfUse = ["DE"]
    c.CountryOfOrigin = "DE"
    c.CreatorLanguageIsoCode = "de-DE"
    c.Status = "Active"
    return c


def _create_classes(
    objects: list[SOMcreator.SOMClass], class_properties, dictionary: bsdd.Dictionary
) -> dict[SOMcreator.SOMClass, bsdd.Class]:
    class_property_dict = {p.property: p for p in class_properties}
    class_dict = dict()
    for obj in objects:
        c = _create_class(obj, dictionary)
        class_dict[obj] = c
        c.ClassProperties = [
            class_property_dict[a]
            for p in obj.get_property_sets(filter=True)
            for a in p.get_properties(filter=True)
        ]
    return class_dict


def _create_parent_reference(
    child_obj: SOMcreator.SOMClass,
    parent_obj: SOMcreator.SOMClass,
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    parent_class = class_dict[parent_obj]
    child_class = class_dict[child_obj]
    child_class.ParentClassCode = parent_class.Code


def _iterate_parent_relations(
    objects: list[SOMcreator.SOMClass],
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    def _iterate(obj: SOMcreator.SOMClass):
        for child in obj.get_children(filter=True):
            _create_parent_reference(child, obj, class_dict)
            _iterate(child)

    root_objects = [o for o in objects if o.parent is None]
    for root in root_objects:
        _iterate(root)


def _create_aggregation(
    parent_obj: SOMcreator.SOMClass,
    child_obj: SOMcreator.SOMClass,
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    parent_class = class_dict[parent_obj]
    child_class = class_dict[child_obj]

    part_of_relation = bsdd.ClassRelation("IsPartOf", parent_class.uri())
    part_of_relation.RelatedClassName = parent_class.Name
    child_class.ClassRelations.append(part_of_relation)

    has_part_relation = bsdd.ClassRelation("HasPart", child_class.uri())
    has_part_relation.RelatedClassName = child_class.Name
    parent_class.ClassRelations.append(has_part_relation)


def _iterate_aggregations(
    objects: list[SOMcreator.SOMClass],
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    for obj in objects:
        children = list()
        for aggregation in obj.aggregations:
            for child_aggregation in aggregation.get_children(filter=True):
                child_obj = child_aggregation.object
                if child_obj in children:
                    continue
                children.append(child_obj)
                _create_aggregation(obj, child_obj, class_dict)


def _get_all_properties(object_list: list[SOMcreator.SOMClass]):
    return [
        a
        for o in object_list
        for p in o.get_property_sets(filter=True)
        for a in p.get_properties(filter=True)
    ]
