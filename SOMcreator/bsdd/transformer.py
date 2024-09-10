import SOMcreator
from SOMcreator import bsdd
from SOMcreator.constants import value_constants
import logging
import datetime

DATATYPE_MAPPING = {
    value_constants.LABEL:   "String",
    value_constants.INTEGER: "Integer",
    value_constants.BOOLEAN: "Boolean",
    value_constants.REAL:    "Real",
    value_constants.DATE:    "Time"
}

PROPERTY_KIND_MAPPING = {
    value_constants.FORMAT: "Single",
    value_constants.RANGE:  "Range",
    value_constants.LIST:   "List",
}


def transform_objects_to_classes(dictionary: bsdd.Dictionary, objects: list[SOMcreator.Object],
                                 predefined_psets: list[SOMcreator.PropertySet]):
    """
    Adds objects and Properties to bsdd.Dictionary
    """
    predefined_attributes = [a for p in predefined_psets for a in p.attributes]
    attributes = _get_all_attributes(objects)
    dictionary.Properties, all_class_properties = _create_properties(predefined_attributes, attributes)
    class_dict = _create_classes(objects, all_class_properties, dictionary)
    _iterate_parent_relations(objects, class_dict)
    _iterate_aggregations(objects, class_dict)


def transform_project_to_dict(proj: SOMcreator.Project):
    d = bsdd.Dictionary("", proj.name, proj.name, proj.version, "de-DE", False, False)
    d.License = "MIT"
    d.LicenseUrl = "https://www.mit.edu/~amini/LICENSE.md"
    d.ReleaseDate = str(datetime.datetime.now().replace(microsecond=0).isoformat())
    return d


def _check_for_existance(attribute: SOMcreator.Attribute,
                         properties: list[bsdd.Property]) -> bsdd.Property | None:
    new_code = str(attribute.name).lower()
    return {p.Code.lower(): p for p in properties}.get(new_code)


def _create_property(attribute: SOMcreator.Attribute) -> bsdd.Property:
    code = str(attribute.name)
    p = bsdd.Property(code, attribute.name)
    p.attribute = attribute
    p.Definition = attribute.description
    p.DataType = DATATYPE_MAPPING[attribute.data_type]
    if attribute.value_type == value_constants.FORMAT and attribute.value:
        p.Pattern = attribute.value[0]
    p.PropertyValueKind = PROPERTY_KIND_MAPPING[attribute.value_type]
    return p


def _find_differences(obj_1: bsdd.Property, obj_2: bsdd.Property) -> dict:
    difference_dict = dict()
    for attribute_name in obj_1.__annotations__.keys():
        value_1 = getattr(obj_1, attribute_name)
        value_2 = getattr(obj_2, attribute_name)
        if value_1 != value_2:
            difference_dict[attribute_name] = [value_1, value_2]
    return difference_dict


def _create_class_property(attribute: SOMcreator.Attribute, existing_properties: list[bsdd.Property]):
    code = attribute.name
    if parent_property := _check_for_existance(attribute, existing_properties):
        pass
    else:
        parent_property = _create_property(attribute)
        print(f"create property: {parent_property.Code}")
        existing_properties.append(parent_property)

    class_property = bsdd.ClassProperty(code, parent_property.Code, "")
    class_property.attribute, class_property.Description, class_property.PropertyType, class_property.IsRequired = (
        attribute, attribute.description, str(attribute.property_set.name), not attribute.optional)

    if not attribute.value:
        return class_property
    if attribute.value_type == value_constants.FORMAT:
        class_property.Pattern = attribute.value[0]
    elif attribute.value_type == value_constants.RANGE:
        class_property.MinInclusive = attribute.value[0][0]
        class_property.MaxInclusive = attribute.value[0][1]
    elif attribute.value_type == value_constants.LIST:
        for val in attribute.value:
            class_property.AllowedValues.append(bsdd.AllowedValue(str(val), str(val)))
    return class_property


