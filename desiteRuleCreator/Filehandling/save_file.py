from __future__ import annotations
from typing import TYPE_CHECKING,Type
from PySide6.QtWidgets import QFileDialog, QMessageBox
from lxml import etree
import os

import desiteRuleCreator.Filehandling
from desiteRuleCreator import __version__ as project_version
from desiteRuleCreator.Windows import popups,graphs_window
from desiteRuleCreator.data import constants, classes

if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow


def save_clicked(main_window:MainWindow) -> str:
    if main_window.save_path is None or not main_window.save_path.endswith("xml"):
        path = save_as_clicked(main_window)
    else:
        save(main_window, main_window.save_path)
        path = main_window.save_path
    return path


def save_as_clicked(main_window:MainWindow) -> str:
    if main_window.save_path is not None:
        base_path = os.path.dirname(main_window.save_path)
        path = \
            QFileDialog.getSaveFileName(main_window, "Save XML",base_path, "xml Files (*.DRCxml *.xml )")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, "Save XML", "", "xml Files ( *.DRCxml *.xml)")[0]

    if path:
        save(main_window,path)
    return path


def save(main_window:MainWindow, path:str) -> None:
    def add_parent(xml_item:etree._Element, item: classes.Object|classes.PropertySet|classes.Attribute) -> None:
        if item.parent is not None:
            xml_item.set(constants.PARENT, str(item.parent.identifier))
        else:
            xml_item.set(constants.PARENT, constants.NONE)

    def add_predefined_property_sets() -> None:
        for predefined_pset in classes.PropertySet:
            if predefined_pset.object is None:
                predefined_pset: classes.PropertySet = predefined_pset
                xml_pset = etree.SubElement(xml_project, constants.PREDEFINED_PSET)
                xml_pset.set(constants.NAME, predefined_pset.name)
                xml_pset.set(constants.IDENTIFIER, str(predefined_pset.identifier))
                xml_pset.set(constants.PARENT, constants.NONE)

                for attribute in predefined_pset.attributes:
                    add_attribute(attribute, predefined_pset, xml_pset)

    def add_property_set(property_set: classes.PropertySet, xml_object:etree._Element) -> None:
        xml_pset = etree.SubElement(xml_object, constants.PROPERTY_SET)
        xml_pset.set(constants.NAME, property_set.name)
        xml_pset.set(constants.IDENTIFIER, str(property_set.identifier))
        add_parent(xml_pset, property_set)

        for attribute in property_set.attributes:
            add_attribute(attribute, property_set, xml_pset)

    def add_object(obj: classes.Object) -> None:

        xml_object = etree.SubElement(xml_project, constants.OBJECT)
        xml_object.set(constants.NAME, obj.name)
        xml_object.set(constants.IDENTIFIER, str(obj.identifier))
        xml_object.set("is_concept", str(obj.is_concept))
        add_parent(xml_object, obj)

        for property_set in obj.property_sets:
            add_property_set(property_set, xml_object)

        for script in obj.scripts:
            script: classes.Script = script
            xml_script = etree.SubElement(xml_object, "Script")
            xml_script.set(constants.NAME, script.name)
            xml_script.text = script.code

    def add_attribute(attribute:classes.Attribute, property_set:classes.PropertySet, xml_pset:etree._Element) -> None:
        xml_attribute = etree.SubElement(xml_pset, constants.ATTRIBUTE)
        xml_attribute.set(constants.NAME, attribute.name)
        xml_attribute.set(constants.DATA_TYPE, attribute.data_type)
        xml_attribute.set(constants.VALUE_TYPE, attribute.value_type)
        xml_attribute.set(constants.IDENTIFIER, str(attribute.identifier))
        xml_attribute.set(constants.CHILD_INHERITS_VALUE, str(attribute.child_inherits_values))
        add_parent(xml_attribute, attribute)

        obj = property_set.object
        if obj is not None and attribute == obj.ident_attrib:
            ident = True
        else:
            ident = False

        xml_attribute.set(constants.IS_IDENTIFIER, str(ident))
        add_value(attribute, xml_attribute)

    def add_value(attribute:classes.Attribute, xml_attribute:etree._Element) -> None:
        values = attribute.value
        for value in values:
            xml_value = etree.SubElement(xml_attribute, "Value")
            if attribute.value_type == constants.RANGE:
                xml_from = etree.SubElement(xml_value, "From")
                xml_to = etree.SubElement(xml_value, "To")
                xml_from.text = str(value[0])
                if len(value) > 1:
                    xml_to.text = str(value[1])
            else:
                xml_value.text = str(value)

    def add_node(node: graphs_window.Node,xml_nodes:etree._Element) -> None:
        xml_node = etree.SubElement(xml_nodes, "Node")
        xml_node.set(constants.IDENTIFIER,str(node.uuid))
        xml_node.set(constants.OBJECT.lower(), str(node.object.identifier))
        if node.parent_box is not None:
            xml_node.set(constants.PARENT, str(node.parent_box.uuid))
        else:
            xml_node.set(constants.PARENT,"None")
        xml_node.set(constants.X_POS,str(node.x()))
        xml_node.set(constants.Y_POS,str(node.y()))
        xml_node.set(constants.IS_ROOT,str(node.is_root))
        connection = node.con_dict.get(node.parent_box)
        if connection is not None:
            xml_node.set(constants.CONNECTION,str(connection.connection_type))
        else:
            xml_node.set(constants.CONNECTION, "None")

    main_window.save_path = path

    xml_project = etree.Element(constants.PROJECT)
    xml_project.set(constants.NAME, str(main_window.project.name))
    xml_project.set(constants.VERSION, str(main_window.project.version))
    xml_project.set(constants.AUTHOR,str(main_window.project.author))

    add_predefined_property_sets()
    for obj in classes.Object:
        add_object(obj)

    xml_nodes = etree.SubElement(xml_project, "Nodes")


    for node in graphs_window.Node._registry:
        add_node(node,xml_nodes)




    tree = etree.ElementTree(xml_project)

    with open(path, "wb") as f:
        tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)

    main_window.project.reset_changed()


def close_event(main_window:MainWindow, event):
    status = main_window.project.changed
    if status:
        reply = popups.msg_close()
        if reply == QMessageBox.Save:
            path = desiteRuleCreator.Filehandling.save_file.save_clicked(main_window)
            if not path or path is None:
                return False
            else:
                return True
        elif reply == QMessageBox.No:
            return True
        else:
            return False
    else:
        return True
