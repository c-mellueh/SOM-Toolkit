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
from SOMcreator.util import xml
from SOMcreator.util.misc import merge_list
from SOMcreator import constants, templates
from SOMcreator.constants import value_constants
import SOMcreator

JS_EXPORT = "JS"
TABLE_EXPORT = "TABLE"


class ClassStructureDict(TypedDict):
    children: set[SOMcreator.SOMClass]


def _handle_template(path: str | os.PathLike) -> jinja2.Template:
    file_loader = jinja2.FileSystemLoader(templates.HOME_DIR)
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


def _handle_checkrun(
    xml_container: Element, name: str, author: str = "DesiteRuleCreator"
) -> Element:
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


def _handle_property_rule_list(xml_rule: Element) -> Element:
    property_rule_list = etree.SubElement(xml_rule, "attributeRuleList")
    return property_rule_list


def _define_xml_elements(
    author: str, xml_container: Element, name: str
) -> tuple[Element, Element]:
    xml_checkrun = _handle_checkrun(xml_container, name=name, author=author)
    xml_rule = _handle_rule(xml_checkrun, "Attributes")
    xml_property_rule_list = _handle_property_rule_list(xml_rule)
    _handle_rule(xml_checkrun, "UniquePattern")

    return xml_checkrun, xml_property_rule_list


def _handle_js_rules(xml_property_rule_list: Element, starts_with: str) -> None:
    folder = os.path.join(templates.HOME_DIR, constants.FILEPATH_JS)

    for fn in os.listdir(folder):
        if str(fn).startswith(starts_with):
            file = codecs.open(f"{folder}/{fn}", encoding="utf-8")
            _add_js_rule(xml_property_rule_list, file)


def _handle_rule_script(xml_property_rule_list: Element, name: str) -> Element:
    rule_script = etree.SubElement(xml_property_rule_list, "ruleScript")
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


def _handle_tree_structure(
    author: str,
    required_data_dict: dict,
    parent_xml_container,
    class_structure: dict[SOMcreator.SOMClass, SOMcreator.SOMClass],
    parent_class: SOMcreator.SOMClass,
    template,
    xml_class_dict,
    export_type: str,
) -> None:
    def check_basics(som_class: SOMcreator.SOMClass):
        if som_class.identifier_property is None:
            return som_class, None, True

        pset_dict = required_data_dict.get(som_class)
        if pset_dict is None:
            return som_class, None, True
        return som_class, pset_dict, False

    def create_container(xml_container):
        new_xml_container = _handle_container(xml_container, parent_class.name)
        if export_type == JS_EXPORT:
            create_js_object(new_xml_container)
        elif export_type == TABLE_EXPORT:
            create_table_object(new_xml_container)

        for child_class in sorted(children, key=lambda x: x.name):
            _handle_tree_structure(
                author,
                required_data_dict,
                new_xml_container,
                class_structure,
                child_class,
                template,
                xml_class_dict,
                export_type,
            )

    def create_js_object(xml_container):
        som_class, pset_dict, abort = check_basics(parent_class)
        if abort:
            return
        xml_checkrun = _handle_checkrun(xml_container, som_class.name, author)
        xml_rule = _handle_rule(xml_checkrun, "Attributes")
        xml_attribute_rule_list = _handle_property_rule_list(xml_rule)
        xml_rule_script = _handle_rule_script(xml_attribute_rule_list, name=som_class.name)
        xml_code = _handle_code(xml_rule_script)
        cdata_code = template.render(
            pset_dict=pset_dict,
            constants=value_constants,
            ignore_pset="",
            xs_dict=xml.DATA_TYPE_MAPPING_DICT,
        )
        xml_code.text = cdata_code
        _handle_rule(xml_checkrun, "UniquePattern")

        xml_class_dict[xml_checkrun] = som_class

    def create_table_object(xml_container):
        som_class, pset_dict, abort = check_basics(parent_class)
        if abort:
            return
        xml_checkrun = _handle_checkrun(xml_container, som_class.name, author)
        xml_rule = _handle_rule(xml_checkrun, "Attributes")
        xml_attribute_rule_tree = _handle_attribute_rule_tree(xml_rule)
        xml_code = _handle_code(xml_container)

        _handle_rule_items_by_pset_dict(pset_dict, xml_attribute_rule_tree)
        xml_code.text = "<![CDATA[]]>"
        _handle_rule(xml_checkrun, "UniquePattern")

        xml_class_dict[xml_checkrun] = som_class

    children = {o for o, parent in class_structure.items() if parent == parent_class}

    if children and required_data_dict.get(parent_class):
        create_container(parent_xml_container)
    else:
        if export_type == JS_EXPORT:
            create_js_object(parent_xml_container)
        elif export_type == TABLE_EXPORT:
            create_table_object(parent_xml_container)