def _create_properties(predefined_attribute: list[SOMcreator.Attribute],
                       object_attributes: list[SOMcreator.Attribute]):
    properties = list()
    for attribute in predefined_attribute:
        if old_property := _check_for_existance(attribute, properties):
            new_property = _create_property(attribute)
            if old_property != new_property:
                difference = _find_differences(new_property, old_property)
                logging.warning(
                    f"Property mismatch found! There are two properties with the same code ({new_property.Code}) but different values for {'|'.join(difference.keys())}! -> keeping first property")
                continue
        else:
            new_property = _create_property(attribute)
            properties.append(new_property)
    class_properties = [_create_class_property(p, properties) for p in object_attributes]
    return properties, class_properties


def _create_class(obj: SOMcreator.Object, d: bsdd.Dictionary):
    c = bsdd.Class(str(obj.ident_value), obj.name, "Class")
    c.Description = obj.description
    c.RelatedIfcEntityNamesList = list(obj.ifc_mapping)
    c.CountriesOfUse = ["DE"]
    c.CountryOfOrigin = "DE"
    c.CreatorLanguageIsoCode = "de-DE"
    c.Status = "Active"
    d.add_class(c)
    return c


def _create_classes(objects: list[SOMcreator.Object], class_properties, dictionary: bsdd.Dictionary) -> dict[
    SOMcreator.Object, bsdd.Class]:
    class_property_dict = {p.attribute: p for p in class_properties}
    class_dict = dict()
    for obj in objects:
        c = _create_class(obj, dictionary)
        class_dict[obj] = c
        c.ClassProperties = [class_property_dict[a] for p in obj.property_sets for a in p.attributes]
    return class_dict


def _create_parent_reference(child_obj: SOMcreator.Object, parent_obj: SOMcreator.Object,
                             class_dict: dict[SOMcreator.Object, bsdd.Class]):
    parent_class = class_dict[parent_obj]
    child_class = class_dict[child_obj]
    # has_parent_relation = ClassRelation("IsChildOf", parent_class.uri())
    # has_parent_relation.related_class_name = parent_class.name
    # child_class.class_relations.append(has_parent_relation)
    child_class.parent_class_code = parent_class.Code
    #
    # has_child_relation = ClassRelation("IsParentOf", child_class.uri())
    # has_child_relation.related_class_name = child_class.name
    # parent_class.class_relations.append(has_child_relation)


def _iterate_parent_relations(objects: list[SOMcreator.Object], class_dict: dict[SOMcreator.Object, bsdd.Class]):
    def _iterate(obj: SOMcreator.Object):
        for child in obj.children:
            _create_parent_reference(child, obj, class_dict)
            _iterate(child)

    root_objects = [o for o in objects if o.parent is None]
    for root in root_objects:
        _iterate(root)


def _create_aggregation(parent_obj: SOMcreator.Object, child_obj: SOMcreator.Object,
                        class_dict: dict[SOMcreator.Object, bsdd.Class]):
    parent_class = class_dict[parent_obj]
    child_class = class_dict[child_obj]

    part_of_relation = bsdd.ClassRelation("IsPartOf", parent_class.uri())
    part_of_relation.RelatedClassName = parent_class.Name
    child_class.ClassRelations.append(part_of_relation)

    has_part_relation = bsdd.ClassRelation("HasPart", child_class.uri())
    has_part_relation.RelatedClassName = child_class.Name
    parent_class.ClassRelations.append(has_part_relation)


def _iterate_aggregations(objects: list[SOMcreator.Object], class_dict: dict[SOMcreator.Object, bsdd.Class]):
    for obj in objects:
        children = list()
        for aggregation in obj.aggregations:
            for child_aggregation in aggregation.children:
                child_obj = child_aggregation.object
                if child_obj in children:
                    continue
                children.append(child_obj)
                _create_aggregation(obj, child_obj, class_dict)


def _get_all_attributes(object_list: list[SOMcreator.Object]):
    return [a for o in object_list for p in o.property_sets for a in p.attributes]
