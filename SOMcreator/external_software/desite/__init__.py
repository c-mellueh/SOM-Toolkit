from __future__ import annotations
import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from lxml import etree

from ...constants import value_constants

output_date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def handle_header(author: str, export_format: str) -> Element:
    ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    xml_header = etree.Element(f'{{http://www.w3.org/2001/XMLSchema-instance}}{export_format}')
    xml_header.set("user", str(author))
    xml_header.set("date", str(output_date_time))
    xml_header.set("version", "3.0.1")  # TODO: Desite version hinzufügen
    return xml_header
