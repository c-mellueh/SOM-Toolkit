from lxml import etree
from . import __version__ as project_version
from PySide6.QtWidgets import QFileDialog,QInputDialog,QLineEdit
from .io_messages import msg_unsaved
from . import constants
from .classes import Group,Object,PropertySet,Attribute,CustomTreeItem,CustomTree
from .io_messages import msg_delete_or_merge
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

    if path:
        widget.clearObjectInput()
        ### OlD FILE

        tree: etree._ElementTree = etree.parse(path)
        projekt_xml: etree._Element = tree.getroot()

        widget.project_name = projekt_xml.attrib.get("Name")
        widget.setWindowTitle(widget.project_name)

        groups_with_duplicates = [group.attrib.get("Fachdisziplin") for group in projekt_xml if
                                  group.tag == "Objekt"]
        groups_without_duplicates = dict.fromkeys(groups_with_duplicates)

        parent = widget.tree.invisibleRootItem()
        for group_name in groups_without_duplicates:
            group = CustomTreeItem(parent, Group(group_name))
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
    project = etree.Element('Project')
    project.set("name", mainWindow.project_name)
    project.set("version", project_version)

    # TODO
    mainWindow.save_path = path
    print(f"Path: {path}")

def save_clicked(mainWindow):
    if mainWindow.save_path is None:
        path = mainWindow.save_as_clicked()
    else:
        save(mainWindow.save_path)
        path = mainWindow.save_path
    return path

def new_file(mainWindow):
    new_file = msg_unsaved(mainWindow.icon)
    if new_file:

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