def _csv_value_in_list(attribute: SOMcreator.SOMProperty):
    return " ".join(f'"{str(val)}"' for val in attribute.allowed_values)


def _csv_check_range(attribute: SOMcreator.SOMProperty) -> str:
    sorted_range_list = sorted(
        [[min(v1, v2), max(v1, v2)] for [v1, v2] in attribute.allowed_values]
    )
    sorted_range_list = merge_list(sorted_range_list)

    pattern = "||".join(f">={v_min}&&<={v_max}" for v_min, v_max in sorted_range_list)
    return pattern


def _build_basics_rule_item(
    xml_parent: etree.Element, attribute: SOMcreator.SOMProperty
) -> etree.Element:
    xml_attrib = etree.SubElement(xml_parent, "ruleItem")
    xml_attrib.set("ID", attribute.uuid)
    data_type = xml.transform_data_format(attribute.data_type)
    xml_attrib.set(
        "name", f"{attribute.property_set.name}:{attribute.name}##{data_type}"
    )
    xml_attrib.set("type", "simple")
    return xml_attrib


def _handle_rule_item_attribute(
    xml_parent: etree.Element, attribute: SOMcreator.SOMProperty
):
    xml_attrib = _build_basics_rule_item(xml_parent, attribute)

    if not attribute.allowed_values:
        xml_attrib.set("pattern", "*")
        return
    pattern = "*"
    if attribute.data_type in (value_constants.INTEGER, value_constants.REAL):
        if attribute.value_type == value_constants.LIST:
            pattern = _csv_value_in_list(attribute)
        elif attribute.value_type == value_constants.RANGE:
            pattern = _csv_check_range(attribute)
        else:
            logging.error(
                f"No Function defined for {attribute.name} ({attribute.value_type} x {attribute.data_type}"
            )
            pattern = "*"

    elif attribute.data_type == value_constants.LABEL:
        if attribute.value_type == value_constants.FORMAT:
            pattern = " || ".join(attribute.allowed_values)
        elif attribute.value_type == value_constants.LIST:
            pattern = " ".join([f'"{v}"' for v in attribute.allowed_values])

    elif attribute.data_type == value_constants.BOOLEAN:
        pattern = "*"
    else:
        logging.error(
            f"No Function defined for {attribute.name} ({attribute.value_type} x {attribute.data_type}"
        )

    xml_attrib.set("pattern", pattern)


def _handle_rule_item_pset(
    xml_parent: etree.Element,
    property_set: SOMcreator.SOMPropertySet,
    attributes: list[SOMcreator.SOMProperty],
):
    xml_pset = etree.SubElement(xml_parent, "ruleItem")
    xml_pset.set("ID", property_set.uuid)
    xml_pset.set("name", property_set.name)
    xml_pset.set("type", "group")
    for attribute in attributes:
        _handle_rule_item_attribute(xml_pset, attribute)


def _handle_rule_items_by_pset_dict(
    pset_dict: dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]],
    attribute_rule_tree: etree.Element,
):
    for pset, attribute_list in pset_dict.items():
        _handle_rule_item_pset(attribute_rule_tree, pset, attribute_list)


def _handle_class_rules(
    author: str,
    required_data_dict: dict,
    class_structure: dict[SOMcreator.SOMClass, SOMcreator.SOMClass],
    base_xml_container: Element,
    template: jinja2.Template,
    export_type: str,
) -> dict[Element, SOMcreator.SOMClass]:
    xml_class_dict: dict[Element, SOMcreator.SOMClass] = dict()

    root_nodes = {som_class for som_class, parent in class_structure.items() if parent is None}

    for root_node in sorted(root_nodes, key=lambda x: x.name):
        _handle_tree_structure(
            author,
            required_data_dict,
            base_xml_container,
            class_structure,
            root_node,
            template,
            xml_class_dict,
            export_type,
        )
    return xml_class_dict


