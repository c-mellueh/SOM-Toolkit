import logging
from typing import Any

from lxml import etree

from . import action as a
from . import condition as c
from . import constants as const


def _write_base(attribute_name: str, pset_name: str, value_type: str) -> (etree.Element, etree.Element):
    """Schreibt basisinfos die für jede Attributregel identisch sind"""
    rule = etree.Element(const.RULE)
    etree.SubElement(rule, const.IFCTYPE).text = const.ANY
    xml_property = etree.SubElement(rule, const.PROPERTY)
    etree.SubElement(xml_property, const.NAME).text = attribute_name
    etree.SubElement(xml_property, const.PSETNAME).text = pset_name
    etree.SubElement(xml_property, const.TYPE).text = const.PROPERTYSET
    etree.SubElement(xml_property, const.VALUETYPE).text = value_type
    etree.SubElement(xml_property, const.UNIT).text = const.NONE
    xml_condition = etree.SubElement(rule, const.CONDITION)
    return rule, xml_condition


def _generate_rule(attribute_name: str, property_set_name: str,
                   value: Any, datatype: str, condition_type: str, action_type: str) -> etree.Element:
    xml_rule, xml_condition = _write_base(attribute_name, property_set_name, datatype)
    etree.SubElement(xml_condition, const.TYPE).text = condition_type
    etree.SubElement(xml_condition, const.VALUE).text = str(value)
    etree.SubElement(etree.SubElement(xml_rule, a.ACTION), const.TYPE).text = action_type
    return xml_rule


def add_if_not_existing(attribute_name: str, pset_name: str, data_type: str) -> list[etree.Element]:
    if data_type == c.DOUBLE:
        c_type = c.NUMERIC_UNDEF
    elif data_type == c.BOOL:
        c_type = c.BOOL_UNDEF
    elif data_type == c.STRING:
        c_type = c.STRING_UNDEF
    else:
        logging.error(f"Datatype {data_type} unknown. Skip Rule")
        return list()
    return [_generate_rule(attribute_name, pset_name, data_type, data_type, c_type,
                           a.ADD)]


def remove_if_not_in_string_list(attribute_name: str, pset_name: str, value_list) -> list[etree.Element]:
    return [_generate_rule(attribute_name, pset_name, ",".join(value_list), c.STRING, c.NOR, a.REMOVE)]


def add_if_not_in_string_list(attribute_name: str, pset_name: str, value_list) -> list[etree.Element]:
    return [_generate_rule(attribute_name, pset_name, ",".join(value_list), c.STRING, c.NOR, a.ADD)]


def remove_if_in_string_list(attribute_name: str, pset_name: str, value_list) -> list[etree.Element]:
    return [_generate_rule(attribute_name, pset_name, ",".join(value_list), c.STRING, c.OR, a.REMOVE)]


def add_if_in_string_list(attribute_name: str, pset_name: str, value_list) -> list[etree.Element]:
    return [_generate_rule(attribute_name, pset_name, ",".join(value_list), c.STRING, c.OR, a.ADD)]


def add_if_outside_of_range(attribute_name: str, pset_name: str, min_value: float, max_value: float) -> \
        list[etree.Element]:
    r1 = _generate_rule(attribute_name, pset_name, min_value, c.DOUBLE, c.LESS, a.ADD)
    r2 = _generate_rule(attribute_name, pset_name, max_value, c.DOUBLE, c.GREATER, a.ADD)
    return [r1, r2]


def add_if_in_range(attribute_name: str, pset_name: str, min_value: float, max_value: float) -> list[etree.Element]:
    r1 = _generate_rule(attribute_name, pset_name, min_value, c.DOUBLE, c.GREATER, a.AND)
    r2 = _generate_rule(attribute_name, pset_name, max_value, c.DOUBLE, c.LESS, a.ADD)
    return [r1, r2]


def numeric_list(attribute_name, pset_name, value_list) -> list[etree.Element]:
    """Schreibt Regel die kontrolliert ob ein Zahlenwert in einer Liste aus Zahlen vorkommt"""
    rule_list: list[etree.Element] = list()
    rule_list += add_if_not_existing(attribute_name, pset_name, c.DOUBLE)
    for index, value in enumerate(value_list):
        if index == len(value_list) - 1:
            xml_rule = _generate_rule(attribute_name, pset_name, value, c.DOUBLE, c.NOTEQ, a.ADD)
        else:
            xml_rule = _generate_rule(attribute_name, pset_name, value, c.DOUBLE, c.NOTEQ, a.AND)
        rule_list.append(xml_rule)
    return rule_list


def merge_list(range_list, start_index=0):
    for i in range(start_index, len(range_list) - 1):
        if range_list[i][1] > range_list[i + 1][0]:
            new_start = range_list[i][0]
            new_end = max(range_list[i + 1][1], range_list[i][1])
            range_list[i] = [new_start, new_end]
            del range_list[i + 1]
            return merge_list(range_list.copy(), start_index=i)
    return range_list


def numeric_range(attribute_name: str, property_set_name: str,
                  value_range_list: list[tuple[float, float]]) -> list[etree.Element]:
    """Schreibt eine Regel die kontrolliert ob ein Zahlenwert in einem Wertebereich vorkommt"""

    if not value_range_list:
        logging.error(f"Empty Value list at {property_set_name}:{attribute_name}")
        return list()

    sorted_range_list = sorted([[min(v1, v2), max(v1, v2)] for [v1, v2] in value_range_list])
    sorted_range_list = merge_list(sorted_range_list)

    minimal_value = sorted_range_list[0][0]
    maximal_value = sorted_range_list[-1][1]

    rule_list = list()
    rule_list += add_if_not_existing(attribute_name, property_set_name, c.DOUBLE)
    rule_list += add_if_outside_of_range(attribute_name, property_set_name, minimal_value, maximal_value)

    for [_, v1_max], [v2_min, _] in zip(sorted_range_list, sorted_range_list[1:]):
        rule_list += add_if_in_range(attribute_name, property_set_name, v1_max, v2_min)
    return rule_list


def remove_if_not_exist(attribute_name: str, property_set_name: str) -> list[etree.Element]:
    return _generate_rule(attribute_name, property_set_name, "", c.STRING, c.ISNOT, a.REMOVE)
