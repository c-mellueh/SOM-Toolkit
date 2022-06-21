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
from desiteRuleCreator.QtDesigns import ui_mainwindow
output_date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
output_date = datetime.datetime.now().strftime("%Y-%m-%d")


def get_path(main_window,file_format:str):
    if main_window.export_path is not None:
        path = \
            QFileDialog.getSaveFileName(main_window, f"Save {file_format}", main_window.export_path, f"xml Files (*.{file_format})")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, f"Save {file_format}", "", f"xml Files (*.{file_format})")[0]

    return path

def handle_header(main_window, export_format:str):
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    xml_header = etree.Element(f'{{http://www.w3.org/2001/XMLSchema-instance}}{export_format}')
    xml_header.set("user", str(main_window.project.author))
    xml_header.set("date", str(output_date_time))
    xml_header.set("version", "3.0.1")       #TODO: Desite version hinzufügen
    return xml_header

##TODO add xs:bool

def export_modelcheck(main_window):

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
        checkrun.set("date", str(output_date_time))
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
        xml_qa_export = handle_header(main_window, "qaExport")
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

        obj_sorted = list(classes.Object)
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

        for xml_checkrun, obj in xml_checkrun_obj._registry():
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

    path = get_path(main_window,"qa.xml")

    if path:
        export(main_window, path)
        pass

def export_bs(main_window):
    def handle_boq_info(xml_parent):
        xml_box_info = etree.SubElement(xml_parent, "BoQInfo")
        name = etree.SubElement(xml_box_info,"name")
        shortText = etree.SubElement(xml_box_info,"shortText")
        date = etree.SubElement(xml_box_info,"date")
        outlCompl = etree.SubElement(xml_box_info,"outlCompl")
        fillchar = etree.SubElement(xml_box_info,"fillChar")

        name.text = "DRC Export"
        shortText.text = "This BoQ was automatically created by DRC"
        date.text = output_date
        outlCompl.text = "AllTxt"
        fillchar.text = "0"

        return xml_box_info

    def handle_attr(xml_parent,obj):
        xml_attr = etree.SubElement(xml_parent, "attr")
        xml_unit = etree.SubElement(xml_attr, "unit")
        xml_up = etree.SubElement(xml_attr, "up")
        xml_up.text = str(0)

    def handle_section(item:classes.CustomTreeItem,xml_item):


        id_dict = dict()
        xml_child = etree.SubElement(xml_item, "section")
        id = str(uuid.uuid4())

        id_dict[item.object] = id
        xml_child.set("ID",id)
        xml_child.set("name", item.object.name)
        xml_child.set("pre","")
        xml_child.set("type", "typeBsGroup")
        xml_child.set("takt","")

        for k in range(item.childCount()):
            child = item.child(k)
            child_id_dict = handle_section(child,xml_child)
            id_dict = {**child_id_dict,**id_dict}
        return id_dict

    def handle_elementsection(main_window,xml_parent):
        ui: ui_mainwindow.Ui_MainWindow = main_window.ui
        xml_elementsection = etree.SubElement(xml_parent, "elementSection")
        root = ui.tree.invisibleRootItem()
        xml_root = etree.SubElement(xml_elementsection,"section")
        xml_root.set("ID",str(uuid.uuid4()))
        xml_root.set("name","BS Autogenerated")
        xml_root.set("pre","")
        xml_root.set("type","typeBsContainer")
        xml_root.set("takt","")

        id_dict = dict()
        for k in range(root.childCount()):
            child = root.child(k)
            child_id_dict = handle_section(child,xml_root)
            id_dict = {**child_id_dict, **id_dict}

        return xml_elementsection,id_dict

    def handle_repository(main_window,xml_parent,id_dict):
        def handle_property_type_section():
            xml_property_type_section = etree.SubElement(xml_repo, "propertyTypeSection")

            attribute_dict = dict()

            i=1
            for attribute in classes.Attribute:

                attribute_text = f"{attribute.property_set.name}:{attribute.name}"
                if attribute_text not in attribute_dict:
                    xml_ptype = etree.SubElement(xml_property_type_section, "ptype")
                    xml_ptype.set("key", str(i))
                    xml_ptype.set("name", attribute_text)
                    xml_ptype.set("datatype",attribute.data_type)
                    xml_ptype.set("unit", "")
                    xml_ptype.set("inh", "false")
                    attribute_dict[attribute_text] = i
                    i+=1

            return attribute_dict

        def handle_property_section():
            xml_property_section = etree.SubElement(xml_repo, "propertySection")

            obj:classes.Object
            for i,obj in enumerate(id_dict):

                for property_set in obj.property_sets:
                    for attribute in property_set.attributes:
                        attribute_text = f"{attribute.property_set.name}:{attribute.name}"
                        ref_type = attribute_dict[attribute_text]
                        ref_id = id_dict[obj]
                        xml_property = etree.SubElement(xml_property_section, "property")
                        xml_property.set("refID",str(ref_id))
                        xml_property.set("refType",str(ref_type))
                        if attribute == obj.ident_attrib:
                            xml_property.text = attribute.value[0]
                        else:
                            xml_property.text = "füllen!"


        xml_repo = etree.SubElement(xml_parent, "repository")
        xml_id_mapping = etree.SubElement(xml_repo, "IDMapping")

        for i,id in enumerate(id_dict.values()):
            xml_id = etree.SubElement(xml_id_mapping,"ID")
            xml_id.set("k",str(i+1))
            xml_id.set("v",str(id))

        attribute_dict = handle_property_type_section()
        handle_property_section()

    def handle_relation_section(xml_parent):
        xml_relation_section = etree.SubElement(xml_parent, "relationSection")

        xml_id_mapping = etree.SubElement(xml_relation_section, "IDMapping")
        xml_relation = etree.SubElement(xml_relation_section, "relation")
        xml_relation.set("name","default")

        pass


    def export(main_window, path):
        xml_boq_export = handle_header(main_window,"bsExport")
        xml_elementsection,id_dict = handle_elementsection(main_window,xml_boq_export)
        xml_link_section = etree.SubElement(xml_boq_export, "linkSection")
        xml_repository = handle_repository(main_window,xml_boq_export,id_dict)
        handle_relation_section(xml_boq_export)

        tree = etree.ElementTree(xml_boq_export)

        with open(path, "wb") as f:
            tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")

    path = get_path(main_window,"bs.xml")

    if path:
        export(main_window, path)
        pass

