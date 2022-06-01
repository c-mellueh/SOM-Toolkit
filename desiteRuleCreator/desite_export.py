from PySide6.QtWidgets import QFileDialog
from . import constants,classes
import os
import codecs
import xml.etree.ElementTree as ET
from lxml import etree
import copy
from jinja2 import Environment, FileSystemLoader
import uuid
import datetime

#TODO add xs:bool

def add_js_rule(parent: etree._Element, file):
    name = os.path.basename(file.name)
    if not name.endswith(".js"):
        return
    else:
        ruleScript = etree.SubElement(parent, "ruleScript")

        name = name.split("_")[1:]
        name = "_".join(name)
        ruleScript.set("name", name[:-3])
        ruleScript.set("active", "true")
        ruleScript.set("resume", "false")

        code = etree.SubElement(ruleScript, "code")
        file = file.read()

        code.text = file
        code.text = etree.CDATA(code.text)

    return file


def get_path(mainWindow):
    if mainWindow.export_path is not None:
        path = \
            QFileDialog.getSaveFileName(mainWindow, "Save qaXML", mainWindow.export_path, "xml Files (*.qa.xml)")[0]
    else:
        path = QFileDialog.getSaveFileName(mainWindow, "Save qaXML", "", "xml Files (*.qa.xml)")[0]

    return path

def save_rules(mainWindow):
    path = get_path(mainWindow)

    if path:
        export(mainWindow,path)
        pass

output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")



def handle_qa_export(mainWindow):
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    qaExport = etree.Element('{http://www.w3.org/2001/XMLSchema-instance}qaExport')
    qaExport.set("user", str(mainWindow.project.author))
    qaExport.set("date", str(output_date))
    qaExport.set("version", "2.8.1")
    return qaExport

def handle_element_section(xml_qa_export):
    xml_elementSection = etree.SubElement(xml_qa_export, "elementSection")
    return xml_elementSection

def handle_container(xml_element_section):
    container = etree.SubElement(xml_element_section, "container")
    container.set("ID", str(uuid.uuid4()))
    container.set("name", "Konsistenzprüfung")
    return container

def handle_checkrun(xml_container,name,author = "CMellueh") ->etree._Element:
    checkrun:etree._Element = etree.SubElement(xml_container, "checkrun")
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

def init_xml(mainWindow):
    xml_qa_export = handle_qa_export(mainWindow)
    xml_elementSection = handle_element_section(xml_qa_export)
    xml_container = handle_container(xml_elementSection)
    return xml_container,xml_qa_export

def handle_rule(xml_checkrun,type):
    rule = etree.SubElement((xml_checkrun), "rule")
    rule.set("type", type)
    if type == "UniquePattern":
        etree.SubElement(rule, "patternList")
        code = etree.SubElement(xml_checkrun, "code")
        code.text = ""

    return rule


def handle_attribute_rule_list(xml_rule):
    attributeRuleList = etree.SubElement(xml_rule, "attributeRuleList")
    return attributeRuleList


def handle_template():
    path = f"{os.path.dirname(os.path.abspath(__file__))}/Template/"
    file_loader = FileSystemLoader(path)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    # env.rstrip_blocks=True
    template = env.get_template("template.txt")
    #ungeprueft_template = env.get_template('ungeprueft.txt')

    return template

def define_xml_elements(mainWindow,xml_container,name):
    xml_checkrun = handle_checkrun(xml_container, name=name, author=mainWindow.project.author)
    xml_rule = handle_rule(xml_checkrun,"Attributes")
    xml_attributeRuleList = handle_attribute_rule_list(xml_rule)
    handle_rule(xml_checkrun, "UniquePattern")

    return xml_checkrun,xml_attributeRuleList



def handle_js_rules(xml_attributeRuleList,starts_with):
    folder =f"{os.path.dirname(os.path.abspath(__file__))}/Template/{constants.FILEPATH_JS}/"

    for fn in os.listdir(folder):
        if fn.startswith(starts_with):
            file = codecs.open(f"{folder}/{fn}", encoding="utf-8")
            add_js_rule(xml_attributeRuleList, file)


def handle_rule_script(xml_attribute_rule_list,name):
    ruleScript = etree.SubElement(xml_attribute_rule_list, "ruleScript")
    ruleScript.set("name", name)
    ruleScript.set("active", "true")
    ruleScript.set("resume", "true")
    return ruleScript
def handle_code(xml_rule_script):
    code = etree.SubElement(xml_rule_script, "code")
    return code

