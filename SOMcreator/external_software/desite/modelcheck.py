from __future__ import annotations

import codecs
import logging
import os
import uuid
from xml.etree.ElementTree import Element

import jinja2
from lxml import etree
from typing import TypedDict

from . import handle_header, output_date_time
from ...external_software import xml
from ..bim_collab_zoom.rule import merge_list
from ... import classes, constants, Template
from ...constants import json_constants, value_constants

JS_EXPORT = "JS"
TABLE_EXPORT = "TABLE"


class ObjectStructureDict(TypedDict):
    children: set[classes.Object]


def _handle_template(path: str | os.PathLike) -> jinja2.Template:
    file_loader = jinja2.FileSystemLoader(Template.HOME_DIR)
    env = jinja2.Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    template = env.get_template(path)
    return template


def _add_js_rule(parent: Element, file: codecs.StreamReaderWriter) -> str | None:
    name = os.path.basename(file.name)
    if not name.endswith(".js"):
        return None
    else:
        rule_script = etree.SubElement(parent, "ruleScript")

        name = name.split("_")[1:]
        name = "_".join(name)
        rule_script.set("name", name[:-3])
        rule_script.set("active", "true")
        rule_script.set("resume", "false")

        code = etree.SubElement(rule_script, "code")
        file = file.read()

        code.text = file
        code.text = etree.CDATA(code.text)

    return file


def _handle_element_section(xml_qa_export: Element) -> Element:
    xml_element_section = etree.SubElement(xml_qa_export, "elementSection")
    return xml_element_section


def _handle_container(xml_element_section: Element, text) -> Element:
    container = etree.SubElement(xml_element_section, "container")
    container.set("ID", str(uuid.uuid4()))
    container.set("name", text)
    return container


def _handle_checkrun(xml_container: Element, name: str, author: str = "DesiteRuleCreator") -> Element:
    checkrun = etree.SubElement(xml_container, "checkrun")
    _uuid = str(uuid.uuid4())
    checkrun.set("ID", _uuid)
    checkrun.set("name", name)
    checkrun.set("active", "true")
    checkrun.set("user", str(author))
    checkrun.set("date", str(output_date_time))
    checkrun.set("state", "0")
    checkrun.set("objectsOnly", "1")
    checkrun.set("partsOfComposites", "0")
    checkrun.set("createFailed", "true")
    checkrun.set("createWarnings", "true")
    checkrun.set("createIgnored", "true")
    checkrun.set("createPassed", "true")
    checkrun.set("createUndefined", "false")
    return checkrun


def _init_xml(author: str, name: str, version: str) -> (Element, Element):
    xml_qa_export = handle_header(author, "qaExport")
    xml_element_section = _handle_element_section(xml_qa_export)
    text = f"{name} : {version}"
    xml_container = _handle_container(xml_element_section, text)
    return xml_container, xml_qa_export


def _handle_rule(xml_checkrun: Element, rule_type: str) -> Element:
    rule = etree.SubElement(xml_checkrun, "rule")
    rule.set("type", rule_type)
    if rule_type == "UniquePattern":
        etree.SubElement(rule, "patternList")
        code = etree.SubElement(xml_checkrun, "code")
        code.text = ""

    return rule


def _handle_attribute_rule_list(xml_rule: Element) -> Element:
    attribute_rule_list = etree.SubElement(xml_rule, "attributeRuleList")
    return attribute_rule_list


def _define_xml_elements(author: str, xml_container: Element, name: str) -> (Element, Element):
    xml_checkrun = _handle_checkrun(xml_container, name=name, author=author)
    xml_rule = _handle_rule(xml_checkrun, "Attributes")
    xml_attribute_rule_list = _handle_attribute_rule_list(xml_rule)
    _handle_rule(xml_checkrun, "UniquePattern")

    return xml_checkrun, xml_attribute_rule_list


