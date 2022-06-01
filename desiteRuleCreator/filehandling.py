from PySide6.QtWidgets import QFileDialog, QInputDialog, QLineEdit, QMessageBox, QTreeWidget, QTreeWidgetItem
from lxml import etree
from uuid import uuid4

from . import __version__ as project_version
from . import constants,classes
from .classes import Object, PropertySet, Attribute, CustomTreeItem
from .io_messages import msg_delete_or_merge
from .io_messages import msg_unsaved, msg_close


# from .run import MainWindow


def fill_tree(mainWindow):
    def fill_next_level(objects, item_dict):

        new_item_dict = dict()
        for el in objects:
            parent_widget = item_dict.get(el.parent)
            if parent_widget is not None:
                tree_widget_item = mainWindow.addObjectToTree(el, parent_widget)
                new_item_dict[el] = tree_widget_item

        objects = [obj for obj in objects if obj not in new_item_dict.keys()]

        if objects:
            fill_next_level(objects, new_item_dict)

    item_dict = dict()
    objects = Object.iter
    for obj in objects:
        if obj.parent == None:
            tree_widget_item = mainWindow.addObjectToTree(obj)
            item_dict[obj] = tree_widget_item

    objects = [obj for obj in objects if obj not in item_dict.keys()]

    fill_next_level(objects, item_dict)


def importData(widget, path=False):
    if path:
        widget.clearObjectInput()

        tree: etree._ElementTree = etree.parse(path)
        projekt_xml: etree._Element = tree.getroot()

        if projekt_xml.attrib.get("version") is None:   #OLD FILES
            import_old(projekt_xml)
            widget.project = classes.Project(projekt_xml.attrib.get("Name"),author="CMellueh")
            print(widget.project.name)
        else:
            import_new(projekt_xml)
            widget.project = classes.Project(projekt_xml.attrib.get("name"))
            print(widget.project.name)
        fill_tree(widget)
        widget.ui.tree.resizeColumnToContents(0)
        widget.save_path = path

        widget.setWindowTitle(widget.project.name)

def import_new(projekt_xml: etree._Element):
    def import_attributes(xml_object):
        def transform_new_values(xml_attribute):
            value_type = xml_attribute.attrib.get("value_type")
            value = list()

            if value_type != constants.RANGE:
                for xml_value in xml_attribute:
                    value.append(xml_value.text)

            else:
                for xml_range in xml_attribute:
                    from_to_list = list()
                    for xml_value in xml_range:
                        if xml_value.tag == "From":
                            from_to_list.append(xml_value.text)
                        if xml_value.tag == "To":
                            from_to_list.append(xml_value.text)
                    value.append(from_to_list)
            return value

        pset_dict = {}
        attribute_list = list()
        ident_attrib = xml_object.attrib.get("identifier")
        for xml_attribute in xml_object:
            if xml_attribute.tag == "Attribute":
                pset_name = xml_attribute.attrib.get("propertySet")
                attribute_name = xml_attribute.attrib.get("name")
                data_type = xml_attribute.attrib.get("data_type")
                value_type = xml_attribute.attrib.get("value_type")
                is_identifier = xml_attribute.attrib.get("is_identifier")

                if not pset_name in pset_dict:
                    pset_dict[pset_name] = PropertySet(pset_name)
                pset = pset_dict[pset_name]

                value = transform_new_values(xml_attribute)
                attrib = Attribute(pset, attribute_name, value, value_type, data_type)
                attribute_list.append(attrib)

                if is_identifier == "True":
                    ident_attrib = attrib
        return ident_attrib, pset_dict.values()

    def import_scripts(xml_object,obj):
        for xml_sub in xml_object:
            if xml_sub.tag == "Script":
                name = xml_sub.attrib.get("name")
                code = xml_sub.text
                script = classes.Script(name,obj)
                script.code = code


    def get_obj_data(xml_object):

        name = xml_object.attrib.get("name")
        parent = xml_object.attrib.get("parent")
        identifier = xml_object.attrib.get("identifier")
        is_concept = xml_object.attrib.get("is_concept")
        if is_concept == "True":
            value = True
        else:
            value = False
        is_concept = value
        return name, parent, identifier, is_concept


    ident_dict = dict()
    parent_dict = dict()
    for xml_object in projekt_xml:
        if xml_object.tag == "Object":
            ident_attrib, pset_list = import_attributes(xml_object)
            name, parent, identifer, is_concept = get_obj_data(xml_object)
            obj = Object(name, ident_attrib, is_concept)
            for pset in pset_list:
                obj.add_property_set(pset)

            ident_dict[identifer] = obj
            parent_dict[obj] = parent

            import_scripts(xml_object,obj)

    for obj, parent_txt in parent_dict.items():
        parent = ident_dict.get(parent_txt)
        if parent is not None:
            parent.add_child(obj)