def export_bookmarks(main_window):
    def handle_bookmark_list(xml_parent):
        xml_bookmark_list = etree.SubElement(xml_parent, "cBookmarkList")

        obj:classes.Object
        for obj in classes.Object:
            xml_bookmark = etree.SubElement(xml_bookmark_list, "cBookmark")
            xml_bookmark.set("ID",str(obj.identifier))

            if isinstance(obj.ident_attrib,classes.Attribute):
                xml_bookmark.set("name",str(obj.ident_attrib.value[0]))

            xml_bookmark.set("bkmType","2")
            xml_col = etree.SubElement(xml_bookmark, "col")
            xml_col.set("v", "Type##xs:string")

            attribute = obj.ident_attrib
            xml_col = etree.SubElement(xml_bookmark, "col")
            text = f"{attribute.property_set.name}:{attribute.name}##{attribute.data_type}"
            xml_col.set("v", text)

            for property_set in obj.property_sets:
                for attribute in property_set.attributes:
                    if attribute != obj.ident_attrib:
                        xml_col = etree.SubElement(xml_bookmark, "col")
                        text = f"{property_set.name}:{attribute.name}##{attribute.data_type}"
                        xml_col.set("v",text)

    def export(main_window, path):

        xml_bookmarks = etree.Element("bookmarks")
        xml_bookmarks.set("xmlnsxsi","http://www.w3.org/2001/XMLSchema-instance")
        handle_bookmark_list(xml_bookmarks)
        tree = etree.ElementTree(xml_bookmarks)

        with open(path, "wb") as f:
            tree.write(f, xml_declaration=True, pretty_print=True, encoding="utf-8", method="xml")


    path = get_path(main_window, "bkxml")

    if path:
        export(main_window, path)
        pass