def _handle_js_rules(xml_attribute_rule_list: Element, starts_with: str) -> None:
    folder = os.path.join(Template.HOME_DIR, constants.FILEPATH_JS)

    for fn in os.listdir(folder):
        if str(fn).startswith(starts_with):
            file = codecs.open(f"{folder}/{fn}", encoding="utf-8")
            _add_js_rule(xml_attribute_rule_list, file)


def _handle_rule_script(xml_attribute_rule_list: Element, name: str) -> Element:
    rule_script = etree.SubElement(xml_attribute_rule_list, "ruleScript")
    rule_script.set("name", name)
    rule_script.set("active", "true")
    rule_script.set("resume", "true")
    return rule_script


def _handle_code(xml_rule_script: Element) -> Element:
    code = etree.SubElement(xml_rule_script, "code")
    return code


def _handle_attribute_rule_tree(xml_rule: Element) -> Element:
    attribute_rule_tree = etree.SubElement(xml_rule, "attributeRuleTree")
    return attribute_rule_tree


def _handle_tree_structure(author: str, required_data_dict: dict, parent_xml_container,
                           object_structure: dict[classes.Object, set[classes.Object]], parent_obj: classes.Object,
                           template,
                           xml_object_dict, export_type: str) -> None:
    def check_basics(obj: classes.Object):
        if obj.ident_attrib is None:
            return obj, None, True

        pset_dict = required_data_dict.get(obj)
        if pset_dict is None:
            return obj, None, True
        return obj, pset_dict, False

    def create_container(xml_container):
        new_xml_container = _handle_container(xml_container, parent_obj.name)
        if export_type == JS_EXPORT:
            create_js_object(new_xml_container)
        elif export_type == TABLE_EXPORT:
            create_table_object(new_xml_container)
        children = object_structure.get(parent_obj)
        for child_obj in sorted(children, key=lambda x: x.name):
            _handle_tree_structure(author, required_data_dict, new_xml_container, object_structure, child_obj, template,
                                   xml_object_dict,
                                   export_type)

    def create_js_object(xml_container):
        obj, pset_dict, abort = check_basics(parent_obj)
        if abort:
            return
        xml_checkrun = _handle_checkrun(xml_container, obj.name, author)
        xml_rule = _handle_rule(xml_checkrun, "Attributes")
        xml_attribute_rule_list = _handle_attribute_rule_list(xml_rule)
        xml_rule_script = _handle_rule_script(xml_attribute_rule_list, name=obj.name)
        xml_code = _handle_code(xml_rule_script)
        cdata_code = template.render(pset_dict=pset_dict, constants=value_constants,
                                     ignore_pset=json_constants.IGNORE_PSET, xs_dict=xml.DATA_TYPE_MAPPING_DICT)
        xml_code.text = cdata_code
        _handle_rule(xml_checkrun, "UniquePattern")

        xml_object_dict[xml_checkrun] = obj

    def create_table_object(xml_container):
        obj, pset_dict, abort = check_basics(parent_obj)
        if abort:
            return
        xml_checkrun = _handle_checkrun(xml_container, obj.name, author)
        xml_rule = _handle_rule(xml_checkrun, "Attributes")
        xml_attribute_rule_tree = _handle_attribute_rule_tree(xml_rule)
        xml_code = _handle_code(xml_container)

        _handle_rule_items_by_pset_dict(pset_dict, xml_attribute_rule_tree)
        xml_code.text = "<![CDATA[]]>"
        _handle_rule(xml_checkrun, "UniquePattern")

        xml_object_dict[xml_checkrun] = obj

    if object_structure.get(parent_obj) and required_data_dict.get(parent_obj):
        create_container(parent_xml_container)
    else:
        if export_type == JS_EXPORT:
            create_js_object(parent_xml_container)
        elif export_type == TABLE_EXPORT:
            create_table_object(parent_xml_container)


def _csv_value_in_list(attribute: classes.Attribute):
    return " ".join(f'"{str(val)}"' for val in attribute.value)