def import_old(projekt_xml):
    def handle_identifier(xml_object):
        attributes = xml_object.attrib
        identifier_string: str = attributes.get("Identifier")
        pSet = PropertySet(identifier_string.split(":")[0])
        attribute = Attribute(pSet, identifier_string.split(":")[1], [attributes.get("Name")],
                              constants.LIST)
        return attribute

    def transform_values(xml_object, value_type):
        value_list = list()
        if value_type == constants.LIST or value_type == constants.FORMAT:
            for xml_value in xml_object:
                value_list.append(xml_value.attrib.get("Wert"))

        if value_type == constants.RANGE:
            for xml_value in xml_object:
                domain = xml_value.attrib.get("Wert").split(":")
                if len(domain) > 1:
                    value_list.append([float(domain[0]), float(domain[1])])
                else:
                    value_list.append(domain)

        return value_list

    def transform_value_types(value_type):
        if value_type == "Wert":
            value_type = constants.LIST
        elif value_type == "Bereich":
            value_type = constants.RANGE
        elif value_type == "Format":
            value_type = constants.FORMAT
        else:
            raise ImportWarning(f"Imported ValueType {value_type} not known")
        return value_type

    fachdisziplinen = [obj.attrib.get("Fachdisziplin") for obj in projekt_xml if obj.tag == "Objekt"]
    fachdisziplinen = list(set(fachdisziplinen))

    fachdisziplinen_dict = dict()
    for fd in fachdisziplinen:
        obj = Object(fd, str(uuid4()), None, True)
        fachdisziplinen_dict[fd] = obj

    for xml_object in projekt_xml:

        if (xml_object.tag == "Objekt"):
            ident_attrib = handle_identifier(xml_object)

            group_name = xml_object.attrib.get("Fachdisziplin")
            obj = Object(xml_object.attrib.get("Name"), ident_attrib)
            obj.add_attribute(ident_attrib)
            obj.parent = fachdisziplinen_dict[group_name]

            for xml_property_set in xml_object:
                psetName = xml_property_set.attrib.get("Name")
                if psetName in obj.psetNameDict:
                    pSet = obj.psetNameDict[psetName]
                else:
                    pSet = PropertySet(psetName)

                for xml_attribute in xml_property_set:
                    attrib = xml_attribute.attrib
                    name = attrib.get("Name")
                    value_type = transform_value_types(attrib.get("Art"))
                    data_type = attrib.get("Datentyp")

                    value = transform_values(xml_attribute, value_type)
                    atrb = Attribute(pSet, name, value, value_type, data_type)
                    obj.add_attribute(atrb)


def save_as_clicked(mainWindow):
    if mainWindow.save_path is not None:
        path = \
            QFileDialog.getSaveFileName(mainWindow, "Save XML", mainWindow.save_path, "xml Files (*.xml *.DRCxml)")[0]
    else:
        path = QFileDialog.getSaveFileName(mainWindow, "Save XML", "", "xml Files (*.xml *.DRCxml)")[0]

    if path:
        mainWindow.save(path)
    return path


