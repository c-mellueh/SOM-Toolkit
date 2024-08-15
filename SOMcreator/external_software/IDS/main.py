from __future__ import annotations

import os
from datetime import date

from lxml.etree import Element, ElementTree, SubElement

from . import ids_xsd, xml_xsd
from ... import classes
from ...constants import value_constants, ifc_datatypes
from ..xml import transform_data_format

NSMAP = {None:  ids_xsd.DEFAULT_NS[1:-1],
         "xs":  xml_xsd.NS_XS[1:-1],
         "xsi": xml_xsd.NS_XSI[1:-1]}


def _build_info(proj: classes.Project, author, xml_parent: Element) -> None:
    xml_element = SubElement(xml_parent, ids_xsd.INFO, nsmap=NSMAP)
    SubElement(xml_element, ids_xsd.TITLE, nsmap=NSMAP).text = f"Pruefregeln fuer Projekt '{proj.name}'"
    SubElement(xml_element, ids_xsd.COPYRIGHT, nsmap=NSMAP).text = "None"
    SubElement(xml_element, ids_xsd.VERSION, nsmap=NSMAP).text = f"0.9"
    SubElement(xml_element, ids_xsd.DESCRIPTION, nsmap=NSMAP).text = f"Autogenerated by SOMcreator"
    SubElement(xml_element, ids_xsd.AUTHOR, nsmap=NSMAP).text = str(author)
    SubElement(xml_element, ids_xsd.DATE, nsmap=NSMAP).text = f"{date.today()}"
    SubElement(xml_element, ids_xsd.PURPOSE, nsmap=NSMAP).text = "Modelcheck"


def _build_specifications(required_data, xml_parent: Element) -> None:
    xml_specifications = SubElement(xml_parent, ids_xsd.SPECIFICATIONS, nsmap=NSMAP)

    for obj, property_set_dict in required_data.items():
        if obj.ident_attrib is None:
            continue
        _build_specification(obj, property_set_dict, xml_specifications)


def _build_applicability(obj: classes.Object, xml_parent: Element) -> None:
    xml_applicability = SubElement(xml_parent, ids_xsd.APPLICABILITY, nsmap=NSMAP)
    xml_property = SubElement(xml_applicability, ids_xsd.PROPERTY, nsmap=NSMAP)
    xml_property.set(ids_xsd.ATTR_DATATYPE, ifc_datatypes.LABEL)
    xml_property_set = SubElement(xml_property, ids_xsd.PROPERTYSET, nsmap=NSMAP)
    SubElement(xml_property_set, ids_xsd.SIMPLEVALUE).text = obj.ident_attrib.property_set.name
    xml_name = SubElement(xml_property, ids_xsd.NAME, nsmap=NSMAP)
    SubElement(xml_name, ids_xsd.SIMPLEVALUE, nsmap=NSMAP).text = obj.ident_attrib.name
    xml_value = SubElement(xml_property, ids_xsd.VALUE)
    SubElement(xml_value, ids_xsd.SIMPLEVALUE, nsmap=NSMAP).text = obj.ident_value


def _build_requirements(property_set_dict: dict[classes.PropertySet, list[classes.Attribute]],
                        xml_parent: Element) -> None:
    xml_requirement = SubElement(xml_parent, ids_xsd.REQUIREMENTS, nsmap=NSMAP)
    for property_set, attribute_list in property_set_dict.items():
        for attribute in attribute_list:
            _build_attribute_requirement(attribute, xml_requirement)


def _build_attribute_requirement(attribute: classes.Attribute, xml_parent: Element) -> None:
    xml_property = SubElement(xml_parent, ids_xsd.PROPERTY, nsmap=NSMAP)
    xml_property.set(ids_xsd.ATTR_DATATYPE, attribute.data_type)
    if attribute.optional:
        xml_property.set(xml_xsd.MINOCCURS, "0")
    else:
        xml_property.set(xml_xsd.MINOCCURS, "1")
    xml_property.set(xml_xsd.MAXOCCURS, "1")

    xml_property_set = SubElement(xml_property, ids_xsd.PROPERTYSET)
    SubElement(xml_property_set, ids_xsd.SIMPLEVALUE, nsmap=NSMAP).text = attribute.property_set.name
    xml_name = SubElement(xml_property, ids_xsd.NAME)
    SubElement(xml_name, ids_xsd.SIMPLEVALUE, nsmap=NSMAP).text = attribute.name
    if not attribute.value:
        return
    xml_value = SubElement(xml_property, ids_xsd.VALUE, nsmap=NSMAP)
    xml_restriction = SubElement(xml_value, xml_xsd.RESTRICTION, nsmap=NSMAP)
    xml_restriction.set(xml_xsd.BASE, transform_data_format(attribute.data_type))

    if attribute.value_type == value_constants.LIST:
        for value in attribute.value:
            SubElement(xml_restriction, xml_xsd.ENUMERATION, nsmap=NSMAP).set(xml_xsd.VALUE, str(value))

    if attribute.value_type == value_constants.RANGE:
        min_value = min(min(v[0] for v in attribute.value), min(v[1] for v in attribute.value))
        max_value = max(max(v[0] for v in attribute.value), max(v[1] for v in attribute.value))
        SubElement(xml_restriction, xml_xsd.MININCLUSIVE, nsmap=NSMAP).set(xml_xsd.VALUE, str(min_value))
        SubElement(xml_restriction, xml_xsd.MAXINCLUSIVE, nsmap=NSMAP).set(xml_xsd.VALUE, str(max_value))

    if attribute.value_type == value_constants.FORMAT:
        pattern = "|".join(attribute.value)
        SubElement(xml_restriction, xml_xsd.PATTERN, nsmap=NSMAP).set(xml_xsd.VALUE, pattern)


def _build_specification(obj: classes.Object, property_set_dict: dict[classes.PropertySet, list[classes.Attribute]],
                         xml_parent: Element) -> None:
    xml_specification = SubElement(xml_parent, ids_xsd.SPECIFICATION, nsmap=NSMAP)
    xml_specification.set(ids_xsd.ATTR_NAME, f"Pruefregel {obj.name} ({obj.ident_value})")
    xml_specification.set(ids_xsd.ATTR_IFCVERSION, ids_xsd.VAL_IFC4)
    xml_specification.set(ids_xsd.ATTR_DESCRIPTION, "Automatisch generierte Attributpruefregel")
    xml_specification.set(xml_xsd.MINOCCURS, "0")
    xml_specification.set(xml_xsd.MAXOCCURS, "unbounded")
    _build_applicability(obj, xml_specification)
    _build_requirements(property_set_dict, xml_specification)


def export(proj: classes.Project,
           required_data: dict[classes.Object, dict[classes.PropertySet, list[classes.Attribute]]],
           path: str | os.PathLike, author=None) -> None:
    if not author:
        author = proj.author
    xml_root = Element(ids_xsd.IDS, nsmap=NSMAP)
    xml_root.set(xml_xsd.NS_XSI + xml_xsd.SCHEMALOCATION, ids_xsd.SCHEME_LOCATION_NS)
    _build_info(proj, author, xml_root)
    _build_specifications(required_data, xml_root)
    ElementTree(xml_root).write(path, pretty_print=True, encoding="UTF-8")