def _csv_check_range(attribute: classes.Attribute) -> str:
    sorted_range_list = sorted([[min(v1, v2), max(v1, v2)] for [v1, v2] in attribute.value])
    sorted_range_list = merge_list(sorted_range_list)

    pattern = "||".join(f">={v_min}&&<={v_max}" for v_min, v_max in sorted_range_list)
    return pattern


def _build_basics_rule_item(xml_parent: etree.Element, attribute: classes.Attribute) -> etree.Element:
    xml_attrib = etree.SubElement(xml_parent, "ruleItem")
    xml_attrib.set("ID", attribute.uuid)
    data_type = xml.transform_data_format(attribute.data_type)
    xml_attrib.set("name", f"{attribute.property_set.name}:{attribute.name}##{data_type}")
    xml_attrib.set("type", "simple")
    return xml_attrib


def _handle_rule_item_attribute(xml_parent: etree.Element, attribute: classes.Attribute):
    xml_attrib = _build_basics_rule_item(xml_parent, attribute)

    if not attribute.value:
        xml_attrib.set("pattern", "*")
        return
    pattern = "*"
    if attribute.data_type in (value_constants.INTEGER, value_constants.REAL):
        if attribute.value_type == value_constants.LIST:
            pattern = _csv_value_in_list(attribute)
        elif attribute.value_type == value_constants.RANGE:
            pattern = _csv_check_range(attribute)
        else:
            logging.error(f"No Function defined for {attribute.name} ({attribute.value_type} x {attribute.data_type}")
            pattern = "*"

    elif attribute.data_type == value_constants.LABEL:
        if attribute.value_type == value_constants.FORMAT:
            pattern = " || ".join(attribute.value)
        elif attribute.value_type == value_constants.LIST:
            pattern = " ".join([f'"{v}"' for v in attribute.value])

    elif attribute.data_type == value_constants.BOOLEAN:
        pattern = "*"
    else:
        logging.error(f"No Function defined for {attribute.name} ({attribute.value_type} x {attribute.data_type}")

    xml_attrib.set("pattern", pattern)


def _handle_rule_item_pset(xml_parent: etree.Element, property_set: classes.PropertySet,
                           attributes: list[classes.Attribute]):
    xml_pset = etree.SubElement(xml_parent, "ruleItem")
    xml_pset.set("ID", property_set.uuid)
    xml_pset.set("name", property_set.name)
    xml_pset.set("type", "group")
    for attribute in attributes:
        _handle_rule_item_attribute(xml_pset, attribute)


def _handle_rule_items_by_pset_dict(pset_dict: dict[classes.PropertySet, list[classes.Attribute]],
                                    attribute_rule_tree: etree.Element):
    for pset, attribute_list in pset_dict.items():
        _handle_rule_item_pset(attribute_rule_tree, pset, attribute_list)


def _handle_object_rules(author: str, required_data_dict: dict,
                         object_structure: dict[classes.Object, set[classes.Object]],
                         base_xml_container: Element,
                         template: jinja2.Template, export_type: str) -> dict[Element, classes.Object]:
    xml_object_dict: dict[Element, classes.Object] = dict()

    root_nodes = {obj for obj, value in object_structure.items() if not value}

    for root_node in sorted(root_nodes, key=lambda x: x.name):
        _handle_tree_structure(author, required_data_dict, base_xml_container, object_structure, root_node, template,
                               xml_object_dict,
                               export_type)
    return xml_object_dict