def _handle_data_section(
    xml_qa_export: Element,
    xml_checkrun_first: Element,
    xml_checkrun_class: dict[Element, SOMcreator.SOMClass | None],
    xml_checkrun_last: Element,
) -> None:
    def get_name() -> str:
        """Transorms native IFC Attributes like IfcType into desite Attributes"""

        pset_name = som_class.identifier_property.property_set.name
        if pset_name == "IFC":
            return som_class.identifier_property.name

        else:
            return f"{pset_name}:{som_class.identifier_property.name}"

    xml_data_section = etree.SubElement(xml_qa_export, "dataSection")

    check_run_data = etree.SubElement(xml_data_section, "checkRunData")
    check_run_data.set("refID", str(xml_checkrun_first.attrib.get("ID")))
    etree.SubElement(check_run_data, "checkSet")

    for xml_checkrun, som_class in xml_checkrun_class.items():
        check_run_data = etree.SubElement(xml_data_section, "checkRunData")
        check_run_data.set("refID", str(xml_checkrun.attrib.get("ID")))
        if som_class is None:
            etree.SubElement(check_run_data, "checkSet")
            continue
        filter_list = etree.SubElement(check_run_data, "filterList")
        xml_filter = etree.SubElement(filter_list, "filter")

        xml_filter.set("name", get_name())
        xml_filter.set("dt", "xs:string")
        pattern = f'"{som_class.ident_value}"'
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


def _handle_untested(
    xml_attribute_rule_list: etree.Element, main_pset: str, main_attribute: str
):
    template = _handle_template(templates.UNTESTED)
    rule_script = etree.SubElement(xml_attribute_rule_list, "ruleScript")
    name = "untested"
    rule_script.set("name", name)
    rule_script.set("active", "true")
    rule_script.set("resume", "false")
    code = etree.SubElement(rule_script, "code")
    code.text = str(template.render(pset_name=main_pset, attribute_name=main_attribute))


def _handle_attribute_rule(attribute: SOMcreator.SOMProperty) -> str:
    data_type = xml.transform_data_format(attribute.data_type)
    pset_name = attribute.property_set.name

    if attribute.value_type == value_constants.RANGE:
        row = ["R", "", f"{pset_name}:{attribute.name}", data_type, "*", f"Pruefung"]
        return ";".join(row)

    if not attribute.allowed_values:
        row = ["R", "", f"{pset_name}:{attribute.name}", data_type, "*", f"Pruefung"]
        return ";".join(row)

    ident_text = f"{pset_name}:{attribute.name}"
    allowed_values = " ".join([f"'{str(v)}'" for v in attribute.allowed_values])
    row = ["R", "", ident_text, data_type, allowed_values, f"Pruefung"]

    return ";".join(row)


def _fast_class_check(
    main_pset: str,
    main_attrib: str,
    author: str,
    required_data_dict: dict,
    base_xml_container: Element,
    template: jinja2.Template,
) -> dict[Element, None]:
    xml_checkrun = _handle_checkrun(base_xml_container, "Main Check", author)
    xml_rule = _handle_rule(xml_checkrun, "Attributes")
    xml_attribute_rule_list = _handle_property_rule_list(xml_rule)
    xml_rule_script = _handle_rule_script(xml_attribute_rule_list, name="Main Check")
    xml_code = _handle_code(xml_rule_script)
    cdata_code = template.render(
        object_dict=required_data_dict,
        main_pset=main_pset,
        main_attrib=main_attrib,
        constants=value_constants,
        ignore_pset="",
        xs_dict=xml.DATA_TYPE_MAPPING_DICT,
    )
    xml_code.text = cdata_code
    _handle_rule(xml_checkrun, "UniquePattern")
    return {xml_checkrun: None}


def build_full_data_dict(
    proj: SOMcreator.SOMProject,
) -> dict[
    SOMcreator.SOMClass, dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]]
]:
    d = dict()
    for som_class in proj.get_classes(filter=True):
        d[som_class] = dict()
        for pset in som_class.get_property_sets(filter=True):
            d[som_class][pset] = list()
            for attribute in pset.get_properties(filter=True):
                d[som_class][pset].append(attribute)
    return d


