from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
from SOMcreator.exporter import bsdd
from SOMcreator.constants import value_constants,ifc_datatypes
import logging
import datetime

STRING = "String"
INTEGER = "Integer"
BOOL = "Boolean"
REAL = "Real"
TIME = "Time"


DATATYPE_MAPPING = {
    value_constants.LABEL: STRING,
    value_constants.INTEGER: INTEGER,
    value_constants.BOOLEAN: BOOL,
    value_constants.REAL: REAL,
    value_constants.DATE: TIME,
    ifc_datatypes.LENGTHMEASURE:REAL,

}

PROPERTY_KIND_MAPPING = {
    value_constants.FORMAT: "Single",
    value_constants.RANGE: "Range",
    value_constants.LIST: "List",
}


def transform_som_class_to_bsdd_class(
    dictionary: bsdd.Dictionary,
    classes: list[SOMcreator.SOMClass],
    predefined_psets: list[SOMcreator.SOMPropertySet],
):
    """
    Adds classes and Properties to bsdd.Dictionary
    """
    predefined_properties = [
        a for p in predefined_psets for a in p.get_properties(filter=True)
    ]
    properties = _get_all_properties(classes)
    dictionary.Properties, all_class_properties = _create_properties(
        predefined_properties, properties
    )
    class_dict = _create_classes(classes, all_class_properties, dictionary)
    _iterate_parent_relations(classes, class_dict)
    _iterate_aggregations(classes, class_dict)


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
    if (
        som_property.value_type == value_constants.FORMAT
        and som_property.allowed_values
    ):
        p.Pattern = "|".join(som_property.allowed_values)
    p.PropertyValueKind = PROPERTY_KIND_MAPPING[som_property.value_type]
    return p


def _find_differences(prop_0: bsdd.Property, prop_1: bsdd.Property) -> dict:
    difference_dict = dict()
    for property_name in prop_0.__annotations__.keys():
        value_1 = getattr(prop_0, property_name)
        value_2 = getattr(prop_1, property_name)
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
            class_property.AllowedValues.append(bsdd.AllowedValue(to_code(val), str(val)))
    return class_property


def to_code(val:str):
    mapping_dict = {
        '"':'c00',
        '#':'c01',
        '%':'c02',
        '/':'c03',
        '\\':'c04',
        ':':'c05',
        '{':'c06',
        '}':'c07',
        '[':'c08',
        ']':'c09',
        '|':'c10',
        ';':'c11',
        '<':'c12',
        '>':'c13',
        '?':'c14',
        '`':'c15',
        '~':'c16',
            }
    result = []

    for char in str(val):
        result.append(mapping_dict.get(char) or char)
    return "".join(result)     


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
    class_properties = [_create_class_property(p, properties) for p in class_properties]
    return properties, class_properties


def _create_class(som_class: SOMcreator.SOMClass, d: bsdd.Dictionary):
    c = bsdd.Class(d, str(som_class.ident_value), som_class.name, "Class")
    c.Definition = som_class.description
    c.RelatedIfcEntityNamesList = list(som_class.ifc_mapping)
    c.CountriesOfUse = ["DE"]
    c.CountryOfOrigin = "DE"
    c.CreatorLanguageIsoCode = "de-DE"
    c.Status = "Active"
    return c


def _create_classes(
    classes: list[SOMcreator.SOMClass], class_properties, dictionary: bsdd.Dictionary
) -> dict[SOMcreator.SOMClass, bsdd.Class]:
    class_property_dict = {p.property: p for p in class_properties}
    class_dict = dict()
    for som_class in classes:
        c = _create_class(som_class, dictionary)
        class_dict[som_class] = c
        c.ClassProperties = [
            class_property_dict[p]
            for pset in som_class.get_property_sets(filter=True)
            for p in pset.get_properties(filter=True)
        ]
    return class_dict


def _create_parent_reference(
    child_class: SOMcreator.SOMClass,
    parent_class: SOMcreator.SOMClass,
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    parent_class = class_dict[parent_class]
    child_class = class_dict[child_class]
    child_class.ParentClassCode = parent_class.Code


def _iterate_parent_relations(
    classes: list[SOMcreator.SOMClass],
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    def _iterate(som_class: SOMcreator.SOMClass):
        for child in som_class.get_children(filter=True):
            _create_parent_reference(child, som_class, class_dict)
            _iterate(child)

    root_classes = [o for o in classes if o.parent is None]
    for root in root_classes:
        _iterate(root)


def _create_aggregation(
    parent_class: SOMcreator.SOMClass,
    child_class: SOMcreator.SOMClass,
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    parent_class = class_dict[parent_class]
    child_class = class_dict[child_class]

    part_of_relation = bsdd.ClassRelation("IsPartOf", parent_class.uri())
    part_of_relation.RelatedClassName = parent_class.Name
    child_class.ClassRelations.append(part_of_relation)

    has_part_relation = bsdd.ClassRelation("HasPart", child_class.uri())
    has_part_relation.RelatedClassName = child_class.Name
    parent_class.ClassRelations.append(has_part_relation)


def _iterate_aggregations(
    classes: list[SOMcreator.SOMClass],
    class_dict: dict[SOMcreator.SOMClass, bsdd.Class],
):
    for som_class in classes:
        children = list()
        for aggregation in som_class.aggregations:
            for child_aggregation in aggregation.get_children(filter=True):
                child_aggregation:SOMcreator.SOMAggregation
                child_class = child_aggregation.som_class
                if child_class in children:
                    continue
                children.append(child_class)
                _create_aggregation(som_class, child_class, class_dict)


def _get_all_properties(classes: list[SOMcreator.SOMClass]):
    return [
        p
        for c in classes
        for pset in c.get_property_sets(filter=True)
        for p in pset.get_properties(filter=True)
    ]