def _handle_data_section(xml_qa_export: Element, xml_checkrun_first: Element,
                         xml_checkrun_obj: dict[Element, classes.Object | None],
                         xml_checkrun_last: Element) -> None:
    def get_name() -> str:
        """Transorms native IFC Attributes like IfcType into desite Attributes"""

        pset_name = obj.ident_attrib.property_set.name
        if pset_name == "IFC":
            return obj.ident_attrib.name

        else:
            return f"{pset_name}:{obj.ident_attrib.name}"

    xml_data_section = etree.SubElement(xml_qa_export, "dataSection")

    check_run_data = etree.SubElement(xml_data_section, "checkRunData")
    check_run_data.set("refID", str(xml_checkrun_first.attrib.get("ID")))
    etree.SubElement(check_run_data, "checkSet")

    for xml_checkrun, obj in xml_checkrun_obj.items():
        check_run_data = etree.SubElement(xml_data_section, "checkRunData")
        check_run_data.set("refID", str(xml_checkrun.attrib.get("ID")))
        if obj is None:
            etree.SubElement(check_run_data, "checkSet")
            continue
        filter_list = etree.SubElement(check_run_data, "filterList")
        xml_filter = etree.SubElement(filter_list, "filter")

        xml_filter.set("name", get_name())
        xml_filter.set("dt", "xs:string")
        pattern = f'"{obj.ident_value}"'
        xml_filter.set("pattern", pattern)

    check_run_data = etree.SubElement(xml_data_section, "checkRunData")
    check_run_data.set("refID", str(xml_checkrun_last.attrib.get("ID")))
    filter_list = etree.SubElement(check_run_data, "filterList")
    xml_filter = etree.SubElement(filter_list, "filter")
    xml_filter.set("name", "Check_State")
    xml_filter.set("dt", "xs:string")
    xml_filter.set("pattern", '"Ungeprüft"')


def _handle_property_section(xml_qa_export: Element) -> None:
    repository = etree.SubElement(xml_qa_export, "repository")
    property_type_section = etree.SubElement(repository, "propertyTypeSection")
    ptype = etree.SubElement(property_type_section, "ptype")

    ptype.set("key", "1")
    ptype.set("name", "Bestandsdaten:Objekttyp")
    ptype.set("datatype", "xs:string")
    ptype.set("unit", "")
    ptype.set("inh", "true")
    etree.SubElement(repository, "propertySection")


def _handle_untested(xml_attribute_rule_list: etree.Element, main_pset: str, main_attribute: str):
    template = _handle_template(Template.UNTESTED)
    rule_script = etree.SubElement(xml_attribute_rule_list, "ruleScript")
    name = "untested"
    rule_script.set("name", name)
    rule_script.set("active", "true")
    rule_script.set("resume", "false")
    code = etree.SubElement(rule_script, "code")
    code.text = str(template.render(pset_name=main_pset, attribute_name=main_attribute))


def _handle_attribute_rule(attribute: classes.Attribute) -> str:
    data_type = xml.transform_data_format(attribute.data_type)
    pset_name = attribute.property_set.name

    if attribute.value_type == value_constants.RANGE:
        row = ["R", "", f"{pset_name}:{attribute.name}", data_type, "*", f"Pruefung"]
        return ";".join(row)

    if not attribute.value:
        row = ["R", "", f"{pset_name}:{attribute.name}", data_type, "*", f"Pruefung"]
        return ";".join(row)

    ident_text = f"{pset_name}:{attribute.name}"
    allowed_values = " ".join([f"'{str(v)}'" for v in attribute.value])
    row = ["R", "", ident_text, data_type, allowed_values, f"Pruefung"]

    return ";".join(row)


def _fast_object_check(main_pset: str, main_attrib: str, author: str, required_data_dict: dict,
                       base_xml_container: Element,
                       template: jinja2.Template) -> dict[Element, None]:
    xml_checkrun = _handle_checkrun(base_xml_container, "Main Check", author)
    xml_rule = _handle_rule(xml_checkrun, "Attributes")
    xml_attribute_rule_list = _handle_attribute_rule_list(xml_rule)
    xml_rule_script = _handle_rule_script(xml_attribute_rule_list, name="Main Check")
    xml_code = _handle_code(xml_rule_script)
    cdata_code = template.render(object_dict=required_data_dict, main_pset=main_pset, main_attrib=main_attrib,
                                 constants=value_constants,
                                 ignore_pset=json_constants.IGNORE_PSET, xs_dict=xml.DATA_TYPE_MAPPING_DICT)
    xml_code.text = cdata_code
    _handle_rule(xml_checkrun, "UniquePattern")
    return {xml_checkrun: None}