def handle_object_rules(xml_container,mainWindow,template):
    xml_object_list = dict()

    obj_sorted = list(classes.Object.iter)
    obj_sorted.sort(key = lambda x: x.name)
    for object in obj_sorted:
        if not object.is_concept:
            object:classes.Object = object
            xml_checkrun = handle_checkrun(xml_container,object.name,mainWindow.project.author)
            xml_object_list[xml_checkrun] = object
            xml_rule = handle_rule(xml_checkrun,"Attributes")
            xml_attribute_rule_list = handle_attribute_rule_list(xml_rule)
            xml_rule_script = handle_rule_script(xml_attribute_rule_list,name = object.name)
            xml_code = handle_code(xml_rule_script)

            attributes = object.attributes

            for inh_attributes in object.inherited_attributes.values():
                attributes+=inh_attributes
            pset_dict = classes.attributes_to_psetdict(attributes)  # pset_dict[PropertySet] = Attribute

            psets = pset_dict.keys()
            ident_name = object.identifier.name
            ident_property_set = object.identifier.propertySet.name
            if ident_property_set == constants.IGNORE_PSET:
                ident_property_set = ""
            else:
                ident_property_set= f"{ident_property_set}:"
            cdata_code = template.render(psets=psets, object=object, ident=ident_name, ident_pset=ident_property_set,constants = constants)
            xml_code.text = cdata_code
            handle_rule(xml_checkrun,"UniquePattern")
    return xml_object_list
def old_file_conversion(projekt):
    projekt = copy.deepcopy(projekt)

    objekte = projekt.get_all_objekte()

    fblist = []
    for obj in objekte:
        if obj.fachdisziplin not in fblist:
            fblist.append(obj.fachdisziplin)

    print(";".join(fblist))

    for objekt in objekte:
        property_sets = objekt.get_all_property_sets()
        for property_set in property_sets:
            properties = property_set.get_all_properties()
            for prop in properties:
                if prop._art == "Bereich":
                    value = []
                    for i, el in enumerate(prop.wert):
                        if ":" in el:
                            value.append(el.split(":"))
                        else:
                            value.append([el])
                    prop.wert = value

    for obj in objekte:
        if obj.name.startswith("_"):
            obj.name = obj.name[1:]

def handle_data_section(xml_qa_export,xml_checkrun_first,xml_checkrun_obj,xml_checkrun_last):
    def get_name(obj:classes.Object):
        pset_name = obj.identifier.propertySet.name
        if pset_name == "IFC":
            return obj.identifier.name

        else:
            return f"{pset_name}:{obj.identifier.name}"

    xml_dataSection = etree.SubElement(xml_qa_export, "dataSection")

    checkRunData = etree.SubElement(xml_dataSection, "checkRunData")
    checkRunData.set("refID", str(xml_checkrun_first.attrib.get("ID")))
    checkSet = etree.SubElement(checkRunData, "checkSet")

    for xml_checkrun,obj in xml_checkrun_obj.items():
        checkRunData = etree.SubElement(xml_dataSection, "checkRunData")
        checkRunData.set("refID", str(xml_checkrun.attrib.get("ID")))
        filterList = etree.SubElement(checkRunData, "filterList")
        filter = etree.SubElement(filterList, "filter")

        filter.set("name", get_name(obj))
        filter.set("dt", "xs:string")
        pattern = f'"{obj.identifier.value[0]}"'            #ToDO: ändern
        filter.set("pattern", pattern)

    checkRunData = etree.SubElement(xml_dataSection, "checkRunData")
    checkRunData.set("refID", str(xml_checkrun_last.attrib.get("ID")))
    filterList = etree.SubElement(checkRunData, "filterList")
    filter = etree.SubElement(filterList, "filter")
    filter.set("name", "Check_State")
    filter.set("dt", "xs:string")
    filter.set("pattern", '"Ungeprüft"')

def handle_propertySection(xml_qa_export):
    repository = etree.SubElement(xml_qa_export, "repository")
    propertyTypeSection = etree.SubElement(repository, "propertyTypeSection")
    ptype = etree.SubElement(propertyTypeSection, "ptype")

    ptype.set("key", "1")
    ptype.set("name", "Bestandsdaten:Objekttyp")
    ptype.set("datatype", "xs:string")
    ptype.set("unit", "")
    ptype.set("inh", "true")

    propertySection = etree.SubElement(repository, "propertySection")

def export(mainWindow, path):

    template = handle_template()
    xml_container,xml_qa_export = init_xml(mainWindow)
    xml_checkrun_first,xml_attribute_rule_list = define_xml_elements(mainWindow,xml_container,"initial_tests")
    handle_js_rules(xml_attribute_rule_list,"start")
    xml_checkrun_obj = handle_object_rules(xml_container,mainWindow,template)
    xml_checkrun_last,xml_attribute_rule_list = define_xml_elements(mainWindow,xml_container,"untested")
    handle_js_rules(xml_attribute_rule_list,"end")
    handle_data_section(xml_qa_export,xml_checkrun_first,xml_checkrun_obj,xml_checkrun_last)
    handle_propertySection(xml_qa_export)


    tree = etree.ElementTree(xml_qa_export)
    with open(path, "wb") as f:
        tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")

