from PySide6.QtWidgets import QFileDialog, QInputDialog, QLineEdit, QMessageBox
from lxml import etree
from uuid import uuid4

from . import __version__ as project_version
from . import constants
from .classes import Object, PropertySet, Attribute, CustomTreeItem
from .io_messages import msg_delete_or_merge
from .io_messages import msg_unsaved, msg_close

#from .run import MainWindow

def importData(widget, path=False):
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

    def import_new(widget,projekt_xml):

        widget.project_name = projekt_xml.attrib.get("name")
        version = projekt_xml.attrib.get("version")     #ToDO: add version Error Message

        widget.setWindowTitle(widget.project_name)

        group_dict = dict()

        # for xml_object in projekt_xml:
        #     if xml_object.tag == "Group":
        #         group = Group(xml_object.attrib.get("name"))
        #         group.identifier = xml_object.get("identifier")
        #         group_dict[group.identifier] = group

        #
        #
        # parent = widget.tree.invisibleRootItem()
        # for group_name in groups_without_duplicates:
        #     group = CustomTreeItem(parent, Group(group_name))
        #     group.setText(0, group_name)
        #     parent.addChild(group)
        #     groups_without_duplicates[group_name] = group
        #
        # for xml_object in projekt_xml:
        #     if (xml_object.tag == "Objekt"):
        #         attributes = xml_object.attrib
        #
        #         identifier_string: str = attributes.get("Identifier")
        #         pSet = PropertySet(identifier_string.split(":")[0])
        #         attribute = Attribute(pSet, identifier_string.split(":")[1], [attributes.get("Name")],
        #                               constants.LIST)
        #
        #         group_name = attributes.get("Fachdisziplin")
        #
        #         obj = Object(attributes.get("Name"), attribute)
        #         widget.addObjectToTree(obj, groups_without_duplicates[group_name])
        #         obj.parent = groups_without_duplicates[group_name]._object
        #
        #         for xml_property_set in xml_object:
        #             psetName = xml_property_set.attrib.get("Name")
        #             if psetName in obj.psetNameDict:
        #                 pSet = obj.psetNameDict[psetName]
        #             else:
        #                 pSet = PropertySet(psetName)
        #             for xml_attribute in xml_property_set:
        #                 attrib = xml_attribute.attrib
        #                 name = attrib.get("Name")
        #                 value_type = transform_value_types(attrib.get("Art"))
        #                 data_type = attrib.get("Datentyp")
        #
        #                 value = transform_values(xml_attribute, value_type)
        #
        #                 atrb = Attribute(pSet, name, value, value_type, data_type)
        #                 obj.add_attribute(atrb)
        #
        # widget.tree.resizeColumnToContents(0)
        # widget.save_path = path

    def import_old(widget,projekt_xml):
        widget.project_name = projekt_xml.attrib.get("Name")
        widget.setWindowTitle(widget.project_name)

        groups_with_duplicates = [group.attrib.get("Fachdisziplin") for group in projekt_xml if
                                  group.tag == "Objekt"]
        groups_without_duplicates = dict.fromkeys(groups_with_duplicates)

        parent = widget.tree.invisibleRootItem()
        for group_name in groups_without_duplicates:
            group = CustomTreeItem(parent, Object(group_name,uuid4(),is_concept=True))
            group.setText(0, group_name)
            parent.addChild(group)
            groups_without_duplicates[group_name] = group

        for xml_objects in projekt_xml:
            if (xml_objects.tag == "Objekt"):
                attributes = xml_objects.attrib

                identifier_string: str = attributes.get("Identifier")
                pSet = PropertySet(identifier_string.split(":")[0])
                attribute = Attribute(pSet, identifier_string.split(":")[1], [attributes.get("Name")],
                                      constants.LIST)

                group_name = attributes.get("Fachdisziplin")

                obj = Object(attributes.get("Name"), attribute)
                widget.addObjectToTree(obj, groups_without_duplicates[group_name])
                obj.parent = groups_without_duplicates[group_name]._object

                for xml_property_set in xml_objects:
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


        widget.tree.resizeColumnToContents(0)
        widget.save_path = path

    if path:
        widget.clearObjectInput()
        ### OlD FILE

        tree: etree._ElementTree = etree.parse(path)
        projekt_xml: etree._Element = tree.getroot()

        if projekt_xml.attrib.get("version") is None:
            import_old(widget,projekt_xml)
        else:
            import_new(widget,projekt_xml)





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

    def add_attributes(object,xml_object):
        for attribute in object.attributes:
            xml_attribute = etree.SubElement(xml_object,"Attribute")
            xml_attribute.set("name",attribute.name)
            xml_attribute.set("propertySet",attribute.propertySet.name)
            xml_attribute.set("data_typ",attribute.data_type)
            xml_attribute.set("value_typ",attribute.value_type)
            if attribute == object.identifier:
                ident = "True"
            else:
                ident = "False"
            xml_attribute.set("is_identifier", ident)

            for value in attribute.value:
                xml_value = etree.SubElement(xml_attribute,"Value")
                if attribute.value_type == constants.RANGE:
                    xml_from = etree.SubElement(xml_value,"From")
                    xml_to = etree.SubElement(xml_value,"To")
                    xml_from.text = str(value[0])
                    if len (value)>1:
                        xml_to.text = str(value[1])
                else:
                    xml_value.text = str(value)
    project = etree.Element('Project')
    project.set("name", mainWindow.project_name)
    project.set("version", project_version)



    # TODO
    mainWindow.save_path = path

    # for group in Group.iter.values():
    #     xml_group = etree.SubElement(project,"Group")
    #     xml_group.set("name",group.name)
    #     xml_group.set("identifier",str(group.identifier))
    #     add_attributes(group,xml_group)
    #
    #     if group.parent is not None:
    #         parent_txt = str(group.parent.identifer)
    #     else:parent_txt = "None"
    #     xml_group.set("parent",parent_txt)

    for obj in Object.iter.values():
        xml_object= etree.SubElement(project,"Object")
        xml_object.set("name",obj.name)
        add_attributes(obj,xml_object)
        if obj.parent is not None:
            parent_txt = str(obj.parent.identifier)
        else:
            parent_txt = "None"
        xml_object.set("parent",parent_txt)


    tree = etree.ElementTree(project)

    with open(path,"wb") as f:
        tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)


def save_clicked(mainWindow):
    if mainWindow.save_path is None:
        path = mainWindow.save_as_clicked()
    else:
        save(mainWindow,mainWindow.save_path)
        path = mainWindow.save_path
    return path


def new_file(mainWindow):
    new_file = msg_unsaved(mainWindow.icon)
    if new_file:
        mainWindow.save_path = None
        project_name = QInputDialog.getText(mainWindow, "New Project", "new Project Name:", QLineEdit.Normal, "")

        if project_name[1]:
            mainWindow.setWindowTitle(project_name[0])
            mainWindow.project_name = project_name[0]
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
