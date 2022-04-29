from lxml import etree
import os
from classes import Attribute,Object,PropertySet

def openOldFile(path):
    tree = etree.parse(path)
    projekt_xml = tree.getroot()
    attributes = projekt_xml.attrib

    for xml_objects in projekt_xml:
        if (xml_objects.tag == "Objekt"):
            attributes = xml_objects.attrib

            identifier_string:str = attributes.get("Identifier")
            pSet = PropertySet(identifier_string.split(":")[0])
            attribute = Attribute(identifier_string.split(":")[1],attributes.get("Name"),pSet)

            obj = Object(attributes.get("Name"),attribute)