def save(mainWindow, path):

    def add_parent(xml_object,obj):
        if obj.parent is not None:
            xml_object.set(constants.PARENT, str(obj.parent.identifier))
        else:
            xml_object.set(constants.PARENT, constants.NONE)

    def add_predefined_property_sets(xml_project):
        for predefined_pset in classes.PropertySet.iter:
            predefined_pset:classes.PropertySet = predefined_pset
            if predefined_pset.is_parent:
                xml_pset = etree.SubElement(xml_project,"PredefinedPropertySet")
                xml_pset.set(constants.NAME,predefined_pset.name)
                xml_pset.set(constants.IDENTIFIER,str(predefined_pset.identifier))
                xml_pset.set(constants.PARENT,constants.NONE)

                for attribute in predefined_pset.attributes:
                    add_attribute(attribute,predefined_pset,xml_pset)

    def add_property_set(property_set:PropertySet,xml_object):
        xml_pset = etree.SubElement(xml_object, "PropertySet")
        xml_pset.set(constants.NAME, property_set.name)
        xml_pset.set(constants.IDENTIFIER, str(property_set.identifier))
        add_parent(xml_pset,property_set)

        for attribute in property_set.attributes:
            add_attribute(attribute,property_set,xml_pset)


    def add_object(obj:Object,xml_project):
        xml_object = etree.SubElement(xml_project, "Object")
        xml_object.set(constants.NAME, obj.name)
        xml_object.set(constants.IDENTIFIER, str(obj.identifier))
        xml_object.set("is_concept", str(obj.is_concept))
        add_parent(xml_object,obj)

        for property_set in obj.property_sets:
            add_property_set(property_set,xml_object)

        for script in obj.scripts:
            script:classes.Script = script
            xml_script = etree.SubElement(xml_object,"Script")
            xml_script.set(constants.NAME,script.name)
            xml_script.text = script.code
        pass

    def add_attribute(attribute,property_set, xml_pset):
        xml_attribute = etree.SubElement(xml_pset, "Attribute")
        xml_attribute.set(constants.NAME, attribute.name)
        xml_attribute.set(constants.DATA_TYPE, attribute.data_type)
        xml_attribute.set(constants.VALUE_TYPE, attribute.value_type)
        xml_attribute.set(constants.IDENTIFIER, str(attribute.identifier))

        add_parent(xml_attribute,attribute)

        obj = property_set.object
        if obj is not None and attribute == obj.identifier:
            ident = "True"
        else:
            ident = "False"

        xml_attribute.set("is_identifier", ident)
        add_value(attribute,xml_attribute)

    def add_value(attribute,xml_attribute):
            value = attribute.value
            xml_value = etree.SubElement(xml_attribute, "Value")
            if attribute.value_type == constants.RANGE:
                xml_from = etree.SubElement(xml_value, "From")
                xml_to = etree.SubElement(xml_value, "To")
                xml_from.text = str(value[0])
                if len(value) > 1:
                    xml_to.text = str(value[1])
            else:
                xml_value.text = str(value)






    mainWindow.save_path = path

    xml_project = etree.Element('Project')
    xml_project.set("name", mainWindow.project.name)
    xml_project.set("version", project_version)

    add_predefined_property_sets(xml_project)
    for obj in Object.iter:
        add_object(obj,xml_project)

    tree = etree.ElementTree(xml_project)

    with open(path, "wb") as f:
        tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)

    mainWindow.project.reset_changed()

def save_clicked(mainWindow):
    if mainWindow.save_path is None:
        path = mainWindow.save_as_clicked()
    else:
        save(mainWindow, mainWindow.save_path)
        path = mainWindow.save_path
    return path


def new_file(mainWindow):
    new_file = msg_unsaved(mainWindow.icon)
    if new_file:
        mainWindow.save_path = None
        project_name = QInputDialog.getText(mainWindow, "New Project", "new Project Name:", QLineEdit.Normal, "")

        if project_name[1]:
            mainWindow.project = classes.Project(project_name[0])
            mainWindow.setWindowTitle(mainWindow.project.name)
            mainWindow.project.name = project_name[0]
            mainWindow.clear_all()


def openFile_dialog(mainWindow, path=False):
    if Object.iter:
        result = msg_delete_or_merge(mainWindow.icon)
        if result is None:
            return
        elif result:
            mainWindow.clear_all()
            mainWindow.openFile(path)
        else:
            mainWindow.merge_new_file()
            mainWindow.openFile(path)

    else:
        mainWindow.openFile(path)


def merge_new_file(mainWindow):
    print("MERGE NEEDS TO BE PROGRAMMED")  # TODO: Write Merge


def close_event(mainWindow, event):
    status = mainWindow.project.changed
    if status:
        reply = msg_close(mainWindow.icon)
        if reply == QMessageBox.Save:
            path = mainWindow.save_clicked()
            if not path or path is None:
                event.ignore()
            else:
                event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()