def build_full_data_dict(proj: classes.Project) -> dict[
    classes.Object, dict[classes.PropertySet, list[classes.Attribute]]]:
    d = dict()
    for obj in proj.objects:
        d[obj] = dict()
        for pset in obj.property_sets:
            d[obj][pset] = list()
            for attribute in pset.attributes:
                d[obj][pset].append(attribute)
    return d


def export(project: classes.Project,
           required_data_dict: dict[classes.Object, dict[classes.PropertySet, list[classes.Attribute]]],
           path: str, main_pset: str, main_attribute: str,
           object_structure: dict[classes.Object, set[classes.Object]] = None,
           export_type: str = "JS") -> None:
    if not object_structure:
        object_structure = {o: o.children for o in project.objects}

    template = _handle_template(Template.TEMPLATE)
    xml_container, xml_qa_export = _init_xml(project.author, project.name, project.version)
    xml_checkrun_first, xml_attribute_rule_list = _define_xml_elements(project.author, xml_container, "initial_tests")
    _handle_js_rules(xml_attribute_rule_list, "start")
    xml_checkrun_obj = _handle_object_rules(project.author, required_data_dict, object_structure, xml_container,
                                            template,
                                            export_type)
    xml_checkrun_last, xml_attribute_rule_list = _define_xml_elements(project.author, xml_container, "untested")
    _handle_untested(xml_attribute_rule_list, main_pset, main_attribute)
    _handle_data_section(xml_qa_export, xml_checkrun_first, xml_checkrun_obj, xml_checkrun_last)
    _handle_property_section(xml_qa_export)

    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")


def csv_export(required_data_dict: dict[classes.Object, dict[classes.PropertySet, list[classes.Attribute]]], path):
    from ... import __version__
    lines = list()
    lines.append(";".join(["#", f"Created by SOMcreator v{__version__}"]))
    lines.append("H;Property Name;;Data Type;Rule;Comment")

    for obj, pset_dict in required_data_dict.items():
        if obj.ident_attrib is None:
            continue
        ident_attrib = f"{obj.ident_attrib.property_set.name}:{obj.ident_attrib.name}"
        data_type = xml.transform_data_format(obj.ident_attrib.data_type)
        lines.append(";".join(
            ["C", ident_attrib, "", data_type, f"'{obj.ident_value}'", f"Nach Objekt {obj.name} filtern"]))

        for pset, attribute_list in pset_dict.items():
            for attribute in attribute_list:
                if attribute.value_type != value_constants.RANGE:
                    lines.append(_handle_attribute_rule(attribute))
    with open(path, "w") as file:
        for line in lines:
            file.write(line + "\n")


def fast_check(project: classes.Project, main_pset: str, main_attrib: str,
               required_data_dict: dict[classes.Object, dict[classes.PropertySet, list[classes.Attribute]]],
               path: str) -> None:
    """
    creates a single rule for all elements -> no containers for checkruns
    :param project:
    :param main_pset: name of main propertyset which is used as matchkey
    :param main_attrib: name of main Attribute wihich is used as matchkey
    :param required_data_dict: Dictionary of all required Objects, Propertysets and Attributes
    :param path: Export Path
    :return:
    """
    template = _handle_template(Template.FAST_TEMPLATE)
    xml_container, xml_qa_export = _init_xml(project.author, project.name, project.version)
    xml_checkrun_first, xml_attribute_rule_list = _define_xml_elements(project.author, xml_container, "initial_tests")
    _handle_js_rules(xml_attribute_rule_list, "start")
    xml_checkrun_obj = _fast_object_check(main_pset, main_attrib, project.author, required_data_dict, xml_container,
                                          template)
    xml_checkrun_last, xml_attribute_rule_list = _define_xml_elements(project.author, xml_container, "untested")
    _handle_untested(xml_attribute_rule_list, main_pset, main_attrib)
    _handle_data_section(xml_qa_export, xml_checkrun_first, xml_checkrun_obj, xml_checkrun_last)
    _handle_property_section(xml_qa_export)

    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")
