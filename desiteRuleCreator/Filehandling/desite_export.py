import codecs
import datetime
import os
import uuid
import xml.etree.ElementTree as ET

from PySide6.QtWidgets import QFileDialog
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from desiteRuleCreator import Template
from desiteRuleCreator.data import classes, constants

output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


##TODO add xs:bool

def add_js_rule(parent, file):
    name = os.path.basename(file.name)
    if not name.endswith(".js"):
        return
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


def get_path(main_window):
    if main_window.export_path is not None:
        path = \
            QFileDialog.getSaveFileName(main_window, "Save qaXML", main_window.export_path, "xml Files (*.qa.xml)")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, "Save qaXML", "", "xml Files (*.qa.xml)")[0]

    return path


def save_rules(main_window):
    path = get_path(main_window)

    if path:
        export(main_window, path)
        pass


def handle_qa_export(main_window):
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    qa_export = etree.Element('{http://www.w3.org/2001/XMLSchema-instance}qaExport')
    qa_export.set("user", str(main_window.project.author))
    qa_export.set("date", str(output_date))
    qa_export.set("version", "2.8.1")
    return qa_export


def handle_element_section(xml_qa_export):
    xml_element_section = etree.SubElement(xml_qa_export, "elementSection")
    return xml_element_section


def handle_container(xml_element_section,project):
    container = etree.SubElement(xml_element_section, "container")
    container.set("ID", str(uuid.uuid4()))
    container.set("name",f"{project.name} : {project.version}")
    return container


def handle_checkrun(xml_container, name, author="CMellueh"):
    checkrun = etree.SubElement(xml_container, "checkrun")
    _uuid = str(uuid.uuid4())
    checkrun.set("ID", _uuid)
    checkrun.set("name", name)
    checkrun.set("active", "true")
    checkrun.set("user", str(author))
    checkrun.set("date", str(output_date))
    checkrun.set("state", "0")
    checkrun.set("objectsOnly", "1")
    checkrun.set("partsOfComposites", "0")
    checkrun.set("createFailed", "true")
    checkrun.set("createWarnings", "true")
    checkrun.set("createIgnored", "false")
    checkrun.set("createPassed", "true")
    checkrun.set("createUndefined", "false")
    return checkrun


def init_xml(main_window):
    xml_qa_export = handle_qa_export(main_window)
    xml_element_section = handle_element_section(xml_qa_export)
    xml_container = handle_container(xml_element_section,main_window.project)
    return xml_container, xml_qa_export


def handle_rule(xml_checkrun, rule_type):
    rule = etree.SubElement(xml_checkrun, "rule")
    rule.set("type", rule_type)
    if rule_type == "UniquePattern":
        etree.SubElement(rule, "patternList")
        code = etree.SubElement(xml_checkrun, "code")
        code.text = ""

    return rule


def handle_attribute_rule_list(xml_rule):
    attribute_rule_list = etree.SubElement(xml_rule, "attributeRuleList")
    return attribute_rule_list


def handle_template():
    path = Template.HOME_DIR
    file_loader = FileSystemLoader(path)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    # env.rstrip_blocks=True
    template = env.get_template("template.txt")
    # ungeprueft_template = env.get_template('ungeprueft.txt')

    return template


def define_xml_elements(main_window, xml_container, name):
    xml_checkrun = handle_checkrun(xml_container, name=name, author=main_window.project.author)
    xml_rule = handle_rule(xml_checkrun, "Attributes")
    xml_attribute_rule_list = handle_attribute_rule_list(xml_rule)
    handle_rule(xml_checkrun, "UniquePattern")

    return xml_checkrun, xml_attribute_rule_list


def handle_js_rules(xml_attribute_rule_list, starts_with):
    folder = f"{Template.HOME_DIR}/{constants.FILEPATH_JS}/"

    for fn in os.listdir(folder):
        if fn.startswith(starts_with):
            file = codecs.open(f"{folder}/{fn}", encoding="utf-8")
            add_js_rule(xml_attribute_rule_list, file)


def handle_rule_script(xml_attribute_rule_list, name):
    rule_script = etree.SubElement(xml_attribute_rule_list, "ruleScript")
    rule_script.set("name", name)
    rule_script.set("active", "true")
    rule_script.set("resume", "true")
    return rule_script


def handle_code(xml_rule_script):
    code = etree.SubElement(xml_rule_script, "code")
    return code


