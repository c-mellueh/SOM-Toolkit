from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QMessageBox
from lxml import etree

import desiteRuleCreator.Filehandling
from desiteRuleCreator import __version__ as project_version
from desiteRuleCreator.Windows.popups import msg_close
from desiteRuleCreator.data import constants, classes
from desiteRuleCreator.data.classes import PropertySet, Object

def save_clicked(main_window) -> str:
    if main_window.save_path is None:
        path = save_as_clicked(main_window)
    else:
        save(main_window, main_window.save_path)
        path = main_window.save_path
    return path


def save_as_clicked(main_window) -> str:
    if main_window.save_path is not None:
        path = \
            QFileDialog.getSaveFileName(main_window, "Save XML", main_window.save_path, "xml Files (*.xml *.DRCxml)")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, "Save XML", "", "xml Files (*.xml *.DRCxml)")[0]

    if path:
        save(main_window,path)
    return path


def save(main_window, path):
    def add_parent(xml_item, item: classes.Object|classes.PropertySet):
        if item.parent is not None:
            xml_item.set(constants.PARENT, str(item.parent.identifier))
        else:
            xml_item.set(constants.PARENT, constants.NONE)

    def add_predefined_property_sets(xml_project):
        for predefined_pset in classes.PropertySet:
            if predefined_pset.object is None:
                predefined_pset: classes.PropertySet = predefined_pset
                xml_pset = etree.SubElement(xml_project, constants.PREDEFINED_PSET)
                xml_pset.set(constants.NAME, predefined_pset.name)
                xml_pset.set(constants.IDENTIFIER, str(predefined_pset.identifier))
                xml_pset.set(constants.PARENT, constants.NONE)

                for attribute in predefined_pset.attributes:
                    add_attribute(attribute, predefined_pset, xml_pset)

    def add_property_set(property_set: PropertySet, xml_object):
        xml_pset = etree.SubElement(xml_object, constants.PROPERTY_SET)
        xml_pset.set(constants.NAME, property_set.name)
        xml_pset.set(constants.IDENTIFIER, str(property_set.identifier))
        add_parent(xml_pset, property_set)

        for attribute in property_set.attributes:
            add_attribute(attribute, property_set, xml_pset)

    def add_object(obj: Object, xml_project):
        def add_aggregation():
            for child in obj.aggregates_to:
                xml_aggregate = etree.SubElement(xml_object,constants.AGGREGATE)
                xml_aggregate.set(constants.AGGREGATES_TO,str(child.identifier))

        xml_object = etree.SubElement(xml_project, constants.OBJECT)
        xml_object.set(constants.NAME, obj.name)
        xml_object.set(constants.IDENTIFIER, str(obj.identifier))
        xml_object.set("is_concept", str(obj.is_concept))
        add_parent(xml_object, obj)
        add_aggregation()

        for property_set in obj.property_sets:
            add_property_set(property_set, xml_object)

        for script in obj.scripts:
            script: classes.Script = script
            xml_script = etree.SubElement(xml_object, "Script")
            xml_script.set(constants.NAME, script.name)
            xml_script.text = script.code
        pass

    def add_attribute(attribute, property_set, xml_pset):
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

    def add_value(attribute, xml_attribute):
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

    main_window.save_path = path

    xml_project = etree.Element(constants.PROJECT)
    xml_project.set(constants.NAME, main_window.project.name)
    xml_project.set(constants.VERSION, project_version)

    add_predefined_property_sets(xml_project)
    for obj in Object:
        add_object(obj, xml_project)

    tree = etree.ElementTree(xml_project)

    with open(path, "wb") as f:
        tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)

    main_window.project.reset_changed()


def close_event(main_window, event):
    status = main_window.project.changed
    if status:
        reply = msg_close()
        if reply == QMessageBox.Save:
            path = desiteRuleCreator.Filehandling.save_file.save_clicked()
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