def export(
    project: SOMcreator.SOMProject,
    required_data_dict: dict[
        SOMcreator.SOMClass,
        dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]],
    ],
    path: str,
    main_pset: str,
    main_property: str,
    class_structure: dict[SOMcreator.SOMClass, SOMcreator.SOMClass] = None,
    export_type: str = "JS",
) -> None:
    if not class_structure:
        class_structure = {o: o.parent for o in project.get_classes(filter=True)}

    template = _handle_template(templates.TEMPLATE)
    xml_container, xml_qa_export = _init_xml(
        project.author, project.name, project.version
    )
    xml_checkrun_first, xml_attribute_rule_list = _define_xml_elements(
        project.author, xml_container, "initial_tests"
    )
    _handle_js_rules(xml_attribute_rule_list, "start")
    xml_checkrun_class = _handle_class_rules(
        project.author,
        required_data_dict,
        class_structure,
        xml_container,
        template,
        export_type,
    )
    xml_checkrun_last, xml_attribute_rule_list = _define_xml_elements(
        project.author, xml_container, "untested"
    )
    _handle_untested(xml_attribute_rule_list, main_pset, main_property)
    _handle_data_section(
        xml_qa_export, xml_checkrun_first, xml_checkrun_class, xml_checkrun_last
    )
    _handle_property_section(xml_qa_export)

    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(
            f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml"
        )


def csv_export(
    required_data_dict: dict[
        SOMcreator.SOMClass,
        dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]],
    ],
    path,
):
    from ... import __version__

    lines = list()
    lines.append(";".join(["#", f"Created by SOMcreator v{__version__}"]))
    lines.append("H;Property Name;;Data Type;Rule;Comment")

    for som_class, pset_dict in required_data_dict.items():
        if som_class.identifier_property is None:
            continue
        ident_attrib = f"{som_class.identifier_property.property_set.name}:{som_class.identifier_property.name}"
        data_type = xml.transform_data_format(som_class.identifier_property.data_type)
        lines.append(
            ";".join(
                [
                    "C",
                    ident_attrib,
                    "",
                    data_type,
                    f"'{som_class.ident_value}'",
                    f"Nach Klasse {som_class.name} filtern",
                ]
            )
        )

        for pset, attribute_list in pset_dict.items():
            for attribute in attribute_list:
                if attribute.value_type != value_constants.RANGE:
                    lines.append(_handle_attribute_rule(attribute))
    with open(path, "w") as file:
        for line in lines:
            file.write(line + "\n")


def fast_check(
    project: SOMcreator.SOMProject,
    main_pset: str,
    main_attrib: str,
    required_data_dict: dict[
        SOMcreator.SOMClass,
        dict[SOMcreator.SOMPropertySet, list[SOMcreator.SOMProperty]],
    ],
    path: str,
) -> None:
    """
    creates a single rule for all elements -> no containers for checkruns
    :param project:
    :param main_pset: name of main propertyset which is used as matchkey
    :param main_attrib: name of main Attribute wihich is used as matchkey
    :param required_data_dict: Dictionary of all required Classes, Propertysets and Attributes
    :param path: Export Path
    :return:
    """
    template = _handle_template(templates.FAST_TEMPLATE)
    xml_container, xml_qa_export = _init_xml(
        project.author, project.name, project.version
    )
    xml_checkrun_first, xml_attribute_rule_list = _define_xml_elements(
        project.author, xml_container, "initial_tests"
    )
    _handle_js_rules(xml_attribute_rule_list, "start")
    xml_checkrun_class = _fast_class_check(
        main_pset,
        main_attrib,
        project.author,
        required_data_dict,
        xml_container,
        template,
    )
    xml_checkrun_last, xml_attribute_rule_list = _define_xml_elements(
        project.author, xml_container, "untested"
    )
    _handle_untested(xml_attribute_rule_list, main_pset, main_attrib)
    _handle_data_section(
        xml_qa_export, xml_checkrun_first, xml_checkrun_class, xml_checkrun_last
    )
    _handle_property_section(xml_qa_export)

    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(
            f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml"
        )