def handle_object_rules(xml_container, main_window, template):
    xml_object_list = dict()

    obj_sorted = list(classes.Object.iter)
    obj_sorted.sort(key=lambda x: x.name)
    for obj in obj_sorted:
        if not obj.is_concept:
            obj: classes.Object = obj
            xml_checkrun = handle_checkrun(xml_container, obj.name, main_window.project.author)
            xml_object_list[xml_checkrun] = obj
            xml_rule = handle_rule(xml_checkrun, "Attributes")
            xml_attribute_rule_list = handle_attribute_rule_list(xml_rule)
            xml_rule_script = handle_rule_script(xml_attribute_rule_list, name=obj.name)
            xml_code = handle_code(xml_rule_script)

            property_sets = obj.property_sets

            ident_name = obj.ident_attrib.name
            ident_property_set = obj.ident_attrib.property_set.name
            if ident_property_set == constants.IGNORE_PSET:
                ident_property_set = ""
            else:
                ident_property_set = f"{ident_property_set}:"

            cdata_code = template.render(psets=property_sets, object=obj, ident=ident_name,
                                         ident_pset=ident_property_set, constants=constants)
            xml_code.text = cdata_code
            handle_rule(xml_checkrun, "UniquePattern")

            for script in obj.scripts:
                xml_rule_script = handle_rule_script(xml_attribute_rule_list, name=script.name)
                xml_code = handle_code(xml_rule_script)
                xml_code.text = script.code

    return xml_object_list


def handle_data_section(xml_qa_export, xml_checkrun_first, xml_checkrun_obj, xml_checkrun_last):
    def get_name():
        pset_name = obj.ident_attrib.property_set.name
        if pset_name == "IFC":
            return obj.ident_attrib.name

        else:
            return f"{pset_name}:{obj.ident_attrib.name}"

    xml_data_section = etree.SubElement(xml_qa_export, "dataSection")

    check_run_data = etree.SubElement(xml_data_section, "checkRunData")
    check_run_data.set("refID", str(xml_checkrun_first.attrib.get("ID")))
    check_set = etree.SubElement(check_run_data, "checkSet")

    for xml_checkrun, obj in xml_checkrun_obj.items():
        check_run_data = etree.SubElement(xml_data_section, "checkRunData")
        check_run_data.set("refID", str(xml_checkrun.attrib.get("ID")))
        filter_list = etree.SubElement(check_run_data, "filterList")
        xml_filter = etree.SubElement(filter_list, "filter")

        xml_filter.set("name", get_name())
        xml_filter.set("dt", "xs:string")
        pattern = f'"{obj.ident_attrib.value[0]}"'  # ToDO: ändern
        xml_filter.set("pattern", pattern)

    check_run_data = etree.SubElement(xml_data_section, "checkRunData")
    check_run_data.set("refID", str(xml_checkrun_last.attrib.get("ID")))
    filter_list = etree.SubElement(check_run_data, "filterList")
    xml_filter = etree.SubElement(filter_list, "filter")
    xml_filter.set("name", "Check_State")
    xml_filter.set("dt", "xs:string")
    xml_filter.set("pattern", '"Ungeprüft"')


def handle_property_section(xml_qa_export):
    repository = etree.SubElement(xml_qa_export, "repository")
    property_type_section = etree.SubElement(repository, "propertyTypeSection")
    ptype = etree.SubElement(property_type_section, "ptype")

    ptype.set("key", "1")
    ptype.set("name", "Bestandsdaten:Objekttyp")
    ptype.set("datatype", "xs:string")
    ptype.set("unit", "")
    ptype.set("inh", "true")

    property_section = etree.SubElement(repository, "propertySection")


def export(main_window, path):
    template = handle_template()
    xml_container, xml_qa_export = init_xml(main_window)
    xml_checkrun_first, xml_attribute_rule_list = define_xml_elements(main_window, xml_container, "initial_tests")
    handle_js_rules(xml_attribute_rule_list, "start")
    xml_checkrun_obj = handle_object_rules(xml_container, main_window, template)
    xml_checkrun_last, xml_attribute_rule_list = define_xml_elements(main_window, xml_container, "untested")
    handle_js_rules(xml_attribute_rule_list, "end")
    handle_data_section(xml_qa_export, xml_checkrun_first, xml_checkrun_obj, xml_checkrun_last)
    handle_property_section(xml_qa_export)

    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")
